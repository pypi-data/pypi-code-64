# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains the abstract base class for datasets in Azure Machine Learning."""

import collections
import re
import json
import pprint
from abc import ABCMeta
from copy import deepcopy

from azureml.data.dataset_factory import TabularDatasetFactory, FileDatasetFactory
from azureml.data.constants import _TELEMETRY_ENTRY_POINT_DATASET
from azureml.data._dataprep_helper import dataprep, is_dataprep_installed, get_dataprep_missing_message
from azureml.data._dataset_rest_helper import _dto_to_dataset, _dataset_to_dto, _dataset_to_saved_dataset_dto, \
    _saved_dataset_dto_to_dataset, _restclient, _dto_to_registration, _custom_headers, _make_request
from azureml.data._loggerfactory import track, _LoggerFactory
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.exceptions import UserErrorException


_PUBLIC_API = 'PublicApi'
_logger = None
_dataprep_missing_for_repr_warned = False


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class AbstractDataset(object):
    """Base class of datasets in Azure Machine Learning.

    Please reference :class:`azureml.data.dataset_factory.TabularDatasetFactory` class and
    :class:`azureml.data.dataset_factory.FileDatasetFactory` class to create instances of dataset.
    """

    __metaclass__ = ABCMeta

    Tabular = TabularDatasetFactory
    File = FileDatasetFactory

    def __init__(self):
        """Class AbstractDataset constructor.

        This constructor is not supposed to be invoked directly. Dataset is intended to be created using
        :class:`azureml.data.dataset_factory.TabularDatasetFactory` class and
        :class:`azureml.data.dataset_factory.FileDatasetFactory` class.
        """
        if self.__class__ == AbstractDataset:
            raise UserErrorException('Cannot create instance of abstract class AbstractDataset')
        self._definition = None
        self._properties = None
        self._registration = None
        self._telemetry_info = None

        # Execution/Pipelines services enable this flag so the latest version of the Dataset is used on the data plane
        self._consume_latest = False

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API)
    def get_by_name(workspace, name, version='latest'):
        """Get a registered Dataset from workspace by its registration name.

        :param workspace: The existing AzureML workspace in which the Dataset was registered.
        :type workspace: azureml.core.Workspace
        :param name: The registration name.
        :type name: str
        :param version: The registration version. Defaults to 'latest'.
        :type version: int
        :return: The registered dataset object.
        :rtype: azureml.data.TabularDataset or azureml.data.FileDataset
        """
        dataset = AbstractDataset._get_by_name(workspace, name, version)
        AbstractDataset._track_lineage([dataset])
        return dataset

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API)
    def get_by_id(workspace, id):
        """Get a Dataset which is saved to the workspace.

        :param workspace: The existing AzureML workspace in which the Dataset is saved.
        :type workspace: azureml.core.Workspace
        :param id: The id of dataset.
        :type id: str
        :return: The dataset object.
            If dataset is registered, its registration name and version will also be returned.
        :rtype: azureml.data.TabularDataset or azureml.data.FileDataset
        """
        dataset = AbstractDataset._get_by_id(workspace, id)
        AbstractDataset._track_lineage([dataset])
        return dataset

    @staticmethod
    @track(_get_logger, activity_type=_PUBLIC_API)
    def get_all(workspace):
        """Get all the registered datasets in the workspace.

        :param workspace: The existing AzureML workspace in which the Datasets were registered.
        :type workspace: azureml.core.Workspace
        :return: A dictionary of TabularDataset and FileDataset objects keyed by their registration name.
        :rtype: dict[str, azureml.data.TabularDataset or azureml.data.FileDataset]
        """
        def list_dataset(continuation_token):
            return _restclient(workspace).dataset.list(
                subscription_id=workspace.subscription_id,
                resource_group_name=workspace.resource_group,
                workspace_name=workspace.name,
                page_size=100,
                include_latest_definition=True,
                include_invisible=False,
                continuation_token=continuation_token,
                custom_headers=_custom_headers)

        def get_dataset(name):
            try:
                return AbstractDataset.get_by_name(workspace, name)
            except Exception:
                return None

        return _DatasetDict(workspace=workspace, list_fn=list_dataset, get_fn=get_dataset)

    @property
    @track(_get_logger, activity_type=_PUBLIC_API)
    def id(self):
        """Return the identifier of the dataset.

        :return: Dataset id. If the dataset is not saved to any workspace, the id will be None.
        :rtype: str
        """
        if self._registration:
            if self._registration.saved_id:
                return self._registration.saved_id
            if self._registration.workspace:
                self._ensure_saved(self._registration.workspace)
                return self._registration.saved_id
        return None

    @property
    @track(_get_logger, activity_type=_PUBLIC_API)
    def name(self):
        """Return the registration name.

        :return: Dataset name.
        :rtype: str
        """
        return None if self._registration is None else self._registration.name

    @property
    @track(_get_logger, activity_type=_PUBLIC_API)
    def version(self):
        """Return the registration version.

        :return: Dataset version.
        :rtype: int
        """
        return None if self._registration is None else self._registration.version

    @property
    @track(_get_logger, activity_type=_PUBLIC_API)
    def description(self):
        """Return the registration description.

        :return: Dataset description.
        :rtype: str
        """
        return None if self._registration is None else self._registration.description

    @property
    @track(_get_logger, activity_type=_PUBLIC_API)
    def tags(self):
        """Return the registration tags.

        :return: Dataset tags.
        :rtype: str
        """
        return None if self._registration is None else self._registration.tags

    @property
    @track(_get_logger, activity_type=_PUBLIC_API)
    def data_changed_time(self):
        """Return the source data changed time.

        .. remarks::

            Data changed time is available for file-based data source. None will be returned when the data source is
            not supported for checking when change has happened.

        :return: The time when the most recent change happened to source data.
        :rtype: datetime.datetime
        """
        _, changed_time = self._dataflow._get_source_data_hash()
        return changed_time

    @property
    @track(_get_logger)
    def _dataflow(self):
        if self._definition is None:
            raise UserErrorException('Dataset definition is missing. Please check how the dataset is created.')
        if self._registration and self._registration.workspace:
            dataprep().api._datastore_helper._set_auth_type(self._registration.workspace)
        if not isinstance(self._definition, dataprep().Dataflow):
            try:
                self._definition = dataprep().Dataflow.from_json(self._definition)
            except Exception as e:
                msg = 'Failed to load dataset definition with azureml-dataprep=={}'.format(dataprep().__version__)
                _get_logger().error('{}. Exception: {}'.format(msg, e))
                raise UserErrorException('{}. Please install the latest version with "pip install -U '
                                         'azureml-dataprep".'.format(msg))
        return self._definition

    @track(_get_logger, activity_type=_PUBLIC_API)
    def as_named_input(self, name):
        """Provide a name for this dataset which will be used to retrieve the materialized dataset in the run.

        .. remarks::

            The name here will only be applicable inside an Azure Machine Learning run. The name must only contain
            alphanumeric and underscore characters so it can be made available as an environment variable. You can use
            this name to retrieve the dataset in the context of a run using two approaches:

            #. Environment Variable:
                The name will be the environment variable name and the materialized dataset will
                be made available as the value of the environment variable. If the dataset is downloaded or mounted,
                the value will be the downloaded/mounted path. For example:

                .. code-block:: python

                    # in your job submission notebook/script:
                    dataset.as_named_input('foo').as_download('/tmp/dataset')

                    # in the script that will be executed in the run
                    import os
                    path = os.environ['foo'] # path will be /tmp/dataset

                If the dataset is set to direct mode, then the value will be the dataset ID. You can then
                retrieve the dataset object by doing `Dataset.get_by_id(os.environ['foo'])`

            #. Run.input_datasets:
                This is a dictionary where the key will be the dataset name you specified in this
                method and the value will be the materialized dataset. For downloaded and mounted dataset, the value
                will be the downloaded/mounted path. For direct mode, the value will be the same dataset object you
                specified in your job submission script.

                .. code-block:: python

                    # in your job submission notebook/script:
                    dataset.as_named_input('foo') # direct mode

                    # in the script that will be executed in the run
                    run = Run.get_context()
                    run.input_datasets['foo'] # this returns the dataset object from above.


        :param name: The name of the dataset for the run.
        :type name: str
        :return: The configuration object describing how the Dataset should be materialized in the run.
        :rtype: azureml.data.dataset_consumption_config.DatasetConsumptionConfig
        """
        return DatasetConsumptionConfig(name, self)

    @track(_get_logger, activity_type=_PUBLIC_API)
    def register(self, workspace, name, description=None, tags=None, create_new_version=False):
        """Register the dataset to the provided workspace.

        :param workspace: The workspace to register the dataset.
        :type workspace: azureml.core.Workspace
        :param name: The name to register the dataset with.
        :type name: str
        :param description: A text description of the dataset. Defaults to None.
        :type description: str
        :param tags: Dictionary of key value tags to give the dataset. Defaults to None.
        :type tags: dict[str, str]
        :param create_new_version: Boolean to register the dataset as a new version under the specified name.
        :type create_new_version: bool
        :return: The registered dataset object.
        :rtype: azureml.data.TabularDataset or azureml.data.FileDataset
        """
        def request():
            return _restclient(workspace).dataset.register(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                dataset_dto=_dataset_to_dto(self, name, description, tags),
                if_exists_ok=create_new_version,
                update_definition_if_exists=create_new_version,
                custom_headers=self._get_telemetry_headers())

        def handle_error(error):
            status_code = error.response.status_code
            if status_code == 409:
                return UserErrorException((
                    'There is already a dataset registered under name "{}". '
                    'Specify `create_new_version=True` to register the dataset as a new version. '
                    'Use `update`, `add_tags`, or `remove_tags` to change only the description or tags.'
                ).format(name))
            if status_code == 400:
                regex = re.compile(
                    r'has been registered as (.+):([0-9]+) \(name:version\).',
                    re.IGNORECASE)
                matches = regex.findall(error.message)
                if len(matches) == 1:
                    existing_name, existing_version = matches[0]
                    return UserErrorException((
                        'An identical dataset had already been registered, which can '
                        'be retrieved with `Dataset.get_by_name(workspace, name="{}", version={})`.'
                    ).format(existing_name, existing_version))

        success, result = _make_request(request, handle_error)
        if not success:
            raise result
        dataset = _dto_to_dataset(workspace, result)
        self.__class__._track_output_reference_lineage(dataset)
        return dataset

    @track(_get_logger, activity_type=_PUBLIC_API)
    def update(self, description=None, tags=None):
        """Perform an in-place update of the dataset.

        :param description: The new description to use for the dataset. This description replaces the existing
            description. Defaults to existing description. To clear description, enter empty string.
        :type description: str
        :param tags: A dictionary of tags to update the dataset with. These tags replace existing tags for the
            dataset. Defaults to existing tags. To clear tags, enter empty dictionary.
        :type tags: dict[str, str]
        :return: The updated dataset object.
        :rtype: azureml.data.TabularDataset or azureml.data.FileDataset
        """
        if not self._registration or not self._registration.workspace or not self._registration.registered_id:
            return UserErrorException('To update this dataset it must be registered.')
        workspace = self._registration.workspace

        def request():
            updated_description = description
            updated_tags = tags
            if description is None:
                updated_description = self._registration.description
            if tags is None:
                updated_tags = self._registration.tags

            return _restclient(workspace).dataset.update_dataset(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                dataset_id=self._registration.registered_id,
                new_dataset_dto=_dataset_to_dto(
                    self,
                    self.name,
                    updated_description,
                    updated_tags,
                    self._registration.registered_id),
                custom_headers=self._get_telemetry_headers())

        success, result = _make_request(request)
        if not success:
            raise result
        result_dto = _dto_to_dataset(workspace, result)
        self._registration.tags = result_dto.tags
        self._registration.description = result_dto.description
        return result_dto

    @track(_get_logger, activity_type=_PUBLIC_API)
    def add_tags(self, tags=None):
        """Add key value pairs to the tags dictionary of this dataset.

        :param tags: The dictionary of tags to add.
        :type tags: dict[str, str]
        :return: The updated dataset object.
        :rtype: azureml.data.TabularDataset or azureml.data.FileDataset
        """
        if not self._registration or not self._registration.workspace or not self._registration.registered_id:
            return UserErrorException('To add tags to this dataset it must be registered.')
        workspace = self._registration.workspace

        def request():
            duplicate_keys = []
            for item in set(tags).intersection(self._registration.tags):
                if self._registration.tags[item] != tags[item]:
                    duplicate_keys.append(item)
            if len(duplicate_keys) > 0:
                raise UserErrorException((
                    'Dataset already contains different values for tags '
                    'with the following keys {}'
                ).format(duplicate_keys))

            updatedTags = deepcopy(self._registration.tags)
            updatedTags.update(tags)

            return _restclient(workspace).dataset.update_dataset(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                dataset_id=self._registration.registered_id,
                new_dataset_dto=_dataset_to_dto(
                    self,
                    self.name,
                    self.description,
                    updatedTags,
                    self._registration.registered_id),
                custom_headers=self._get_telemetry_headers())

        success, result = _make_request(request)
        if not success:
            raise result
        result_dto = _dto_to_dataset(workspace, result)
        self._registration.tags = result_dto.tags
        return result_dto

    @track(_get_logger, activity_type=_PUBLIC_API)
    def remove_tags(self, tags=None):
        """Remove the specified keys from tags dictionary of this dataset.

        :param tags: The list of keys to remove.
        :type tags: List[str]
        :return: The updated dataset object.
        :rtype: azureml.data.TabularDataset or azureml.data.FileDataset
        """
        if not self._registration or not self._registration.workspace or not self._registration.registered_id:
            return UserErrorException('To remove tags from this dataset it must be registered.')
        workspace = self._registration.workspace

        def request():
            updatedTags = deepcopy(self._registration.tags)
            for item in set(tags).intersection(updatedTags):
                del updatedTags[item]

            return _restclient(workspace).dataset.update_dataset(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                dataset_id=self._registration.registered_id,
                new_dataset_dto=_dataset_to_dto(
                    self,
                    self.name,
                    self.description,
                    updatedTags,
                    self._registration.registered_id),
                custom_headers=self._get_telemetry_headers())

        success, result = _make_request(request)
        if not success:
            raise result
        result_dto = _dto_to_dataset(workspace, result)
        self._registration.tags = result_dto.tags
        return result_dto

    @track(_get_logger, activity_type=_PUBLIC_API)
    def unregister_all_versions(self):
        """Unregister all versions under the registration name of this dataset from the workspace.

        .. remarks::

            The operation does not change any source data.
        """
        if not self._registration or not self._registration.workspace or not self._registration.registered_id:
            return  # no-op if dataset is not registered
        workspace = self._registration.workspace

        def request():
            return _restclient(workspace).dataset.unregister_dataset(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                self.name,
                custom_headers=_custom_headers)

        success, result = _make_request(request)
        if not success:
            raise result
        self._registration = None

    @classmethod
    @track(_get_logger)
    def _create(cls, definition, properties=None, registration=None, telemetry_info=None):
        if registration is not None and not isinstance(registration, _DatasetRegistration):
            raise UserErrorException('registration must be instance of `_DatasetRegistration`')
        if telemetry_info is not None and not isinstance(telemetry_info, _DatasetTelemetryInfo):
            raise UserErrorException('telemetry_info must be instance of `_DatasetTelemetryInfo`')
        dataset = cls()
        dataset._definition = definition  # definition is either str or Dataflow which is immutable
        dataset._properties = deepcopy(properties) if properties else {}
        dataset._registration = registration
        dataset._telemetry_info = telemetry_info
        return dataset

    @track(_get_logger)
    def _ensure_saved(self, workspace):
        saved_id = self._ensure_saved_internal(workspace)
        self.__class__._track_output_reference_lineage(self)
        return saved_id

    def _get_telemetry_headers(self):
        telemetry_entry_point = _TELEMETRY_ENTRY_POINT_DATASET
        if self._telemetry_info and self._telemetry_info.entry_point:
            telemetry_entry_point = self._telemetry_info.entry_point
        headers = {'x-ms-azureml-dataset-entry-point': telemetry_entry_point}
        headers.update(_custom_headers)
        return headers

    @staticmethod
    def _track_lineage(datasets):
        from azureml.core import Run

        try:
            run = Run.get_context()
            run._update_dataset_lineage(datasets)
        except AttributeError:
            pass
        except Exception:
            _get_logger().error('Failed to update dataset lineage')

    @staticmethod
    def _track_output_reference_lineage(dataset):
        from azureml._restclient.models import OutputDatasetLineage, DatasetIdentifier, DatasetOutputType
        from azureml.core import Run

        if not dataset._registration:
            return

        id = dataset.id
        registered_id = dataset._registration and dataset._registration.registered_id
        version = dataset.version
        dataset_id = DatasetIdentifier(id, registered_id, version)
        output_lineage = OutputDatasetLineage(dataset_id, DatasetOutputType.reference)

        try:
            run = Run.get_context()
            run._update_output_dataset_lineage([output_lineage])
        except AttributeError:
            pass
        except Exception as e:
            _get_logger().warning('Failed to update output dataset lineage due to {}.'.format(type(e).__name__))

    @staticmethod
    def _get_by_name(workspace, name, version):
        if version != 'latest':
            try:
                version = int(version)
            except ValueError:
                raise UserErrorException('Invalid value {} for version. Version value must be number or "latest".'
                                         .format(version))
        else:
            version = None

        def request():
            dto = _restclient(workspace).dataset.get_dataset_by_name(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                dataset_name=name,
                version_id=version,
                custom_headers=_custom_headers)

            return dto

        def handle_error(error):
            if error.response.status_code == 404:
                return UserErrorException(
                    'Cannot find dataset registered with name "{}"{} in the workspace.'
                    .format(name, '' if version == 'latest' else ' (version: {})'.format(version)))

        success, result = _make_request(request, handle_error)
        if not success:
            raise result
        return _dto_to_dataset(workspace, result)

    @staticmethod
    def _get_by_id(workspace, id):
        def request_for_registered():
            return _restclient(workspace).dataset.get_datasets_by_saved_dataset_id(
                subscription_id=workspace.subscription_id,
                resource_group_name=workspace.resource_group,
                workspace_name=workspace.name,
                saved_dataset_id=id,
                page_size=1,  # just need the 1st (can only be more than one for dataset created in the old age)
                custom_headers=_custom_headers)

        success, result = _make_request(request_for_registered)
        if success and len(result.value) == 1:
            return _dto_to_dataset(workspace, result.value[0])

        def request_for_unregistered():
            return _restclient(workspace).dataset.get_by_id(
                subscription_id=workspace.subscription_id,
                resource_group_name=workspace.resource_group,
                workspace_name=workspace.name,
                id=id,
                resolve_legacy_id=True,
                custom_headers=_custom_headers)

        def handle_error(error):
            if error.response.status_code == 404:
                return UserErrorException(
                    'Cannot find dataset with id "{}" in the workspace.'
                    .format(id))

        success, result = _make_request(request_for_unregistered, handle_error)
        if not success:
            raise result
        return _saved_dataset_dto_to_dataset(workspace, result)

    def _register(self, workspace, name, description=None, tags=None, create_new_version=False):
        def request():
            return _restclient(workspace).dataset.register(
                workspace.subscription_id,
                workspace.resource_group,
                workspace.name,
                dataset_dto=_dataset_to_dto(self, name, description, tags),
                if_exists_ok=create_new_version,
                update_definition_if_exists=create_new_version,
                custom_headers=self._get_telemetry_headers())

        def handle_error(error):
            status_code = error.response.status_code
            if status_code == 409:
                return Exception((
                    'There is already a dataset registered under name "{}". ' +
                    'Specify `create_new_version=True` to register the dataset as a new version.'
                ).format(name))
            if status_code == 400:
                regex = re.compile(
                    r'has been registered as (.+):([0-9]+) \(name:version\).',
                    re.IGNORECASE)
                matches = regex.findall(error.message)
                if len(matches) == 1:
                    existing_name, existing_version = matches[0]
                    return Exception((
                        'An identical dataset had already been registered, which can ' +
                        'be retrieved with `Dataset.get_by_name(workspace, name="{}", version={})`.'
                    ).format(existing_name, existing_version))

        success, result = _make_request(request, handle_error)
        if not success:
            raise result
        return _dto_to_dataset(workspace, result)

    def _ensure_saved_internal(self, workspace):
        if not self._registration or not self._registration.saved_id:
            # only call service when dataset is not saved yet
            def request():
                return _restclient(workspace).dataset.ensure_saved(
                    subscription_id=workspace.subscription_id,
                    resource_group_name=workspace.resource_group,
                    workspace_name=workspace.name,
                    dataset=_dataset_to_saved_dataset_dto(self),
                    custom_headers=self._get_telemetry_headers())

            success, result = _make_request(request)
            if not success:
                raise result
            saved_dataset = _saved_dataset_dto_to_dataset(workspace, result)

            # modify _definition using service response
            self._definition = saved_dataset._definition

            # modify self._registration.saved_id using service response
            if self._registration:
                self._registration.saved_id = saved_dataset._registration.saved_id
            else:
                self._registration = saved_dataset._registration

        return self._registration.saved_id

    @track(_get_logger, activity_type=_PUBLIC_API)
    def __str__(self):
        """Format the dataset object into a string.

        :return: Return string representation of the dataset object
        :rtype: str
        """
        return '{}\n{}'.format(type(self).__name__, self.__repr__())

    @track(_get_logger, activity_type=_PUBLIC_API)
    def __repr__(self):
        """Format the dataset object into a string.

        :return: Return string representation of the the dataset object
        :rtype: str
        """
        content = collections.OrderedDict()
        if is_dataprep_installed():
            steps = self._dataflow._get_steps()
            step_type_pattern = re.compile(r'Microsoft.DPrep.(.*)Block', re.IGNORECASE)
            step_type = steps[0].step_type
            step_arguments = steps[0].arguments

            if hasattr(step_arguments, 'to_pod'):
                step_arguments = step_arguments.to_pod()
            if step_type == 'Microsoft.DPrep.GetDatastoreFilesBlock':
                source = [
                    '(\'{}\', \'{}\')'.format(store['datastoreName'], store['path'])
                    for store in step_arguments['datastores']
                ]
            elif step_type == 'Microsoft.DPrep.GetFilesBlock':
                source = [details['path'] for details in step_arguments['path']['resourceDetails']]
            else:
                source = None

            encoder = dataprep().api.engineapi.typedefinitions.CustomEncoder \
                if hasattr(dataprep().api.engineapi.typedefinitions, 'CustomEncoder') \
                else dataprep().api.engineapi.engine.CustomEncoder
            content['source'] = source
            content['definition'] = [
                step_type_pattern.search(s.step_type).group(1) for s in steps
            ]
        else:
            encoder = None
            global _dataprep_missing_for_repr_warned
            if not _dataprep_missing_for_repr_warned:
                _dataprep_missing_for_repr_warned = True
                import logging
                logging.getLogger().warning(get_dataprep_missing_message(
                    'Warning: Cannot load "definition" and "source" for the dataset'))

        if self._registration is not None:
            content['registration'] = collections.OrderedDict([
                ('id', self.id),
                ('name', self.name),
                ('version', self.version)
            ])

            if self.description:
                content['registration']['description'] = self.description
            if self.tags:
                content['registration']['tags'] = self.tags
            content['registration']['workspace'] = self._registration.workspace.__repr__()

        return json.dumps(content, indent=2, cls=encoder)


