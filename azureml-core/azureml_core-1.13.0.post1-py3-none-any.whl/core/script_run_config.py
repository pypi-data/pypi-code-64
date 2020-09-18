# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality to manage configuration for submitting training runs in Azure Machine Learning."""
import logging
from copy import deepcopy

from azureml._base_sdk_common.tracking import global_tracking_info_registry
from azureml._logging import ChainedIdentity
from azureml.data._dataset import _Dataset
from azureml.data._loggerfactory import collect_datasets_usage
from azureml.data.constants import _SCRIPT_RUN_SUBMIT_ACTIVITY, _DATASET_ARGUMENT_TEMPLATE, \
    _SKIP_VALIDATE_DATASETS, _DATASET_OUTPUT_ARGUMENT_TEMPLATE
from azureml.core.runconfig import Data, RunConfiguration, TensorflowConfiguration, MpiConfiguration
from azureml.exceptions import UserErrorException, RunConfigurationException
from azureml.data.datapath import DataPath, DataPathComputeBinding

from ._experiment_method import experiment_method


module_logger = logging.getLogger(__name__)


def submit(script_run_config, workspace, experiment_name, run_id=None, _parent_run_id=None):
    """Submit and return a script run.

    This function creates an :class:`azureml.core.Experiment`, applies the run configuration,
    submits the run, and returns a :class:`azureml.core.script_run.ScriptRun` object.

    :param script_run_config: The configuration information for the run.
    :type script_run_config:  azureml.core.script_run_config.ScriptRunConfig
    :param workspace: A workspace in which to create the experiment.
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name: The name of the experiment.
    :type experiment_name: str
    :param run_id: An optional ID of the run.
    :type run_id: str
    :param _parent_run_id: Internal use only.
    :type _parent_run_id: str
    :return: A script run object.
    :rtype: azureml.core.script_run.ScriptRun
    """
    from azureml.core import Experiment
    from azureml._execution import _commands
    from azureml._project.project import Project

    experiment = Experiment(workspace, experiment_name, _create_in_cloud=False)
    project = Project(directory=script_run_config.source_directory, experiment=experiment)

    run_config = get_run_config_from_script_run(script_run_config)
    inputs, _ = _update_args_and_io(workspace, run_config)
    collect_datasets_usage(module_logger, _SCRIPT_RUN_SUBMIT_ACTIVITY, inputs,
                           workspace, run_config.target)
    run = _commands.start_run(project, run_config,
                              telemetry_values=script_run_config._telemetry_values,
                              run_id=run_id, parent_run_id=_parent_run_id)
    run.add_properties(global_tracking_info_registry.gather_all(script_run_config.source_directory))

    return run


def get_run_config_from_script_run(script_run_config):
    """Get the RunConfiguration object with parameters copied from the ScriptRunConfig.

    :param script_run_config: The ScriptRunConfig from which to get the run configuration.
    :type script_run_config:  azureml.core.script_run_config.ScriptRunConfig
    :return: The run configuration.
    :rtype: azureml.core.runconfig.RunConfiguration
    """
    # Gets a deep copy of run_config
    run_config = RunConfiguration._get_run_config_object(
        path=script_run_config.source_directory, run_config=script_run_config.run_config)

    if script_run_config.arguments:
        # Gets a deep copy of arguments as arguments contains not only simple type (e.g. DatasetConsumptionConfig)
        run_config.arguments = deepcopy(script_run_config.arguments)

    if script_run_config.script:
        run_config.script = script_run_config.script

    return run_config


