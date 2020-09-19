# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utils for evaluations using the EvalMetricsGraph."""

from __future__ import absolute_import
from __future__ import division
# Standard __future__ imports
from __future__ import print_function

from typing import Any, Dict, Iterable, List, Optional, Text

import apache_beam as beam
from tensorflow_model_analysis import constants
from tensorflow_model_analysis import model_util
from tensorflow_model_analysis import types
from tensorflow_model_analysis.eval_metrics_graph import eval_metrics_graph
from tensorflow_model_analysis.metrics import metric_types


def metric_computations_using_eval_saved_model(
    model_name: Text,
    model_loader: types.ModelLoader,
    batch_size: Optional[int] = None) -> metric_types.MetricComputations:
  """Returns computations for computing metrics natively using EvalMetricsGraph.

  Note that unlike other computations, there is no direct key associated with
  this computation. Instead the final computation returns the actual internal
  metric keys used by the model such as 'auc', etc).

  Args:
    model_name: Name of model.
    model_loader: Loader for shared model containing eval saved model to use for
      metric computations.
    batch_size: Batch size to use during evaluation (testing only).
  """
  return [
      # _EvalSavedModelPreprocessor loads the EvalSavedModel into memory under a
      # shared handle that can be used by subsequent steps. Combiner lifting and
      # producer-consumer fusion should ensure that the processor and combiner
      # run in the same process and memory space.
      #
      # TODO(b/69566045): Remove model loading from _EvalSavedModelPreprocessor
      # and move model loading to _EvalSavedModelCombiner.setup after it is
      # available in Beam.
      metric_types.MetricComputation(
          keys=[],
          preprocessor=_EvalSavedModelPreprocessor(model_name, model_loader),
          combiner=_EvalSavedModelCombiner(model_name, model_loader,
                                           batch_size))
  ]


class _EvalSavedModelPreprocessor(model_util.DoFnWithModels):
  """A DoFn that loads the EvalSavedModel and returns the input."""

  def __init__(self, model_name: Text, model_loader: types.ModelLoader):
    super(_EvalSavedModelPreprocessor,
          self).__init__({model_name: model_loader})

  def process(self, extracts: types.Extracts) -> Iterable[bytes]:
    yield extracts[constants.INPUT_KEY]


def _add_metric_variables(  # pylint: disable=invalid-name
    left: types.MetricVariablesType,
    right: types.MetricVariablesType) -> types.MetricVariablesType:
  """Returns left and right metric variables combined."""
  if left is not None and right is not None:
    if len(left) != len(right):
      raise ValueError('metric variables lengths should match, but got '
                       '%d and %d' % (len(left), len(right)))
    return [x + y for x, y in zip(left, right)]
  elif left is not None:
    return left
  else:
    return right


def _metrics_by_output_name(
    metrics: Dict[Text, Any]) -> Dict[Text, Dict[Text, Any]]:
  """Returns metrics grouped by output name."""
  # If an output (head) name is used in an estimator, the metric names are of
  # the form "<metric_name>/<head>". This code checks for the existence of a '/'
  # where the trailing suffix is shared by at least three metrics. This
  # seemingly random choice of three was choose to avoid standard cases such as
  # 'label/mean' and 'prediction/mean' that are used by estimators but are not
  # indicative of a multi-headed model.
  result = {}
  for name, value in metrics.items():
    index = name.rfind('/')
    if index == -1:
      return {'': metrics}
    output_name = name[index + 1:]
    if output_name not in result:
      result[output_name] = {}
    result[output_name][name[:index]] = value
  for output_name, values in result.items():
    if len(values) <= 2:
      return {'': metrics}
  return result


class _AggState(object):
  """Combine state for AggregateCombineFn.

  There are two parts to the state: the metric variables (the actual state),
  and a list of FeaturesPredictionsLabels or other inputs. See
  _AggregateCombineFn for why we need this.
  """

  __slots__ = ['metric_variables', 'inputs', 'total_input_byte_size']

  def __init__(self):
    self.metric_variables = None  # type: Optional[types.MetricVariablesType]
    self.inputs = []  # type: List[bytes]
    self.total_input_byte_size = 0

  def copy_from(self, other: '_AggState'):
    if other.metric_variables:
      self.metric_variables = other.metric_variables
    self.inputs = other.inputs

  def __iadd__(self, other: '_AggState') -> '_AggState':
    self.metric_variables = _add_metric_variables(self.metric_variables,
                                                  other.metric_variables)
    self.inputs.extend(other.inputs)
    return self

  def add_input(self, new_input: bytes):
    self.inputs.append(new_input)
    self.total_input_byte_size += len(new_input)

  def clear_inputs(self):
    del self.inputs[:]
    self.total_input_byte_size = 0

  def add_metrics_variables(self, metric_variables: types.MetricVariablesType):
    self.metric_variables = _add_metric_variables(self.metric_variables,
                                                  metric_variables)