class _DatasetRegistration(object):
    def __init__(self, workspace, saved_id, registered_id=None, name=None, version=None, description=None, tags=None):
        # Deep copy has been overridden, if you add any new members, please make sure you update the deepcopy method
        # accordingly
        self.workspace = workspace  # this member will not be deep copied
        self.saved_id = saved_id
        self.registered_id = registered_id
        self.name = name
        self.version = version
        self.description = description
        self.tags = tags

    def __repr__(self):
        return "DatasetRegistration(id='{}', name='{}', version={}, description='{}', tags={})".format(
            self.saved_id, self.name, self.version, self.description or '', self.tags)

    def __deepcopy__(self, memodict={}):
        from copy import deepcopy

        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            if k == 'workspace':
                # we don't deepcopy workspace because some Authentication classes has locks which cannot be deep
                # copied
                continue
            setattr(result, k, deepcopy(v))
        return result


class _DatasetTelemetryInfo(object):
    def __init__(self, entry_point):
        self.entry_point = entry_point


_Mapping = collections.abc.Mapping if hasattr(collections, 'abc') else collections.Mapping


class _DatasetDict(_Mapping):
    def __init__(self, workspace, list_fn, get_fn):
        self._workspace = workspace
        self._list_fn = list_fn
        self._get_fn = get_fn
        self._all_listed = False
        self._list_continuation_token = None
        self._list_cached = {}
        self._getitem_cached = {}

    @property
    def registrations(self):
        self._list_all()
        return list(self._list_cached.values())

    def __getitem__(self, key):
        if key in self._getitem_cached:
            return self._getitem_cached[key]
        result = self._get_fn(name=key)
        if result is None:
            raise KeyError(key)
        self._getitem_cached[key] = result
        return result

    def __iter__(self):
        return iter(self._list_cached if self._all_listed else _DatasetDictKeyIterator(self))

    def __len__(self):
        self._list_all()
        return len(self._list_cached)

    def __str__(self):
        self._list_all()
        return pprint.pformat(self._list_cached, indent=2)

    def __repr__(self):
        self._list_all()
        return str({name: self._list_cached[name] for name in self._list_cached})

    def _list_all(self):
        while not self._all_listed:
            self._list_more()

    def _list_more(self):
        new_listed_names = []
        if not self._all_listed:
            list_result = self._list_fn(continuation_token=self._list_continuation_token)
            if list_result.continuation_token is None:
                self._all_listed = True
            else:
                self._list_continuation_token = list_result.continuation_token
            for ds in list_result.value:
                if ds is not None:
                    self._list_cached[ds.name] = _dto_to_registration(self._workspace, ds)
                    new_listed_names.append(ds.name)
        return new_listed_names


