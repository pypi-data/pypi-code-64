# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality for Dataset consumption configuration."""

import re

from azureml.data.constants import DIRECT_MODE, DOWNLOAD_MODE, MOUNT_MODE


class DatasetConsumptionConfig:
    """Represent how to deliver the dataset to a compute target.

    :param name: The name of the dataset in the run, which can be different to the registered name.
        The name will be registered as environment variable and can be used in data plane.
    :param dataset: The dataset that will be consumed in the run.
    :type dataset: azureml.data.abstract_dataset.AbstractDataset
        or azureml.pipeline.core.PipelineParameter
        or azureml.data.output_dataset_config.OutputDatasetConfig
    :type name: str
    :param mode: Defines how the dataset should be delivered to the compute target. There are three modes:
        1. 'direct': consume the dataset as dataset.
        2. 'download': download the dataset and consume the dataset as downloaded path.
        3. 'mount': mount the dataset and consume the dataset as mount path.
    :type mode: str
    :param path_on_compute: The target path on the compute to make the data available at. The folder structure
            of the source data will be kept, however, we might add prefixes to this folder structure to avoid
            collision. Use ``tabular_dataset.to_path`` to see the output folder structure.
    :type path_on_compute: str
    """

    _SUPPORTED_MODE = {DIRECT_MODE, DOWNLOAD_MODE, MOUNT_MODE}

    def __init__(self, name, dataset, mode=DIRECT_MODE, path_on_compute=None):
        """Represent how to deliver the dataset to the compute target.

        :param name: The name of the dataset in the run, which can be different to the registered name.
            The name will be registered as environment variable and can be used in data plane.
        :type name: str
        :param dataset: The dataset to be delivered, as a Dataset object, Pipeline Parameter that ingests a Dataset,
            a tuple of (workspace, Dataset name), or a tuple of (workspace, Dataset name, Dataset version).
            If only a name is provided, the DatasetConsumptionConfig will use the latest version of the Dataset.
        :type dataset: azureml.core.dataset.Dataset
            or azureml.pipeline.core.PipelineParameter
            or tuple(azureml.core.workspace.Workspace, str)
            or tuple(azureml.core.workspace.Workspace, str, str)
            or azureml.data.output_dataset_config.OutputDatasetConfig
        :param mode: Defines how the dataset should be delivered to the compute target. There are three modes:
            1. 'direct': consume the dataset as dataset.
            2. 'download': download the dataset and consume the dataset as downloaded path.
            3. 'mount': mount the dataset and consume the dataset as mount path.
        :type mode: str
        :param path_on_compute: The target path on the compute to make the data available at. The folder structure
            of the source data will be kept, however, we might add prefixes to this folder structure to avoid
            collision. We recommend calling `tabular_dataset.to_path` to see the output folder structure.
        :type path_on_compute: str
        """
        mode = mode.lower()
        DatasetConsumptionConfig._validate_mode(dataset, mode)

        from azureml.core import Dataset
        if isinstance(dataset, tuple):
            ws, ds_name = dataset[0], dataset[1]
            try:
                ds_version = dataset[2]
            except IndexError:
                # No version specified, use latest
                ds_version = 'latest'
            dataset = Dataset.get_by_name(ws, ds_name, ds_version)

            if ds_version == 'latest':
                dataset._consume_latest = True

        self.dataset = self._validate_if_pipeline_parameter(dataset)
        self.name = self._validate_name(name) if name else None
        self.mode = mode
        self.path_on_compute = path_on_compute

    @staticmethod
    def _validate_name(name):
        from azureml.exceptions import UserErrorException

        if re.search(r"^[a-zA-Z_]+[a-zA-Z0-9_]*$", name):
            return name
        raise UserErrorException(
            "Invalid name {}. Dataset input name can only be alphanumeric characters and underscore, ".format(name) +
            "and must not begin with a number."
        )

    @staticmethod
    def _validate_mode(dataset, mode):
        from azureml.data import TabularDataset
        from azureml.data.output_dataset_config import OutputTabularDatasetConfig
        from azureml.exceptions import UserErrorException

        if mode not in DatasetConsumptionConfig._SUPPORTED_MODE:
            raise UserErrorException("Invalid mode '{}'. Mode can only be mount, download, or direct".format(mode))

        try:
            # Expose the underlying dataset for validation
            dataset = dataset.default_value
        except AttributeError:
            pass

        if isinstance(dataset, TabularDataset) or isinstance(dataset, OutputTabularDatasetConfig):
            if mode == 'download' or mode == 'mount':
                raise UserErrorException("{} does not support {}. Only FileDataset supports {}".format(
                    type(dataset), mode, mode
                ))

    @staticmethod
    def _validate_if_pipeline_parameter(param):
        from azureml.data import FileDataset, TabularDataset
        from azureml.exceptions import UserErrorException
        try:
            default_value = param.default_value
        except AttributeError:
            # Passed in param is of type Dataset, skip validation
            return param
        if not (isinstance(default_value, FileDataset) or isinstance(default_value, TabularDataset)):
            raise UserErrorException("Invalid PipelineParameter with default value '{}. Default value must be of "
                                     "types: {} or {}".format(default_value, FileDataset.__name__,
                                                              TabularDataset.__name__))
        return param

    def as_download(self, path_on_compute=None):
        """Set the mode to download.

        In the submitted run, files in the dataset will be downloaded to local path on the compute target.
        The download location can be retrieved from argument values and the input_datasets field of the run context.

        .. code-block:: python

            # Given a run submitted with dataset input like this:
            dataset_input = dataset.as_named_input('input_1').as_download()
            experiment.submit(ScriptRunConfig(source_directory, arguments=[dataset_input]))


            # Following are sample codes running in context of the submitted run:

            # The download location can be retrieved from argument values
            import sys
            download_location = sys.argv[1]

            # The download location can also be retrieved from input_datasets of the run context.
            from azureml.core import Run
            download_location = Run.get_context().input_datasets['input_1']

        .. remarks::

            When the dataset is created from path of a single file, the download location will be path of the single
            downloaded file. Otherwise, the download location will be path of the enclosing folder for all the
            downloaded files.

            If path_on_compute starts with a /, then it will be treated as an absolute path. If it doesn't start
            with a /, then it will be treated as a relative path relative to the working directory. If you have
            specified an absolute path, please make sure that the job has permission to write to that directory.

        :param path_on_compute: The target path on the compute to make the data available at.
        :type path_on_compute: str
        """
        return DatasetConsumptionConfig(name=self.name, dataset=self.dataset,
                                        mode='download', path_on_compute=path_on_compute)

    def as_mount(self, path_on_compute=None):
        """Set the mode to mount.

        In the submitted run, files in the datasets will be mounted to local path on the compute target.
        The mount point can be retrieved from argument values and the input_datasets field of the run context.

        .. code-block:: python

            # Given a run submitted with dataset input like this:
            dataset_input = dataset.as_named_input('input_1').as_mount()
            experiment.submit(ScriptRunConfig(source_directory, arguments=[dataset_input]))


            # Following are sample codes running in context of the submitted run:

            # The mount point can be retrieved from argument values
            import sys
            mount_point = sys.argv[1]

            # The mount point can also be retrieved from input_datasets of the run context.
            from azureml.core import Run
            mount_point = Run.get_context().input_datasets['input_1']

        .. remarks::

            When the dataset is created from path of a single file, the mount point will be path of the single mounted
            file. Otherwise, the mount point will be path of the enclosing folder for all the mounted files.

            If path_on_compute starts with a /, then it will be treated as an absolute path. If it doesn't start
            with a /, then it will be treated as a relative path relative to the working directory. If you have
            specified an absolute path, please make sure that the job has permission to write to that directory.

        :param path_on_compute: The target path on the compute to make the data available at.
        :type path_on_compute: str
        """
        return DatasetConsumptionConfig(name=self.name, dataset=self.dataset,
                                        mode='mount', path_on_compute=path_on_compute)