def _update_args_and_io(workspace, run_config):
    from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
    from azureml.data.output_dataset_config import OutputDatasetConfig
    from azureml.core.runconfig import OutputData

    if not workspace:
        raise RuntimeError("Argument workspace cannot be None.")

    input_data = []
    output_data = {}

    def update_args_and_io(args, inputs, outputs):
        for index in range(len(args)):
            if isinstance(args[index], _Dataset):
                raise UserErrorException("Dataset cannot be used without providing a name for the run. Please provide "
                                         "a name by calling the as_named_input instance method on dataset.")
            elif isinstance(args[index], Data):
                raise UserErrorException("azureml.core.runconfig.Data is not supported in arguments. Only "
                                         "DatasetConsumptionConfig is supported. It can be created by calling "
                                         "dataset.as_named_input('my_dataset')")
            elif isinstance(args[index], DatasetConsumptionConfig):
                dataset = args[index]
                if dataset.name in inputs:
                    module_logger.warning(("Dataset with the name {} is already defined in the data section of the "
                                           "RunConfiguration. The DatasetConsumptionConfig in the data section will "
                                           "be used to materialized the data").format(dataset.name))
                else:
                    inputs[dataset.name] = dataset
                args[index] = _DATASET_ARGUMENT_TEMPLATE.format(dataset.name)
            elif isinstance(args[index], OutputDatasetConfig):
                output = args[index]
                args[index] = _DATASET_OUTPUT_ARGUMENT_TEMPLATE.format(output.name)
                outputs[output.name] = output
            elif isinstance(args[index], OutputData):
                raise UserErrorException("Arguments does not support OutputData. You need to pass the placeholder "
                                         "into arguments which will be replaced with the output directory where "
                                         "your script should write the output to. The placeholder has the following "
                                         "format: {}:name where name is the key of the OutputData in the "
                                         "output_data section of the run "
                                         "configuration.".format(_DATASET_OUTPUT_ARGUMENT_TEMPLATE))

    def update_io(inputs, outputs):
        for key, value in inputs.items():
            if isinstance(value, _Dataset):
                raise UserErrorException("Dataset cannot be used without providing a name for the run. Please provide "
                                         "a name by calling the as_named_input instance method on dataset.")
            elif isinstance(value, DatasetConsumptionConfig):
                value.dataset._ensure_saved(workspace)
                inputs[key] = Data.create(value)
                input_data.append(value)

                # Set the environment variable for mount validation
                if value.dataset._consume_latest:
                    env_vars = run_config.environment.environment_variables
                    if _SKIP_VALIDATE_DATASETS not in env_vars:
                        env_vars[_SKIP_VALIDATE_DATASETS] = value.name
                    else:
                        env_vars[_SKIP_VALIDATE_DATASETS] = ",".join([env_vars[_SKIP_VALIDATE_DATASETS], value.name])
            elif isinstance(value, Data):
                input_data.append(value)
            else:
                raise UserErrorException("{} cannot be used as input.".format(type(value).__name__))
        for key, value in outputs.items():
            if isinstance(value, OutputDatasetConfig):
                outputs[key] = output_data[key] = value._to_output_data()
            elif isinstance(value, OutputData):
                output_data[key] = value
            else:
                raise UserErrorException("{} cannot be used as output.".format(type(value).__name__))

    update_args_and_io(run_config.arguments, run_config.data, run_config.output_data)
    update_io(run_config.data, run_config.output_data)

    return input_data, output_data