class _DatasetDictKeyIterator():
    def __init__(self, ds_dict):
        self._ds_dict = ds_dict
        self._pending_keys = list(ds_dict._list_cached.keys())

    def __iter__(self):
        return self

    def __next__(self):
        if self._ds_dict._all_listed and not self._pending_keys:
            raise StopIteration
        if not self._pending_keys:
            self._pending_keys.extend(self._ds_dict._list_more())
        if not self._pending_keys:
            raise StopIteration
        return self._pending_keys.pop(0)


def _get_path_from_step(step_type, step_arguments):
    if step_type == 'Microsoft.DPrep.GetDatastoreFilesBlock':
        datastores = step_arguments['datastores']
        if len(datastores) > 1:
            return None
        datastore = datastores[0]
        return '{}/{}'.format(datastore['datastoreName'], datastore['path'].lstrip('/\\'))
    if step_type == 'Microsoft.DPrep.GetFilesBlock':
        resource_details = step_arguments['path']['resourceDetails']
        if len(resource_details) > 1:
            return None
        return resource_details[0]['path']
    if step_type == 'Microsoft.DPrep.ReferenceAndInverseSplitBlock':
        source_step = step_arguments['sourceFilter']['anonymousSteps'][0]
        return _get_path_from_step(source_step['type'], source_step['arguments'])
    _get_logger().warning('Unrecognized type "{}" for first step in FileDataset.'.format(step_type))
    return None
