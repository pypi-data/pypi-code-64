# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality for managing the configuration of experiment runs in Azure Machine Learning.

The key class in this module is :class:`azureml.core.runconfig.RunConfiguration`, which encapsulates
information necessary to submit a training run on a specified compute target. The configuration
includes a wide set of behavior definitions, such as whether to use an existing Python environment
or to use a Conda environment that's built from a specification.

Other configuration classes in the module are accessed through RunConfiguration.
"""
import json
import os
import logging
import collections
import ruamel.yaml

from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml._base_sdk_common.abstract_run_config_element import _AbstractRunConfigElement
from azureml._base_sdk_common.field_info import _FieldInfo
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.compute_target import AbstractComputeTarget
from azureml.core.compute import ComputeTarget
from azureml.core.container_registry import ContainerRegistry as Cr
from azureml.core.environment import Environment, DEFAULT_CPU_IMAGE, DEFAULT_GPU_IMAGE
from azureml.core.run import Run
from azureml.core._serialization_utils import _serialize_to_dict, _deserialize_and_add_to_object, \
    _check_before_comment, _yaml_set_comment_before_after_key_with_error

from azureml._base_sdk_common.common import RUNCONFIGURATION_EXTENSION, AML_CONFIG_DIR,\
    AZUREML_DIR, COMPUTECONTEXT_EXTENSION, to_camel_case, to_snake_case, get_run_config_dir_path, \
    get_run_config_dir_name
from azureml.exceptions import UserErrorException, RunConfigurationException

# Following imports are kept around for backward compatability
# noqa # pylint: disable=unused-import
from azureml.core.environment import SparkSection, DockerSection, SparkEnvironment, DockerEnvironment, \
    PythonEnvironment, PythonSection
from azureml.core.databricks import MavenLibrary, PyPiLibrary, RCranLibrary, JarLibrary, EggLibrary, \
    DatabricksCluster, DatabricksSection, DatabricksEnvironment


DEFAULT_CPU_IMAGE = DEFAULT_CPU_IMAGE
DEFAULT_GPU_IMAGE = DEFAULT_GPU_IMAGE

MPI_CPU_IMAGE = DEFAULT_CPU_IMAGE
MPI_GPU_IMAGE = DEFAULT_GPU_IMAGE

LOCAL_RUNCONFIG_NAME = "local"

SUPPORTED_DATAREF_MODES = ["mount", "download", "upload"]

SUPPORTED_DELIVERY_MECHANISM = ["direct", "mount", "download", "upload"]

module_logger = logging.getLogger(__name__)


class ContainerRegistry(Cr):
    """Represents configuration information for Container Registry.

    ContainerRegistry will be deprecated. Use the
    :class:`azureml.core.container_registry.ContainerRegistry` class.
    """

    def __init__(self):
        """Class ContainerRegistry constructor."""
        super(ContainerRegistry, self).__init__()
        module_logger.warning("'ContainerRegistry' will be deprecated soon. Please use ContainerRegistry from 'azureml.core.container_registry'.")


class AzureContainerRegistry(ContainerRegistry):
    """Represents configuration information for Azure Container Registry.

    AzureContainerRegistry will be deprecated. Use the
    :class:`azureml.core.container_registry.ContainerRegistry` class.
    """

    def __init__(self):
        """Class AzureContainerRegistry constructor."""
        super(AzureContainerRegistry, self).__init__()
        module_logger.warning("'AzureContainerRegistry' will be deprecated soon. Please use 'ContainerRegistry'.")


class HdiConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for experiments that target HDInsightCompute.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    You can specify the field `yarn_deploy_mode` with the value of either 'cluster' or 'client'.
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("yarn_deploy_mode", _FieldInfo(str, "Yarn deploy mode. Options are cluster and client."))
    ])

    def __init__(self):
        """Class HdiConfiguration constructor."""
        super(HdiConfiguration, self).__init__()
        self.yarn_deploy_mode = "cluster"
        self._initialized = True


class TensorflowConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for experiments using Tensorflow.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param worker_count: The number of worker tasks.
    :type worker_count: int
    :param parameter_server_count: The number of parameter server tasks.
    :type parameter_server_count: int
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("worker_count", _FieldInfo(int, "The number of worker tasks.")),
        ("parameter_server_count", _FieldInfo(int, "The number of parameter server tasks."))
    ])

    def __init__(self):
        """Class TensorflowConfiguration constructor."""
        super(TensorflowConfiguration, self).__init__()
        self.worker_count = 1
        self.parameter_server_count = 1
        self._initialized = True


class MpiConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for distributed MPI jobs.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param process_count_per_node: When using MPI, this parameters is number of processes per node.
    :type process_count_per_node: int
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("process_count_per_node", _FieldInfo(int, "When using MPI, number of processes per node."))
    ])

    def __init__(self):
        """Class MpiConfiguration constructor."""
        super(MpiConfiguration, self).__init__()
        self.process_count_per_node = 1
        self._initialized = True


class ParallelTaskConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for distributed ParallelTask jobs.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param max_retries_per_worker: Maximum number of retries per process ("worker"). Default is 0.
    :type max_retries_per_worker: int

    :param worker_count_per_node: The number of workers per node. Default is 1.
    :type worker_count_per_node: int

    :param terminal_exit_codes: Worker exit codes to terminate job. Will not retry worker with exit code and fails job.
    :type terminal_exit_codes: builtin.list[int]
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("max_retries_per_worker", _FieldInfo(int, "Maximum number of retries per worker. Default 0.")),
        ("worker_count_per_node", _FieldInfo(int, "The number of workers/processes per node. Default 1.")),
        ("terminal_exit_codes", _FieldInfo(list, "Worker exit codes to terminate job."))
    ])

    def __init__(self):
        """Class ParallelTaskConfiguration constructor."""
        super(ParallelTaskConfiguration, self).__init__()
        self.max_retries_per_worker = 0
        self.worker_count_per_node = 1
        self.terminal_exit_codes = None



class AmlComputeConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for experiments that target AmlCompute.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param vm_size: The VM size of the cluster to be created. Supported values: Any
        `Azure VM size <https://docs.microsoft.com/azure/cloud-services/cloud-services-sizes-specs>`_.
    :type vm_size: str

    :param vm_priority: The VM priority of the cluster to be created.
        Allowed values are 'dedicated' and 'lowpriority'.
    :type vm_priority: str
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("vm_size", _FieldInfo(str, "VM size of the Cluster to be created.Allowed values are Azure vm sizes."
                                    "The list of vm sizes is available in '"
                                    "https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs")
         ),
        ("vm_priority", _FieldInfo(str, "VM priority of the Cluster to be created. Allowed values are:"
                                        "\"dedicated\" , \"lowpriority\".")),
        ("_retain_cluster", _FieldInfo(bool, "A bool that indicates if the cluster has to be retained "
                                             "after job completion.", serialized_name="retain_cluster")),
        ("_name", _FieldInfo(str, "Name of the cluster to be created. If not specified, runId will be "
                                  "used as cluster name.", serialized_name="name")),
        ("_cluster_max_node_count", _FieldInfo(int, "Maximum number of nodes in the AmlCompute cluster to be created. "
                                                    "Minimum number of nodes will always be set to 0.",
                                               serialized_name="cluster_max_node_count"))
    ])

    def __init__(self):
        """Class AmlComputeConfiguration constructor."""
        super(AmlComputeConfiguration, self).__init__()
        self.vm_size = None
        self.vm_priority = None
        self._retain_cluster = False
        self._name = None
        self._cluster_max_node_count = None
        self._initialized = True


class EnvironmentDefinition(Environment):
    """DEPRECATED. Use the :class:`azureml.core.Environment` object."""

    def __init__(self, name=None):
        """Class EnvironmentDefinition constructor."""
        super(EnvironmentDefinition, self).__init__(name)


class SparkConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for experiment runs that target Apache Spark.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param configuration: The Spark configuration.
    :type configuration: dict
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        # In dict, values are assumed to be str
        ("configuration", _FieldInfo(dict, "The Spark configuration.")),
        ])

    def __init__(self):
        """Class SparkConfiguration constructor."""
        super(SparkConfiguration, self).__init__()
        self.configuration = {
            "spark.app.name": "Azure ML Experiment",
            "spark.yarn.maxAppAttempts": 1}
        self._initialized = True


class _AmbientAuthenticationConfiguration(_AbstractRunConfigElement):
    """Represents configuration information for ambient authentication in runs.

    This class is used in the :class:`azureml.core.runconfig.HistoryConfiguration` class.

    :param method: Method used for default authentication in the run. Supported values: none (default), armtoken,
        runtoken, serviceprincipal.
    :type method: str

    :param app_id: Application ID for service principal authentication.
    :type app_id: str

    :param secret: Name of a secret in the workspace key vault. For service principal authentication, the secret value
        is the password. For ARM token authentication, the secret value is the token itself.
    :type secret: str

    :param tenant: Tenant ID for service principal authentication.
    :type tenant: str

    :param delete_secret_after_run: Delete the secret from the key vault after the run completes. This helps keep the
        vault clean of transient secrets. Default: False.
    :type delete_secret_after_run: bool
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("method", _FieldInfo(str, "Method used for default authentication in the run. Supported values: aadtoken, "
                                   "runtoken, serviceprincipal.")),
        ("app_id", _FieldInfo(str, "Application ID for service principal authentication.")),
        ("secret", _FieldInfo(str, "Name of a secret in the workspace key vault. For service principal "
                                   "authentication, the secret value is the password. For ARM token authentication, "
                                   "the secret value is the token itself.")),
        ("tenant", _FieldInfo(str, "Tenant ID for service principal authentication.")),
        ("delete_secret_after_run", _FieldInfo(bool, "Delete the secret from the key vault after the run completes. "
                                                     "This helps keep the vault clean of transient secrets. Default: "
                                                     "False."))
        ])

    def __init__(self):
        """Class _AmbientAuthenticationConfiguration constructor."""
        super(_AmbientAuthenticationConfiguration, self).__init__()
        self.method = None
        self.app_id = None
        self.secret = None
        self.tenant = None
        self.delete_secret_after_run = False
        self._initialized = True

    def _validate(self):
        if self.method is None:
            if self.app_id or self.secret or self.tenant or self.delete_secret_after_run:
                raise UserErrorException("Do not provide ambient authentication parameters without a method.")
        else:
            self.method = str(self.method).lower()

            if self.method == "aadtoken":
                if not self.secret:
                    raise UserErrorException("AAD token authentication requires the secret field.")

                if self.app_id or self.tenant:
                    raise UserErrorException("Do not provide app_id or tenant for AAD token authentication.")
            elif self.method == "runtoken":
                if self.app_id or self.secret or self.tenant or self.delete_secret_after_run:
                    raise UserErrorException("Do not provide app_id, secret, tenant, or delete_secret_after_run for "
                                             "run token authentication.")
            elif self.method == "serviceprincipal":
                if not self.app_id or not self.secret or not self.tenant:
                    raise UserErrorException("Service principal authentication requires the app_id, secret, and "
                                             "tenant fields.")
            else:
                raise UserErrorException("Method {} is not supported for ambient authentication. Supported methods: "
                                         "aadtoken, runtoken, and serviceprincipal.".format(self.method))