class ScriptRunConfig(ChainedIdentity):
    """Represents configuration information for submitting a training run in Azure Machine Learning.

    A ScriptRunConfig packages together the configuration information needed to submit a run in Azure ML, including
    the script, compute target, environment, and any distributed job-specific configs.

    Once a script run is configured and submitted with the :meth:`azureml.core.Experiment.submit`,
    a :class:`azureml.core.script_run.ScriptRun` is returned.

    .. remarks::

        The Azure Machine Learning SDK provides you with a series of interconnected classes, that are
        designed to help you train and compare machine learning models that are related by the shared
        problem that they are solving.

        An :class:`azureml.core.Experiment` acts as a logical container for these training runs. A ScriptRunConfig
        object is used to configure the information necessary for submitting a training run as part of an Experiment.
        When a run is submitted using a ScriptRunConfig object, the submit method returns an object of type
        :class:`azureml.core.ScriptRun`. Then returned ScriptRun object gives you programmatic access to information
        about the training run. ScriptRun is a child class of :class:`azureml.core.Run`.

        The key concept to remember is that there are different configuration objects that are used to
        submit an experiment, based on what kind of run you want to trigger. The type of the configuration object
        then informs what child class of Run you get back from the submit method. When you pass a
        ScriptRunConfig object in a call to Experiment's submit method, you get back a ScriptRun object.
        Examples of other run objects returned include :class:`azureml.train.automl.run.AutoMLRun` (returned for
        an AutoML run) and :class:`azureml.pipeline.core.PipelineRun` (returned for a Pipeline run).

        The following sample shows how to submit a training script on your local machine.

        .. code-block:: python

                from azureml.core import ScriptRunConfig, RunConfiguration, Experiment

                # create or load an experiment
                experiment = Experiment(workspace, 'MyExperiment')
                # create or retrieve a compute target
                cluster = workspace.compute_targets['MyCluster']
                # create or retrieve an environment
                env = Environment.get(ws, name='MyEnvironment')
                # configure and submit your training run
                config = ScriptRunConfig(source_directory='.',
                                         script='train.py',
                                         arguments=['--arg1', arg1_val, '--arg2', arg2_val],
                                         compute_target=cluster,
                                         environment=env)
                script_run = experiment.submit(config)

        For more examples showing how to work with ScriptRunConfig, see:

        * the article `Select and use a compute target to train your
          model <https://docs.microsoft.com/azure/machine-learning/how-to-set-up-training-targets>`_
        * these `training
          notebooks <https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/training>`_

    :param source_directory: A local directory containing code files needed for a run.
    :type source_directory: str
    :param script: The file path relative to the source_directory of the script to be run.
    :type script: str
    :param arguments: Optional command-line arguments to pass to the training script.
        Arguments are passed in pairs, for example, ['--arg1', arg1_val, '--arg2', arg2_val].
    :type arguments: builtin.list or str
    :param run_config: Optional run configuration to use.
    :type run_config: azureml.core.runconfig.RunConfiguration
    :param _telemetry_values: Internal use only.
    :type _telemetry_values: dict
    :param compute_target: The compute target where training will happen. This can either be a ComputeTarget
        object, the name of an existing ComputeTarget, or the string "local". If no compute target is
        specified, your local machine will be used.
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param environment: The environment to use for the run. If no environment is specified,
        azureml.core.runconfig.DEFAULT_CPU_IMAGE will be used as the Docker image for the run.
    :type environment: azureml.core.environment.Environment
    :param distributed_job_config: For jobs that require additional distributed job-specific configurations.
    :type distributed_job_config: TensorflowConfiguration or MpiConfiguration
    :param resume_from: The DataPath containing the checkpoint or model files from which to resume the
        experiment.
    :type resume_from: azureml.data.datapath.DataPath
    :param max_run_duration_seconds: The maximum time allowed for the run. The system will attempt to
        automatically cancel the run if it took longer than this value.
        :type max_run_duration_seconds: int
    """

    @experiment_method(submit_function=submit)
    def __init__(self, source_directory, script=None, arguments=None, run_config=None, _telemetry_values=None,
                 compute_target=None, environment=None, distributed_job_config=None, resume_from=None,
                 max_run_duration_seconds=2592000):
        """Class ScriptRunConfig constructor.

        :param source_directory: A local directory containing code files needed for a run.
        :type source_directory: str
        :param script: The file path relative to the source_directory of the script to be run.
        :type script: str
        :param arguments: Optional command-line arguments to pass to the training script.
            Arguments are passed in pairs, for example, ['--arg1', arg1_val, '--arg2', arg2_val].
        :type arguments: builtin.list[str]
        :param run_config: Optional run configuration to use.
        :type run_config: azureml.core.runconfig.RunConfiguration
        :param _telemetry_values: Internal use only.
        :type _telemetry_values: dict
        :param compute_target: The compute target where training will happen. This can either be a ComputeTarget
            object, the name of an existing ComputeTarget, or the string "local". If no compute target is
            specified, your local machine will be used.
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param environment: The environment to use for the run. If no environment is specified,
            azureml.core.runconfig.DEFAULT_CPU_IMAGE will be used as the Docker image for the run.
        :type environment: azureml.core.environment.Environment
        :param distributed_job_config: For jobs that require additional distributed job-specific configurations.
        :type distributed_job_config: TensorflowConfiguration or MpiConfiguration
        :param resume_from: The DataPath containing the checkpoint or model files from which to resume the
            experiment.
        :type resume_from: azureml.data.datapath.DataPath
        :param max_run_duration_seconds: The maximum time allowed for the run. The system will attempt to
            automatically cancel the run if it took longer than this value.
        :type max_run_duration_seconds: int
        """
        self.source_directory = source_directory
        self.script = script
        self.arguments = arguments

        if run_config:
            if run_config.script:
                logging.warning("If 'script' has been provided here and a script file name has been specified in "
                                "'run_config', 'script' provided in ScriptRunConfig initialization will take "
                                "precedence.")
                if not self.script:
                    self.script = run_config.script
            if run_config.arguments:
                logging.warning("If 'arguments' has been provided here and arguments have been specified in "
                                "'run_config', 'arguments' provided in ScriptRunConfig initialization will "
                                "take precedence.")
                if not self.arguments:
                    self.arguments = run_config.arguments

            self.run_config = run_config
        else:
            self.run_config = RunConfiguration()
            self.run_config.target = compute_target if compute_target else "local"
            self.run_config.environment = environment
            self.run_config.max_run_duration_seconds = max_run_duration_seconds

            if distributed_job_config:
                if not isinstance(distributed_job_config, (TensorflowConfiguration, MpiConfiguration)):
                    raise RunConfigurationException("'distributed_job_config' must be a 'TensorflowConfiguration' "
                                                    "or 'MpiConfiguration' object.")
                if isinstance(distributed_job_config, TensorflowConfiguration):
                    self.run_config.tensorflow = distributed_job_config
                    self.run_config.framework = "TensorFlow"
                    self.run_config.communicator = "ParameterServer"
                elif isinstance(distributed_job_config, MpiConfiguration):
                    self.run_config.mpi = distributed_job_config
                    self.run_config.framework = "Python"
                    self.run_config.communicator = "IntelMpi"

        if resume_from:
            if not isinstance(resume_from, DataPath):
                raise UserErrorException("resume_from parameter should be of type DataPath. "
                                         "Found {}.".format(type(resume_from)))
            outputs_data_reference = resume_from. \
                create_data_reference(data_reference_name="MODEL_LOCATION",
                                      datapath_compute_binding=DataPathComputeBinding(mode="mount"))

            self.arguments.extend(["--resume-from", outputs_data_reference])

        self._telemetry_values = _telemetry_values