@beam.typehints.with_input_types(bytes)
@beam.typehints.with_output_types(Dict[metric_types.MetricKey, Any])
class _EvalSavedModelCombiner(model_util.CombineFnWithModels):
  """Aggregate combine function.

  This function really does three things:
    1. Batching of FeaturesPredictionsLabels.
    3. "Partial reduction" of these batches by sending this through the
       "intro metrics" step.
    3. The "normal" combining of MetricVariables.

  What we really want to do is conceptually the following:
  Predictions | GroupByKey() | KeyAwareBatchElements()
              | ParDo(IntroMetrics()) | CombineValues(CombineMetricVariables()).

  but there's no way to KeyAwareBatchElements in Beam, and no way to do partial
  reductions either. Hence, this CombineFn has to do the work of batching,
  partial reduction (intro metrics), and actual combining, all in one.

  We do this by accumulating FeaturesPredictionsLabels in the combine state
  until we accumulate a large enough batch, at which point we send them
  through the "intro metrics" step. When merging, we merge the metric variables
  and accumulate FeaturesPredictionsLabels accordingly. We do one final
  "intro metrics" and merge step before producing the final output value.

  See also:
  BEAM-3737: Key-aware batching function
  (https://issues.apache.org/jira/browse/BEAM-3737).
  """

  # We really want the batch size to be adaptive like it is in
  # beam.BatchElements(), but there isn't an easy way to make it so. For now
  # we will limit stored inputs to a max overall byte size.
  # TODO(b/73789023): Figure out how to make this batch size dynamic.
  _TOTAL_INPUT_BYTE_SIZE_THRESHOLD = 16 << 20  # 16MiB
  _BATCH_SIZE = 1000

  def __init__(self,
               model_name: Text,
               model_loader: types.ModelLoader,
               batch_size: Optional[int] = None):
    super(_EvalSavedModelCombiner, self).__init__({model_name: model_loader})
    self._model_name = model_name
    self._batch_size = (
        batch_size if batch_size is not None else self._BATCH_SIZE)
    self._eval_metrics_graph = None  # type: eval_metrics_graph.EvalMetricsGraph
    self._batch_size_beam_metric = beam.metrics.Metrics.distribution(
        constants.METRICS_NAMESPACE, 'eval_saved_model_combiner_batch_size')
    self._total_input_byte_size_beam_metric = beam.metrics.Metrics.distribution(
        constants.METRICS_NAMESPACE,
        'eval_saved_model_combiner_total_input_byte_size')

  def _maybe_do_batch(self,
                      accumulator: _AggState,
                      force: bool = False) -> None:
    """Maybe intro metrics and update accumulator in place.

    Checks if accumulator has enough FPLs for a batch, and if so, does the
    intro metrics for the batch and updates accumulator in place.

    Args:
      accumulator: Accumulator. Will be updated in place.
      force: Force intro metrics even if accumulator has less FPLs than the
        batch size or max byte size.
    """

    if self._eval_metrics_graph is None:
      self._setup_if_needed()
      self._eval_metrics_graph = self._loaded_models[self._model_name]
    batch_size = len(accumulator.inputs)
    if (force or batch_size >= self._batch_size or
        accumulator.total_input_byte_size >=
        self._TOTAL_INPUT_BYTE_SIZE_THRESHOLD):
      if accumulator.inputs:
        self._batch_size_beam_metric.update(batch_size)
        self._total_input_byte_size_beam_metric.update(
            accumulator.total_input_byte_size)
        inputs_for_metrics = accumulator.inputs
        if inputs_for_metrics:
          accumulator.add_metrics_variables(
              self._eval_metrics_graph.metrics_reset_update_get_list(
                  inputs_for_metrics))
        else:
          # Call to metrics_reset_update_get_list does a reset prior to the
          # metrics update, but does not handle empty updates. Explicitly
          # calling just reset here, to make the flow clear.
          self._eval_metrics_graph.reset_metric_variables()
        accumulator.clear_inputs()

  def create_accumulator(self) -> _AggState:
    return _AggState()

  def add_input(self, accumulator: _AggState, elem: bytes) -> _AggState:
    accumulator.add_input(elem)
    self._maybe_do_batch(accumulator)
    return accumulator

  def merge_accumulators(self, accumulators: Iterable[_AggState]) -> _AggState:
    result = self.create_accumulator()
    for acc in accumulators:
      result += acc
      # Compact within the loop to avoid accumulating too much data.
      #
      # During the "map" side of combining merging happens with memory limits
      # but on the "reduce" side it's across all bundles (for a given key).
      #
      # So we could potentially accumulate get num_bundles * batch_size
      # elements if we don't process the batches within the loop, which
      # could cause OOM errors (b/77293756).
      self._maybe_do_batch(result)
    return result

  def compact(self, accumulator: _AggState) -> _AggState:
    self._maybe_do_batch(accumulator, force=True)  # Guaranteed compaction.
    return accumulator

  def extract_output(
      self, accumulator: _AggState) -> Dict[metric_types.MetricKey, Any]:
    # It's possible that the accumulator has not been fully flushed, if it was
    # not produced by a call to compact (which is not guaranteed across all Beam
    # Runners), so we defensively flush it here again, before we extract data
    # from it, to ensure correctness.
    self._maybe_do_batch(accumulator, force=True)
    result = {}
    if accumulator.metric_variables:
      eval_saved_model = self._loaded_models[self._model_name]
      grouped_metrics = _metrics_by_output_name(
          eval_saved_model.metrics_set_variables_and_get_values(
              accumulator.metric_variables))
      for output_name, metrics in grouped_metrics.items():
        for name, value in metrics.items():
          key = metric_types.MetricKey(
              name=name, model_name=self._model_name, output_name=output_name)
          result[key] = value
    return result