class HistoryConfiguration(_AbstractRunConfigElement):
    """Represents configuration information to disable or enable experiment history logging features in experiments.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param output_collection: Indicates whether to enable history tracking, which allows status, logs, metrics,
        and outputs to be collected for a run.
    :type output_collection: bool

    :param snapshot_project: Indicates whether to take snapshots for history.
    :type snapshot_project: bool
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("output_collection", _FieldInfo(bool, "Enable history tracking -- this allows status, logs, metrics, and "
                                               "outputs\nto be collected for a run.")),
        ("snapshot_project", _FieldInfo(bool, "Whether to take snapshots for history.")),
        ("directories_to_watch", _FieldInfo(list, "Directories to sync with FileWatcher.", list_element_type=str)),
        ("_ambient_authentication", _FieldInfo(_AmbientAuthenticationConfiguration,
                                               "Default authentication parameters for the run.",
                                               serialized_name="ambientAuthentication", exclude_if_none=True))
        ])

    def __init__(self):
        """Class HistoryConfiguration constructor."""
        super(HistoryConfiguration, self).__init__()
        self.output_collection = True
        self.snapshot_project = True
        self.directories_to_watch = ['logs']
        self._ambient_authentication = None
        self._initialized = True


class DataReferenceConfiguration(_AbstractRunConfigElement):
    """Represents configuration-specific data sources available during a run.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param datastore_name: The name of the datastore.
    :type datastore_name: str
    :param mode: An operation on the datastore: 'mount', 'download', or 'upload'.
    :type mode: str
    :param path_on_datastore: The relative path on the datastore.
    :type path_on_datastore: str
    :param path_on_compute: The path on the compute target.
    :type path_on_compute: str
    :param overwrite: Indicates whether to overwrite existing data.
    :type overwrite: bool
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("data_store_name", _FieldInfo(str, "Name of the datastore.")),
        ("path_on_data_store", _FieldInfo(str, "Relative path on the datastore.")),
        ("mode", _FieldInfo(str, "Operation on the datastore, mount, download, upload")),
        ("overwrite", _FieldInfo(bool, "Whether to overwrite the data if existing")),
        ("path_on_compute", _FieldInfo(str, "The path on the compute target."))
    ])

    def __init__(self, datastore_name=None, mode="mount", path_on_datastore=None, path_on_compute=None,
                 overwrite=False):
        """Class DataReferenceConfiguration constructor."""
        super(DataReferenceConfiguration, self).__init__()
        self.data_store_name = datastore_name
        self.path_on_data_store = path_on_datastore
        self.path_on_compute = path_on_compute
        self.mode = mode.lower()
        self.overwrite = overwrite
        self._initialized = True

    def _validate(self):
        if not self.data_store_name:
            raise UserErrorException("Missing data store name")
        if not self.mode or (self.mode.lower() not in SUPPORTED_DATAREF_MODES):
            raise UserErrorException("mode {0} is not supported. Only mount, download allowed".format(self.mode))
        self.mode = self.mode.lower()


class DataPath(_AbstractRunConfigElement):
    """Currently not used.

    :param datastore_name: The name of the datastore.
    :type datastore_name: str
    :param relative_path: The relative path on datastore.
    :type relative_path: str
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("datastore_name", _FieldInfo(str, "Name of the datastore.")),
        ("relative_path", _FieldInfo(str, "Relative path on datastore."))
    ])

    def __init__(self, datastore_name, relative_path):
        """Class DataPath constructor."""
        super(self.__class__, self).__init__()
        self.datastore_name = datastore_name
        self.relative_path = relative_path
        self._initialized = True

    def _validate(self):
        if not self.datastore_name:
            raise UserErrorException("For a data path, the datastore_name cannot be empty.")
        if not self.path:
            raise UserErrorException("For a data path, the relative_path cannot be empty.")


class Dataset(_AbstractRunConfigElement):
    """Represents a reference to a saved or registered dataset which will be used in the run.

    In typical training scenarios you will not use this class. Instead, you will create a dataset from the
    :class:`azureml.core.Dataset` class and then pass it into a training script. For more information,
    see `Add & register
    datasets <https://docs.microsoft.com/azure/machine-learning/how-to-create-register-datasets>`_.

    :param dataset_id: The ID of a :class:`azureml.core.Dataset`.
    :type dataset_id: str
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("id", _FieldInfo(str, "Id of the dataset.")),
        ("name", _FieldInfo(str, "Name of the dataset.")),
        ("version", _FieldInfo(str, "Version of the dataset."))
    ])

    def __init__(self, dataset_id=None, dataset_name=None, dataset_version=None):
        """Initialize a Dataset object.

        :param dataset_id: The ID of a dataset.
        :type dataset_id: str
        """
        super(self.__class__, self).__init__()
        self.id = dataset_id
        self.name = dataset_name
        self.version = dataset_version
        self._initialized = True

    def _validate(self):
        if not self.id:
            if not (self.name and self.version):
                raise UserErrorException("The Dataset must be saved, which means it has an id, or it must be"
                                         "referenced by name and version.")


class DataLocation(_AbstractRunConfigElement):
    """Used in the :class:`azureml.core.runconfig.Data` class for managing the location of data to use in a run.

    :param dataset: The Dataset used for the run. Specify either a `dataset` or a `datapath`.
    :type dataset: str
    :param datapath: The DataPath used for the run. Specify either a `dataset` or a `datapath`.
    :type datapath: azureml.core.runconfig.DataPath
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("dataset", _FieldInfo(Dataset, "the Dataset used for this run.")),
        ("datapath", _FieldInfo(DataPath, "the DataPath used for this run."))
    ])

    def __init__(self, dataset=None, datapath=None):
        """Class Dataset constructor."""
        super(self.__class__, self).__init__()
        self.dataset = dataset
        self.datapath = datapath
        self._initialized = True

    def _validate(self):
        if not self.dataset and not self.datapath:
            raise UserErrorException("Either dataset or datapath should be presented.")


class Data(_AbstractRunConfigElement):
    """Represents data available during a run execution.

    This class is used in the :class:`azureml.core.runconfig.RunConfiguration` class.

    :param data_location: The location of the data.
    :type data_location: azureml.core.runconfig.DataLocation
    :param create_output_directories: Indcates whether to create new folder.
    :type create_output_directories: bool
    :param mechanism: Direct, mount, download, or upload.
    :type mechanism: str
    :param environment_variable_name: The environment variable name which points to the delivered data on the compute
        target.
    :type environment_variable_name: str
    :param path_on_compute: The target path on the compute to make the data available at.
    :type path_on_compute: str
    :param overwrite: Whether to overwrite existing data.
    :type overwrite: bool
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("data_location", _FieldInfo(DataLocation, "Data Location")),
        ("create_output_directories", _FieldInfo(bool, "Whether to create new folder.")),
        ("mechanism", _FieldInfo(str, "The mode to handle")),
        ("environment_variable_name", _FieldInfo(str, "Point where the data is download or mount or upload.")),
        ("path_on_compute", _FieldInfo(str, "relative path where the data is download or mount or upload.")),
        ("overwrite", _FieldInfo(bool, "Whether to overwrite the data if existing."))
    ])

    def __init__(self,
                 data_location=None,
                 create_output_directories=None,
                 mechanism="direct",
                 environment_variable_name=None,
                 path_on_compute=None,
                 overwrite=False):
        """Class DataSetPathRunConfiguration constructor."""
        super(self.__class__, self).__init__()
        self.data_location = data_location
        self.create_output_directories = create_output_directories
        self.mechanism = mechanism.lower()
        self.environment_variable_name = environment_variable_name
        self.path_on_compute = path_on_compute
        self.overwrite = overwrite
        self._initialized = True

    @staticmethod
    def create(data):
        """Create a DataConfiguration from a DatasetConsumptionConfig.

        :param data: the DatasetConsumptionConfig to create the DataConfiguration from.
        :type data: azureml.data.dataset_consumption_config.DatasetConsumptionConfig
        :return: the DataConfiguration representing how to deliver the data to the compute target.
        :rtype: DataConfiguration
        """
        if isinstance(data, DatasetConsumptionConfig):
            if data.dataset._consume_latest:
                dataset = Dataset(dataset_name=data.dataset.name,
                                  dataset_version='latest')
            else:
                if not data.dataset.id:
                    raise RuntimeError("Dataset can only be used in experiments where an Azure Machine Learning "
                                       "workspace is present")
                dataset = Dataset(dataset_id=data.dataset.id,
                                  dataset_name=data.dataset.name,
                                  dataset_version=data.dataset.version)
            data_location = DataLocation(dataset=dataset)
            return Data(data_location=data_location,
                        create_output_directories=False,
                        mechanism=data.mode,
                        environment_variable_name=data.name,
                        path_on_compute=data.path_on_compute,
                        overwrite=False)
        raise UserErrorException("Data must be an instance of DatasetConsumptionConfig.")


class RunConfiguration(_AbstractRunConfigElement):
    """Represents configuration for experiment runs targeting different compute targets in Azure Machine Learning.

    The RunConfiguration object encapsulates the information necessary to submit a training run in an
    experiment. Typically, you will not create a RunConfiguration object directly but get one
    from a method that returns it, such as the :class:`azureml.core.Experiment.submit` method of the
    :class:`azureml.core.Experiment` class.

    RunConfiguration is a base environment configuration that is also used in other types of
    configuration steps that depend on what kind of run you are triggering. For example, when setting
    up a :class:`azureml.pipeline.steps.python_script_step.PythonScriptStep`, you can access the
    step's RunConfiguration object and configure Conda dependencies or access the environment properties for
    the run.

    For examples of run configurations, see `Select and use a compute target to train your
    model <https://docs.microsoft.com/azure/machine-learning/how-to-set-up-training-targets>`_.

    .. remarks::

        We build machine learning systems typically to solve a specific problem. For example, we might
        be interested in finding the best model that ranks web pages that might be served as search results
        corresponding to a query. Our search for the best machine learning model may require us try out different
        algorithms, or consider different parameter settings, etc.

        In the Azure Machine Learning SDK, we use the concept of an experiment to capture the notion that
        different training runs are related by the problem that they're trying to solve. An
        :class:`azureml.core.experiment.Experiment` then acts as a logical container for these training runs,
        making it easier to track progress across training runs, compare two training runs directly, etc.

        The RunConfiguration encapsulates execution environment settings necessary to submit a training run in an
        experiment. It captures both the shared structure of training runs that are designed to solve the
        same machine learning problem, as well as the differences in the configuration parameters (e.g.,
        learning rate, loss function, etc.) that distinguish distinct training runs from each other.

        In typical training scenarios, RunConfiguration is used by creating a
        :class:`azureml.core.script_run_config.ScriptRunConfig` object that packages together a RunConfiguration
        object and an execution script for training.

        The configuration of RunConfiguration includes:

        *  Bundling the experiment source directory including the submitted script.
        *  Setting the Command line arguments for the submitted script.
        *  Configuring the path for the Python interpreter.
        *  Obtain Conda configuration for to manage the application dependencies. The job submission process
           can use the configuration to provision a temp Conda environment and launch the application within.
           The temp environments are cached and reused in subsequent runs.
        *  Optional usage of Docker and custom base images.
        *  Optional choice of submitting the experiment to multiple types of Azure compute.
        *  Advanced runtime settings for common runtimes like spark and tensorflow.

        The following example shows how to submit a training script on your local machine.

        .. code-block:: python

                from azureml.core import ScriptRunConfig, RunConfiguration, Experiment

                # create or load an experiment
                experiment = Experiment(workspace, "MyExperiment")
                # run a trial from the train.py code in your current directory
                config = ScriptRunConfig(source_directory='.', script='train.py',
                    run_config=RunConfiguration())
                run = experiment.submit(config)

    :param script: The relative path to the Python script file.
        The file path is relative to the source directory passed to :func:`azureml.core.experiment.Experiment.submit`.
    :type script: str

    :param arguments: Command line arguments for the Python script file.
    :type arguments: builtin.list[str]

    :param framework: The targeted framework used in the run.
        Supported frameworks are Python, PySpark, TensorFlow, and PyTorch.
    :type framework: str

    :param communicator: The communicator used in the run.
        The supported communicators are None, ParameterServer, OpenMpi, and IntelMpi.
        Keep in mind that OpenMpi requires a custom image with OpenMpi installed.
        Use ParameterServer or OpenMpi for AmlCompute clusters.
        Use IntelMpi for distributed training jobs.
    :type communicator: str

    :param conda_dependencies: When left at the default value of False, the system creates a Python environment,
        which includes the packages specified in ``conda_dependencies``.
        When set true, an existing Python environment can be specified with the python_interpreter setting.
    :type conda_dependencies: azureml.core.conda_dependencies.CondaDependencies

    :var environment: The environment definition. This field configures the Python environment.
        It can be configured to use an existing Python environment or configure to setup a temp environment for the
        experiment. The definition is also responsible for setting the required application dependencies.
    :vartype environment: azureml.core.Environment

    :param auto_prepare_environment: DEPRECATED. This setting is no longer used.
    :type auto_prepare_environment: bool

    :var max_run_duration_seconds: The maximum time allowed for the run. The system will attempt to automatically
        cancel the run if it took longer than this value.
    :vartype max_run_duration_seconds: int

    :var node_count: The number of nodes to use for the job.
    :vartype node_count: int

    :var history: The configuration section used to disable and enable experiment history logging features.
    :vartype history: azureml.core.runconfig.HistoryConfiguration

    :var spark: When the platform is set to PySpark,
        the Spark configuration section is used to set the default SparkConf for the submitted job.
    :vartype spark: azureml.core.runconfig.SparkConfiguration

    :var hdi: The HDI configuration section takes effect only when the target is set to an Azure HDI compute.
        The HDI Configuration is used to set the YARN deployment mode.
        The default deployment mode is cluster.
    :vartype hdi: azureml.core.runconfig.HdiConfiguration

    :var tensorflow: The configuration section used to configure distributed TensorFlow parameters.
        This parameter takes effect only when the ``framework`` is set to TensorFlow, and the
        ``communicator`` to ParameterServer. :class:`azureml.core.compute.AmlCompute` is the only
        supported compute for this configuration.
    :vartype tensorflow: azureml.core.runconfig.TensorflowConfiguration

    :var mpi: The configuration section used to configure distributed MPI job parameters.
        This parameter takes effect only when the ``framework`` is set to Python, and the
        ``communicator`` to OpenMpi or IntelMpi. :class:`azureml.core.compute.AmlCompute` is
        the only supported compute type for this configuration.
    :vartype mpi: azureml.core.runconfig.MpiConfiguration

    :var paralleltask: The configuration section used to configure distributed paralleltask job parameters.
        This parameter takes effect only when the ``framework`` is set to Python, and the
        ``communicator`` to ParallelTask. :class:`azureml.core.compute.AmlCompute` is
        the only supported compute type for this configuration.
    :vartype paralleltask: azureml.core.runconfig.ParallelTaskConfiguration

    :var data_references: All the data sources are available to the run during execution based
        on each configuration. For each item of the dictionary, the key is a name given to the
        data source and the value is a DataReferenceConfiguration.
    :vartype data_references: azureml.core.runconfig.DataReferenceConfiguration

    :var data: All the data to make available to the run during execution.
    :vartype data: azureml.core.runconfig.Data

    :var source_directory_data_store: The backing datastore for the project share.
    :vartype source_directory_data_store: str

    :var amlcompute: The details of the compute target to be created during
        experiment. The configuration only takes effect when the compute target is AmlCompute.
    :vartype amlcompute: azureml.core.runconfig.AmlComputeConfiguration
    """

    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("script", _FieldInfo(str, "The script to run.")),
        ("arguments", _FieldInfo(list, "The arguments to the script file.", list_element_type=str)),
        ("_target", _FieldInfo(str, "The name of the compute target to use for this run.", serialized_name="target")),
        ("framework", _FieldInfo(str, "Framework to execute inside. Allowed values are "
                                      "\"Python\" ,  \"PySpark\", \"CNTK\",  \"TensorFlow\", and \"PyTorch\".")),
        ("communicator", _FieldInfo(str, "Communicator for the given framework. Allowed values are "
                                         "\"None\" ,  \"ParameterServer\", \"OpenMpi\", and \"IntelMpi\".")),
        ("max_run_duration_seconds", _FieldInfo(int, "Maximum allowed duration for the run.")),
        ("node_count", _FieldInfo(int, "Number of nodes to use for running job.")),
        ("environment", _FieldInfo(EnvironmentDefinition, "Environment details.")),
        ("history", _FieldInfo(HistoryConfiguration, "History details.")),
        ("spark", _FieldInfo(SparkConfiguration, "Spark configuration details.")),
        ("hdi", _FieldInfo(HdiConfiguration, "HDI details.")),
        ("tensorflow", _FieldInfo(TensorflowConfiguration, "Tensorflow details.")),
        ("mpi", _FieldInfo(MpiConfiguration, "Mpi details.")),
        ("paralleltask", _FieldInfo(ParallelTaskConfiguration, "ParallelTask details.")),
        ("data_references", _FieldInfo(dict, "data reference configuration details",
                                       list_element_type=DataReferenceConfiguration)),
        ("data", _FieldInfo(dict, "The configuration details for data.",
                            list_element_type=Data)),
        ("source_directory_data_store", _FieldInfo(str, "Project share datastore reference.")),
        ("amlcompute", _FieldInfo(AmlComputeConfiguration, "AmlCompute details.")),
    ])

    def __init__(self, script=None, arguments=None, framework=None, communicator=None,
                 conda_dependencies=None, _history_enabled=None, _path=None, _name=None):
        """Initialize a RunConfiguration with the default settings."""
        super(RunConfiguration, self).__init__()

        # Used for saving to local file
        self._name = _name
        self._path = _path

        # Default values
        self.script = script if script else "train.py"
        self.arguments = arguments if arguments else []
        self._target = LOCAL_RUNCONFIG_NAME
        self.framework = framework if framework else "Python"
        self.communicator = communicator if communicator else "None"
        self.max_run_duration_seconds = None
        self.node_count = 1

        self.environment = EnvironmentDefinition()
        self.history = HistoryConfiguration()
        self.spark = SparkConfiguration()

        self.hdi = HdiConfiguration()
        self.tensorflow = TensorflowConfiguration()
        self.mpi = MpiConfiguration()
        self.paralleltask = ParallelTaskConfiguration()
        self.data_references = {}
        self.data = {}
        self.amlcompute = AmlComputeConfiguration()
        self.source_directory_data_store = None
        if _history_enabled:
            self.history.output_collection = _history_enabled

        conda_dependencies = conda_dependencies if conda_dependencies else CondaDependencies()
        self.environment.python.conda_dependencies = conda_dependencies
        self._initialized = True

    def __repr__(self):
        """Return the string representation of the RunConfiguration object.

        :return: String representation of the RunConfiguration object
        :rtype: str
        """
        run_config_dict = _serialize_to_dict(self)
        return json.dumps(run_config_dict, indent=4)

    @property
    def auto_prepare_environment(self):
        """Get the ``auto_prepare_environment`` parameter. This is a deprecated and unused setting."""
        module_logger.warning("'auto_prepare_environment' is deprecated and unused. It will be removed in a future release.")
        return True

    @auto_prepare_environment.setter
    def auto_prepare_environment(self, _):
        """Set the ``auto_prepare_environment`` parameter. This is a deprecated and unused setting."""
        module_logger.warning("'auto_prepare_environment' is deprecated and unused. It will be removed in a future release.")

    @property
    def target(self):
        """Get compute target where the job is scheduled for execution.

        The default target is "local" refering to the local machine. Available cloud compute targets can
        be found using the function :attr:`azureml.core.Workspace.compute_targets`.

        :return: The target name
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Set target.

        :param target:
        :type target: str
        """
        if isinstance(target, (AbstractComputeTarget, ComputeTarget)):
            self._target = target.name
        elif isinstance(target, str):
            if target == "amlcompute":
                print("""
                        DEPRECATED
                        We will be deprecating the run based creation of compute in the next release.
                        We recommend creating an actual Amlcompute cluster as a persistent compute target, 
                        and using the cluster name as the compute target in your run configuration. 
                        See example notebook here: aka.ms/amlcomputenb
                        """)
            self._target = target

    def save(self, path=None, name=None, separate_environment_yaml=False):
        """Save the RunConfiguration to a file on disk.

        A :class:`azureml.exceptions.UserErrorException` is raised when:

        * The RunConfiguration can't be saved with the name specified.
        * No ``name`` parameter was specified.
        * The ``path`` parameter is invalid.

        If ``path`` is of the format <dir_path>/<file_name>, where <dir_path> is a valid directory, then the
        RunConfiguration is saved at <dir_path>/<file_name>.

        If ``path`` points to a directory, which should be a project directory, then the RunConfiguration is saved
        at &lt;path&gt;/.azureml/&lt;name&gt; or &lt;path&gt;/aml_config/&lt;name&gt;.

        This method is useful when editing the configuration manually or when sharing the configuration with the CLI.

        :param separate_environment_yaml: Indicates whether to save the Conda environment configuration.
            If True, the Conda environment configuration is saved to a YAML file named 'environment.yml'.
        :type separate_environment_yaml: bool
        :param path: A user selected root directory for run configurations. Typically this is the Git Repository
            or the Python project root directory. The configuration is saved to a sub directory named .azureml.
        :type path: str
        :param name: [Required] The configuration file name.
        :type name: str
        :return:
        :rtype: None
        """
        if not path:
            if self._path:
                path = self._path
            else:
                path = os.getcwd()

        # True if the specified path is a project directory. False if the path specified is a file.
        project_dir_case = True
        if os.path.exists(path) and os.path.isdir(path):
            # This should be the project directory
            if name is None and self._name is None:
                raise UserErrorException("Cannot save a runconfig without a name specified")

            name = name if name else self._name
            if not name or len(name) == 0:
                raise UserErrorException("Name is required to save the runconfig")
        else:
            # A user might have specified the file location to save.
            parent_dir = os.path.dirname(path)
            if os.path.exists(parent_dir) and os.path.isdir(parent_dir):
                project_dir_case = False
            else:
                raise UserErrorException("{} argument is invalid".format(path))

        commented_map_dict = _serialize_to_dict(self, use_commented_map=True)

        # Since the Conda dependencies are being written to a separate file, don't include them inline.
        del commented_map_dict["environment"]["python"]["condaDependencies"]

        # If self.environment.python.conda_dependencies_file is none, which can be if
        # runconfig is fetched from cloud, then we default to conda_dependencies.yml
        run_config_dir_name = get_run_config_dir_name(path)
        conda_file_path = commented_map_dict["environment"]["python"]["condaDependenciesFile"]
        if conda_file_path is None:
            if project_dir_case:
                # Doesn't use os.path.join to make these files cross-platform compatible.
                conda_file_path = run_config_dir_name + "/conda_dependencies.yml"
            else:
                conda_file_path = "conda_dependencies.yml"

            commented_map_dict["environment"]["python"]["condaDependenciesFile"] = conda_file_path

        # If path is none, then cwd is used.
        self._save_with_default_comments(commented_map_dict, path, name,
                                         separate_environment_yaml=separate_environment_yaml,
                                         project_dir_case=project_dir_case)

        # After this we also save the conda dependencies to the conda dependencies file.
        if project_dir_case:
            self.environment.python.conda_dependencies.save_to_file(path, conda_file_path=conda_file_path)
        else:
            self.environment.python.conda_dependencies.save_to_file(os.path.dirname(path),
                                                                    conda_file_path=conda_file_path)

    @staticmethod
    def load(path, name=None):
        """Load a previously saved run configuration file from an on-disk file.

        If ``path`` points to a file, the RunConfiguration is loaded from that file.

        If ``path`` points to a directory, which should be a project directory, then the RunConfiguration is loaded
        from &lt;path&gt;/.azureml/&lt;name&gt; or &lt;path&gt;/aml_config/&lt;name&gt;.

        :param path: A user selected root directory for run configurations. Typically this is the Git Repository
            or the Python project root directory. For backward compatibility, the configuration will also be
            loaded from .azureml or aml_config sub directory. If the file is not in those directories, the file is
            loaded from the specified path.
        :type path: str
        :param name: The configuration file name.
        :type name: str
        :return: The run configuration object.
        :rtype: azureml.core.runconfig.RunConfiguration
        """
        if not path:
            path = os.getcwd()

        project_dir_case = True
        if os.path.isfile(path):
            full_runconfig_path = path
            project_dir_case = False
        else:
            # Project directory case.
            run_config_dir_name = get_run_config_dir_name(path) + "/"
            full_runconfig_path = os.path.join(path, run_config_dir_name + name)

        if os.path.isfile(full_runconfig_path):
            return RunConfiguration._load_from_path(full_runconfig_path=full_runconfig_path,
                                                    path=path,
                                                    name=name,
                                                    project_dir_case=project_dir_case)

        # Appending .runconfig suffix for backcompat case.
        full_runconfig_path = full_runconfig_path + RUNCONFIGURATION_EXTENSION
        if not os.path.isfile(full_runconfig_path):
            # check for file not in .azureml or aml_config directory
            full_runconfig_path = os.path.join(path, name + RUNCONFIGURATION_EXTENSION)

        if os.path.isfile(full_runconfig_path):
            # Setting name=name_with_ext, so that any subsequent save happens
            # on the name.runconfig file instead of name
            return RunConfiguration._load_from_path(full_runconfig_path=full_runconfig_path,
                                                    path=path,
                                                    name=name + RUNCONFIGURATION_EXTENSION,
                                                    project_dir_case=project_dir_case)
        else:
            raise UserErrorException("Failed to load RunConfiguration from path={} name={}".format(path, name))

    @staticmethod
    def _load_from_path(full_runconfig_path, path, name, project_dir_case):
        """Load legacy runconfig from serialized_dict and returns a RunConfiguration object.

        :param full_runconfig_path: full file path to load RunConfiguration from
        :type full_runconfig_path: str
        :param path: directory of runconfig file
        :type path: str
        :param name: The run config name.
        :type name: str
        :param project_dir_case: If the runconfig file is in a project directory
        :type project_dir_case: bool
        :return: The run configuration object.
        :rtype: RunConfiguration
        """
        with open(full_runconfig_path, "r") as run_config:
            # Loads with all the comments intact.
            commented_map_dict = ruamel.yaml.round_trip_load(run_config)
            return RunConfiguration._get_runconfig_using_dict(commented_map_dict,
                                                              path=path, name=name,
                                                              project_dir_case=project_dir_case)

    @staticmethod
    def delete(path, name):
        """Delete a run configuration file.

        Raises a :class:`azureml.exceptions.UserErrorException` if the configuration file is not found.

        :param path: A user selected root directory for run configurations. Typically this is the Git Repository
            or the Python project root directory. The configuration is deleted from a sub directory named .azureml.
        :type path: str
        :param name: The configuration file name.
        :type name: str
        :return:
        :raises: UserErrorException
        """
        file_found = False
        legacy_full_file_path = os.path.join(path, AML_CONFIG_DIR, name + RUNCONFIGURATION_EXTENSION)
        full_file_path = os.path.join(path, AZUREML_DIR, name + RUNCONFIGURATION_EXTENSION)
        if os.path.isfile(legacy_full_file_path):
            file_found = True
            os.remove(legacy_full_file_path)
        if os.path.isfile(full_file_path):
            file_found = True
            os.remove(full_file_path)

        if file_found == False:
            raise UserErrorException('Run config {} not found in {}'.format(name, os.getcwd()))

    @staticmethod
    def _check_old_config(serialized_dict):
        """Check old config serialization format.

        :param serialized_dict:
        :type serialized_dict: dict
        :return: Returns true if serialized_dict is an old config serialization.
        :rtype: bool
        """
        # We check for the new config parameters.
        # TODO: A better way to distinguish, right now we just check
        # these two keys as they occur in the new config.
        # We expect these to be present even in local, docker cases.
        if to_camel_case("environment") in serialized_dict and to_camel_case("history"):
            return False
        else:
            return True

    @staticmethod
    def _load_legacy_runconfig(path, name, commented_dict):
        """Load legacy runconfig from serialized_dict and returns a RunConfiguration object.

        :param path:
        :type path: str
        :param name: The run config name.
        :type name: str
        :param commented_dict:
        :type commented_dict: ruamel.yaml.comments.CommentedMap
        :return: The run configuration object.
        :rtype: RunConfiguration
        """
        # Old config fields
        script = None
        argument_vector = None
        conda_dependencies = None
        framework = None
        spark_dependencies_file = None
        target = None
        tracked_run = None

        # Old runconfig case is title case.
        if "ArgumentVector" in commented_dict:
            argument_vector = commented_dict["ArgumentVector"]
            if argument_vector and len(argument_vector) >= 1:
                script = argument_vector[0]
                argument_vector = argument_vector[1:]
            else:
                raise UserErrorException("ArgumentVector in runconfig cannot be empty.")

        if "Target" in commented_dict:
            target = commented_dict["Target"]

        if "Framework" in commented_dict:
            framework = commented_dict["Framework"]

        if "CondaDependenciesFile" in commented_dict:
            conda_dependencies = CondaDependencies(
                conda_dependencies_file_path=commented_dict["CondaDependenciesFile"])

        if "TrackedRun" in commented_dict:
            tracked_run = commented_dict["TrackedRun"]

        run_config_object = RunConfiguration(script=script, _history_enabled=tracked_run, _path=path, _name=name)
        run_config_object.arguments = argument_vector
        run_config_object.target = target
        run_config_object.framework = framework
        run_config_object.environment.python.conda_dependencies = conda_dependencies

        if "EnvironmentVariables" in commented_dict:
            run_config_object.environment.environment_variables = commented_dict["EnvironmentVariables"]

        if run_config_object.target:
            RunConfiguration._modify_runconfig_using_compute_config(run_config_object, path)

        if "SparkDependenciesFile" in commented_dict:
            spark_dependencies_file = commented_dict["SparkDependenciesFile"]

        if spark_dependencies_file:
            RunConfiguration._modify_runconfig_using_spark_config(spark_dependencies_file,
                                                                  run_config_object, path)

        # TODO: use_sampling not used.
        return run_config_object

    @staticmethod
    def _modify_runconfig_using_compute_config(run_config_object, path):
        """Read <run_config_object.target>.compute file and updates the required parameters in run_config_object.

        :param run_config_object:
        :type run_config_object: RunConfiguration
        :param path:
        :type path: str
        :return:
        :rtype: None
        """
        run_config_dir_path = get_run_config_dir_path(path)
        compute_target_path = os.path.join(
            run_config_dir_path,
            run_config_object.target + COMPUTECONTEXT_EXTENSION)

        if not os.path.isfile(compute_target_path):
            raise UserErrorException("Compute target = {} doesn't exist at {}".format(
                run_config_object.target, compute_target_path))

        with open(compute_target_path, "r") as compute_target_file:
            compute_target_dict = ruamel.yaml.round_trip_load(compute_target_file)
            if "baseDockerImage" in compute_target_dict:
                run_config_object.environment.docker.base_image \
                    = compute_target_dict["baseDockerImage"]

            if "pythonLocation" in compute_target_dict:
                run_config_object.environment.python.interpreter_path = compute_target_dict["pythonLocation"]

            # For user managed environment set spark cache packages to false.
            # This will bypass image build step.
            if "userManagedEnvironment" in compute_target_dict:
                run_config_object.environment.python.user_managed_dependencies \
                    = compute_target_dict["userManagedEnvironment"]
                run_config_object.environment.spark.precache_packages \
                    = not compute_target_dict["userManagedEnvironment"]

            if "type" in compute_target_dict:
                if compute_target_dict["type"] == "remotedocker" or \
                        compute_target_dict["type"] == "localdocker" or \
                        compute_target_dict["type"] == "amlcompute" or \
                        compute_target_dict["type"] == "containerinstance":
                    run_config_object.environment.docker.enabled = True

            if "sharedVolumes" in compute_target_dict:
                run_config_object.environment.docker.shared_volumes = compute_target_dict["sharedVolumes"]

            if "nvidiaDocker" in compute_target_dict:
                run_config_object.environment.docker.gpu_support = compute_target_dict["nvidiaDocker"]

            if "yarnDeployMode" in compute_target_dict:
                run_config_object.hdi.yarn_deploy_mode = compute_target_dict["yarnDeployMode"]

            if "nodeCount" in compute_target_dict:
                run_config_object.node_count = compute_target_dict["nodeCount"]

    @staticmethod
    def _modify_runconfig_using_spark_config(spark_dependencies_file, run_config_object, path,
                                             use_commented_map=False):
        """Read the spark dependencies file and updates the runconfig.

        :param spark_dependencies_file: The spark dependencies file, the path should be relative to the project
        directory.
        :type spark_dependencies_file: str
        :param run_config_object:
        :type run_config_object: RunConfiguration
        :param path:
        :type path: str
        :param use_commented_map: use_commented_map=True, uses the ruamel's CommentedMap instead of dict.
        CommentedMap gives us an ordered dict in which we also add default comments before dumping into the file.
        :type use_commented_map: bool
        :return:
        :rtype: None
        """
        if spark_dependencies_file:
            # Reading spark dependencies file.
            spark_dependencies_path = os.path.join(
                path, spark_dependencies_file)

            if not os.path.isfile(spark_dependencies_path):
                raise UserErrorException("Spark dependencies file = {} doesn't exist at {}".format(
                    spark_dependencies_file, spark_dependencies_path))

            with open(spark_dependencies_path, "r") as spark_file:
                if use_commented_map:
                    spark_file_dict = ruamel.yaml.round_trip_load(spark_file)
                else:
                    spark_file_dict = ruamel.yaml.safe_load(spark_file)

                spark_config_object = _deserialize_and_add_to_object(
                    SparkConfiguration, spark_file_dict)
                spark_environment_object = _deserialize_and_add_to_object(
                    SparkSection, spark_file_dict)
                run_config_object.spark = spark_config_object
                run_config_object.environment.spark = spark_environment_object

    def _save_with_default_comments(self, commented_map_dict, path, name, separate_environment_yaml=False,
                                    project_dir_case=True):
        """Save the RunConfiguration to the on-disk <config_name>.runconfig file with the default comments for fields.

        The save() method doesn't do this because we don't want to overwrite a user's comments in a runconfig
        file with the default comments.

        The method is useful to create runconfigs on a compute target attach. After that, we should be using save()
        method.
        This method overwrites <run_config_name>.runconfig on-disk.
        :param path: The path of the run configuration.
        :type path: str
        :param name: The name of the run configuration.
        :type name: str
        :param separate_environment_yaml: separate_environment_yaml=True saves the environment configuration in
        a separate yaml file. The environment file name will be environment.yml
        :type separate_environment_yaml: bool
        :param project_dir_case: If True, runconfigs will be saved in path/.azureml folder.
        If False, runconfigs will be saved in the file specified by path.
        :type project_dir_case: bool
        :return:
        :rtype: None
        """
        # Computing path values for both cases.
        if project_dir_case:
            run_config_dir_name = get_run_config_dir_name(path) + "/"
            full_runconfig_path = os.path.join(path, run_config_dir_name + name)
            full_env_path = os.path.join(path, run_config_dir_name + "environment.yml")
        else:
            run_config_dir_name = ""
            full_runconfig_path = path
            full_env_path = os.path.join(os.path.dirname(path), "environment.yml")

        if separate_environment_yaml:
            environment_commented_map = commented_map_dict.get("environment")
            commented_map_dict["environment"] = run_config_dir_name + "environment.yml"

            if not _check_before_comment(commented_map_dict, "environment"):
                # A hack to prevent a ruamel bug.
                # commented_map_dict.ca.items["environment"] = [None, [], None, None]
                _yaml_set_comment_before_after_key_with_error(
                    commented_map_dict, "environment", "The file path that contains the environment configuration.")

            with open(full_runconfig_path, 'w') as outfile:
                ruamel.yaml.round_trip_dump(commented_map_dict, outfile)

            with open(full_env_path, 'w') as outfile:
                ruamel.yaml.round_trip_dump(environment_commented_map, outfile)
        else:
            with open(full_runconfig_path, 'w') as outfile:
                ruamel.yaml.round_trip_dump(commented_map_dict, outfile)

    @staticmethod
    def _check_camel_case_keys(current_object, current_class):
        """Recursive function that converts all keys to camel case.

        Returns (all_camel_case, new_current_object). where all_camel_case=False means that non-camel case keys were
        found in current_object. new_current_object is a copy of current_object where all keys are in camel case.

        :param current_object:
        :type current_object: CommentedMap, list or any basic type.
        :param current_class: The current class whose serialized element we are checking.
        :type current_class: _AbstractRunConfigElement
        :return:(all_camel_case, new_current_object)
        :rtype: bool, object
        """
        all_camel_case = True
        new_class_name = None
        from ruamel.yaml.comments import CommentedMap
        if isinstance(current_object, CommentedMap) or isinstance(current_object, dict):
            if isinstance(current_object, CommentedMap):
                new_commented_map = CommentedMap()
            else:
                new_commented_map = dict()

            for (key, value) in current_object.items():
                snake_case_key = to_snake_case(to_camel_case(key))
                field_info = None

                if current_class and issubclass(current_class, _AbstractRunConfigElement):
                    field_info = RunConfiguration._get_field_info_object(current_class, snake_case_key)

                # We skip changing case for user keys
                if field_info and field_info.user_keys:
                    new_commented_map[to_camel_case(key)] = value
                else:
                    if field_info:
                        new_class_name = field_info.field_type
                        # list is a special case, where we send the list element type.
                        if isinstance(value, list):
                            new_class_name = field_info.list_element_type

                    sub_all_camel_case, new_value = RunConfiguration._check_camel_case_keys(value, new_class_name)
                    if not sub_all_camel_case or to_camel_case(key) != key:
                        all_camel_case = False

                    new_commented_map[to_camel_case(key)] = new_value
            return all_camel_case, new_commented_map
        elif isinstance(current_object, list):
            new_list = list()
            for list_item in current_object:
                sub_all_camel_case, new_list_item = RunConfiguration._check_camel_case_keys(list_item, current_class)
                if not sub_all_camel_case:
                    all_camel_case = sub_all_camel_case
                new_list.append(new_list_item)

            return all_camel_case, new_list
        else:
            # Basic types case.
            # TODO: We may want to have a deepcopy here, but doesn't look necessary.
            return all_camel_case, current_object

    @staticmethod
    def _get_field_info_object(class_type, snake_case_key):
        """Return a _FieldInfo object for a key.

        The key has to be a snake case key.

        :param class_type:
        :type class_type: object
        :param snake_case_key:
        :type snake_case_key: str
        :return:
        :rtype: _FieldInfo
        """
        if class_type and issubclass(class_type, _AbstractRunConfigElement):
            field_type_dict = class_type._field_to_info_dict
            if snake_case_key in field_type_dict:
                return field_type_dict[snake_case_key]
        return None

    @staticmethod
    def _get_run_config_object(path, run_config):
        """Return run config object.

        :param path:
        :type path: str
        :param run_config:
        :type run_config: RunConfiguration
        :return: Returns the run configuration object
        :rtype: azureml.core.runconfig.RunConfiguration
        """
        if isinstance(run_config, str):
            # If it is a string then we don't need to create a copy.
            return RunConfiguration.load(path, run_config)
        elif isinstance(run_config, RunConfiguration):
            # TODO: Deep copy of project and auth object too.
            import copy
            return copy.deepcopy(run_config)
        else:
            raise UserErrorException("Unsupported runconfig type {}. run_config can be of str or "
                                     "azureml.core.runconfig.RunConfiguration type.".format(type(run_config)))

    @classmethod
    def _get_runconfig_using_runid(cls, experiment, run_id):
        """Return a runconfig using the experiment and runconfig.

        Implementation details: fetching the runconfig from the experiment service in the cloud.

        :param experiment:
        :type experiment: azureml.core.experiment.Experiment
        :param run_id:
        :type run_id: str
        :return:
        :rtype: RunConfiguration
        """
        run = Run(experiment, run_id)
        run_details = run.get_details()
        return cls._get_runconfig_using_run_details(run_details)

    @classmethod
    def _get_runconfig_using_run_details(cls, run_details):
        """Return a runconfig using the experiment and runconfig.

        Uses the runconfig dictionary from the run details.

        :param run_details:
        :type run_details: dict
        :return:
        :rtype: RunConfiguration
        """
        if "runDefinition" in run_details:
            return cls._get_runconfig_using_dict(run_details["runDefinition"])
        else:
            raise RunConfigurationException("Run configuration not found for the given experiment and run id.")

    @classmethod
    def _get_runconfig_using_dict(cls, commented_map_or_dict, path=None, name=None,
                                  project_dir_case=True):
        """Construct the runconfig object from the serialized commented_map_or_dict.

        :param commented_map_or_dict:
        :type commented_map_or_dict: dict
        :param path:
        :type path: str
        :param name:
        :type name: str
        :param project_dir_case:
        :type project_dir_case: bool
        :return:
        :rtype:RunConfiguration
        """
        all_camel_case, new_commented_map = cls._check_camel_case_keys(commented_map_or_dict, cls)
        if not all_camel_case:
            # Replacing with the new map that has keys in camelCase
            commented_map_or_dict = new_commented_map

        if cls._check_old_config(commented_map_or_dict):
            # Old runconfig case.
            return cls._load_legacy_runconfig(path, name,
                                              commented_map_or_dict)
        else:
            # New runconfig case.
            if project_dir_case:
                dir_to_load = path
            else:
                dir_to_load = os.path.dirname(path)

            # Check if environment is specified as a dict or a file reference.
            if "environment" in commented_map_or_dict and type(commented_map_or_dict["environment"]) == str:
                # environment is specified as a file reference.
                environment_path = os.path.join(dir_to_load,
                                                commented_map_or_dict["environment"])
                with open(environment_path, "r") as environment_config:
                    # Replacing string path with the actual environment serialized dictionary.
                    commented_map_or_dict["environment"] = ruamel.yaml.round_trip_load(environment_config)

            run_config_object = cls(_path=path, _name=name)

            # Only wants to preserve the comments if it is a commented map.
            if type(commented_map_or_dict) == ruamel.yaml.comments.CommentedMap:
                run_config_object._loaded_commented_map = commented_map_or_dict

            _deserialize_and_add_to_object(
                cls, commented_map_or_dict, object_to_populate=run_config_object)

            # Loading the conda file as conda object and setting that in the runconfig.
            # this method gets invoked when trying to load the run config from a file on disk
            # the conda dependencies file should already be populated to the correct value
            # Default to use the new .azureml path
            if hasattr(run_config_object.environment, "python"):
                if run_config_object.environment.python.conda_dependencies_file is not None:
                    conda_dependencies = CondaDependencies(
                        os.path.join(dir_to_load, run_config_object.environment.python.conda_dependencies_file))
                    run_config_object.environment.python.conda_dependencies = conda_dependencies

            return run_config_object
