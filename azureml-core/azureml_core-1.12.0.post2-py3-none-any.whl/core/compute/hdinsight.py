# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains functionality for managing HDInsight Cluster compute targets in Azure Machine Learning."""

import copy
import json
import requests
import traceback
from azureml._compute._constants import MLC_COMPUTE_RESOURCE_ID_FMT
from azureml._compute._constants import MLC_WORKSPACE_API_VERSION
from azureml._compute._util import hdinsight_payload_template
from azureml._compute._util import get_requests_session
from azureml.core.compute import ComputeTarget
from azureml.core.compute.compute import ComputeTargetAttachConfiguration
from azureml.exceptions import ComputeTargetException
from azureml._restclient.clientbase import ClientBase


class HDInsightCompute(ComputeTarget):
    """Manages an HDInsight cluster compute target in Azure Machine Learning.

    Azure HDInsight is a popular platform for big-data analytics. The platform provides Apache Spark,
    which can be used to train your model.
    For more information, see `What are compute targets in Azure Machine
    Learning? <https://docs.microsoft.com/azure/machine-learning/concept-compute-target>`_

    .. remarks::

        The following sample shows how to create a Spark for HDInsight cluster in Azure.

        .. code-block:: python

            from azureml.core.compute import ComputeTarget, HDInsightCompute
            from azureml.exceptions import ComputeTargetException
            import os

            try:
            # If you want to connect using SSH key instead of username/password you can provide parameters private_key_file and private_key_passphrase

            # Attaching a HDInsight cluster using the public address of the HDInsight cluster is no longer supported.
            # Instead, use resourceId of the HDInsight cluster.
            # The resourceId of the HDInsight Cluster can be constructed using the following string format:
            # /subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.HDInsight/clusters/<cluster_name>.
            # You can also use subscription_id, resource_group and cluster_name without constructing resourceId.
                attach_config = HDInsightCompute.attach_configuration(resource_id='<resource_id>',
                                                                      ssh_port=22,
                                                                      username=os.environ.get('hdiusername', '<ssh_username>'),
                                                                      password=os.environ.get('hdipassword', '<my_password>'))

                hdi_compute = ComputeTarget.attach(workspace=ws,
                                                   name='myhdi',
                                                   attach_configuration=attach_config)

            except ComputeTargetException as e:
                print("Caught = {}".format(e.message))


            hdi_compute.wait_for_completion(show_output=True)

        Full sample is available from
        https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/training/train-in-spark/train-in-spark.ipynb


    :param workspace: The workspace object containing the HDInsightCompute object to retrieve.
    :type workspace: azureml.core.Workspace
    :param name: The name of the of the HDInsightCompute object to retrieve.
    :type name: str
    """

    _compute_type = 'HDInsight'

    def _initialize(self, workspace, obj_dict):
        """Initialize implementation method.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        name = obj_dict['name']
        compute_resource_id = MLC_COMPUTE_RESOURCE_ID_FMT.format(workspace.subscription_id, workspace.resource_group,
                                                                 workspace.name, name)
        resource_manager_endpoint = self._get_resource_manager_endpoint(workspace)
        mlc_endpoint = '{}{}'.format(resource_manager_endpoint, compute_resource_id)
        location = obj_dict['location']
        compute_type = obj_dict['properties']['computeType']
        tags = obj_dict['tags']
        description = obj_dict['properties']['description']
        created_on = obj_dict['properties'].get('createdOn')
        modified_on = obj_dict['properties'].get('modifiedOn')
        cluster_resource_id = obj_dict['properties']['resourceId']
        cluster_location = obj_dict['properties']['computeLocation'] \
            if 'computeLocation' in obj_dict['properties'] else None
        provisioning_state = obj_dict['properties']['provisioningState']
        provisioning_errors = obj_dict['properties']['provisioningErrors']
        is_attached = obj_dict['properties']['isAttachedCompute']
        vm_size = obj_dict['properties']['properties']['virtualMachineSize'] \
            if 'virtualMachineSize' in obj_dict['properties']['properties'] else None
        address = obj_dict['properties']['properties']['address'] \
            if 'address' in obj_dict['properties']['properties'] else None
        ssh_port = obj_dict['properties']['properties']['sshPort'] \
            if 'sshPort' in obj_dict['properties']['properties'] else None

        super(HDInsightCompute, self)._initialize(compute_resource_id, name, location, compute_type, tags, description,
                                                  created_on, modified_on, provisioning_state, provisioning_errors,
                                                  cluster_resource_id, cluster_location, workspace, mlc_endpoint, None,
                                                  workspace._auth, is_attached)
        self.vm_size = vm_size
        self.address = address
        self.ssh_port = ssh_port

    def __repr__(self):
        """Return the string representation of the HDInsightCompute object.

        :return: String representation of the HDInsightCompute object
        :rtype: str
        """
        return super().__repr__()

    @staticmethod
    def attach(workspace, name, username, address, ssh_port='22', password='', private_key_file='',
               private_key_passphrase=''):
        """DEPRECATED. Use the ``attach_configuration`` method instead.

        Associate an existing HDI resource with the provided workspace.

        :param workspace: The workspace object to associate the compute resource with.
        :type workspace: azureml.core.Workspace
        :param name: The name to associate with the compute resource inside the provided workspace. Does not have to
            match the name of the compute resource to be attached.
        :type name: str
        :param username: The username needed to access the resource.
        :type username: str
        :param address: The address of the resource to be attached.
        :type address: str
        :param ssh_port: The exposed port for the resource. Defaults to 22.
        :type ssh_port: int
        :param password: The password needed to access the resource.
        :type password: str
        :param private_key_file: The path to a file containing the private key for the resource.
        :type private_key_file: str
        :param private_key_passphrase: The private key phrase needed to access the resource.
        :type private_key_passphrase: str
        :return: An HDInsightCompute object representation of the compute object.
        :rtype: azureml.core.compute.hdinsight.HDInsightCompute
        :raises azureml.exceptions.ComputeTargetException:
        """
        raise ComputeTargetException('This method is DEPRECATED. Please use the following code to attach a HDI '
                                     'compute resource.\n'
                                     '# Attach HDI\n'
                                     'attach_config = HDInsightCompute.attach_configuration(address="ip_address",\n'
                                     '                                                      ssh_port=22,\n'
                                     '                                                      username="username",\n'
                                     '                                                      password=None, # If '
                                     'using ssh key\n'
                                     '                                                      private_key_file='
                                     '"path_to_a_file",\n'
                                     '                                                      private_key_passphrase='
                                     '"some_key_phrase")\n'
                                     'compute = ComputeTarget.attach(workspace, name, attach_config)')

    @staticmethod
    def _attach(workspace, name, config):
        """Associates an existing HDI resource with the provided workspace.

        :param workspace: The workspace object to associate the compute resource with.
        :type workspace: azureml.core.Workspace
        :param name: The name to associate with the compute resource inside the provided workspace. Does not have to
            match the name of the compute resource to be attached.
        :type name: str
        :param config: Attach configuration object,
        :type config: azureml.core.compute.hdinsight.HDInsightAttachConfiguration
        :return: A HDInsightCompute object representation of the compute object
        :rtype: azureml.core.compute.hdinsight.HDInsightCompute
        :raises azureml.exceptions.ComputeTargetException:
        """
        resource_id = config.resource_id
        if not resource_id and config.subscription_id and config.resource_group and config.cluster_name:
            resource_id = HDInsightCompute._build_resource_id(config.subscription_id, config.resource_group,
                                                              config.cluster_name)
        attach_payload = HDInsightCompute._build_attach_payload(resource_id, config.address,
                                                                config.ssh_port, config.username,
                                                                config.password, config.private_key_file,
                                                                config.private_key_passphrase)
        return ComputeTarget._attach(workspace, name, attach_payload, HDInsightCompute)

    @staticmethod
    def _build_resource_id(subscription_id, resource_group, cluster_name):
        """Build the Azure resource ID for the compute resource.

        :param subscription_id: The Azure subscription ID
        :type subscription_id: str
        :param resource_group: Name of the resource group in which HDI cluster is located.
        :type resource_group: str
        :param cluster_name: The HDI cluster name
        :type cluster_name: str
        :return: The Azure resource ID for the compute resource
        :rtype: str
        """
        HDI_RESOURCE_ID_FMT = ('/subscriptions/{}/resourcegroups/{}/providers/Microsoft.HDInsight/clusters/{}')
        return HDI_RESOURCE_ID_FMT.format(subscription_id, resource_group, cluster_name)

    @staticmethod
    def attach_configuration(username, subscription_id=None, resource_group=None, cluster_name=None, resource_id=None,
                             address=None, ssh_port='22', password='', private_key_file='', private_key_passphrase=''):
        """Create a configuration object for attaching an HDInsight compute target.

        Attaching a HDInsight cluster using the public address of the HDInsight cluster is no longer supported.
        Instead, use resourceId of the HDInsight cluster.
        The resourceId of the HDInsight Cluster can be constructed using the following string format:
        "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/
        providers/Microsoft.HDInsight/clusters/<cluster_name>".

        You can also use subscription_id, resource_group and cluster_name without constructing resourceId.
        For more details: https://aka.ms/azureml-compute-hdi

        :param username: The username needed to access the resource.
        :type username: str
        :param subscription_id: The Azure subscription ID
        :type subscription_id: str
        :param resource_group: Name of the resource group in which HDI cluster is located.
        :type resource_group: str
        :param cluster_name: The HDI cluster name
        :type cluster_name: str
        :param resource_id: The Azure Resource Manager (ARM) resource ID for the resource to be attached.
        :type resource_id: str
        :param address: The address for the resource to be attached.
        :type address: str
        :param ssh_port: The exposed port for the resource. Defaults to 22.
        :type ssh_port: int
        :param password: The password needed to access the resource.
        :type password: str
        :param private_key_file: The path to a file containing the private key for the resource.
        :type private_key_file: str
        :param private_key_passphrase: The private key phrase needed to access the resource.
        :type private_key_passphrase: str
        :return: A configuration object to be used when attaching a Compute object.
        :rtype: azureml.core.compute.hdinsight.HDInsightAttachConfiguration
        """
        config = HDInsightAttachConfiguration(username, subscription_id, resource_group, cluster_name, resource_id,
                                              address, ssh_port, password, private_key_file, private_key_passphrase)
        return config

    @staticmethod
    def _build_attach_payload(resource_id, address, ssh_port, username, password=None, private_key_file=None,
                              private_key_passphrase=None):
        """Build attach payload.

        :param resource_id:
        :type resource_id: str
        :param address:
        :type address: str
        :param ssh_port:
        :type ssh_port: int
        :param username:
        :type username: str
        :param password:
        :type password: str
        :param private_key_file:
        :type private_key_file: str
        :param private_key_passphrase:
        :type private_key_passphrase: str
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(hdinsight_payload_template)
        if not address and not resource_id:
            raise ComputeTargetException('Error, missing address/resource_id.')
        if address and resource_id:
            raise ComputeTargetException('Error, only one of address/resource_id can be used.')
        if not ssh_port:
            raise ComputeTargetException('Error, missing ssh-port.')

        if not username:
            raise ComputeTargetException('Error, no username provided. Please provide a username and either a'
                                         'password or key information.')
        json_payload['properties']['properties']['administratorAccount']['username'] = username
        if not password and not private_key_file:
            raise ComputeTargetException('Error, no password or key information provided. Please provide either a '
                                         'password or key information.')
        if password and private_key_file:
            raise ComputeTargetException('Invalid attach information, both password and key information provided. '
                                         'Please provide either a password or key information')
        if password:
            json_payload['properties']['properties']['administratorAccount']['password'] = password
            del (json_payload['properties']['properties']['administratorAccount']['publicKeyData'])
            del (json_payload['properties']['properties']['administratorAccount']['privateKeyData'])
        else:
            try:
                with open(private_key_file, 'r') as private_key_file_obj:
                    private_key = private_key_file_obj.read()
            except (IOError, OSError) as exc:
                raise ComputeTargetException("Error while reading key information:\n"
                                             "{}".format(traceback.format_exc().splitlines()[-1]))
            json_payload['properties']['properties']['administratorAccount']['privateKeyData'] = private_key
            if private_key_passphrase:
                json_payload['properties']['properties']['administratorAccount']['passphrase'] = private_key_passphrase

        del (json_payload['properties']['properties']['virtualMachineSize'])
        del (json_payload['properties']['computeLocation'])
        json_payload['properties']['properties']['address'] = address
        json_payload['properties']['resourceId'] = resource_id
        json_payload['properties']['properties']['sshPort'] = ssh_port
        return json_payload

    def refresh_state(self):
        """Perform an in-place update of the properties of the object.

        This method updates the properties based on the current state of the corresponding cloud object.
        This is primarily used for manual polling of compute state.
        """
        cluster = HDInsightCompute(self.workspace, self.name)
        self.modified_on = cluster.modified_on
        self.provisioning_state = cluster.provisioning_state
        self.provisioning_errors = cluster.provisioning_errors
        self.cluster_resource_id = cluster.cluster_resource_id
        self.cluster_location = cluster.cluster_location
        self.vm_size = cluster.vm_size
        self.address = cluster.address
        self.ssh_port = cluster.ssh_port

    def delete(self):
        """Delete is not supported for HDInsightCompute object. Use :meth:`detach` instead.

        :raises azureml.exceptions.ComputeTargetException:
        """
        raise ComputeTargetException('Delete is not supported for HDICompute object. Try to use detach instead.')

    def detach(self):
        """Detaches the HDInsightCompute object from its associated workspace.

        Underlying cloud objects are not deleted, only the association is removed.

        :raises azureml.exceptions.ComputeTargetException:
        """
        self._delete_or_detach('detach')

    def get_credentials(self):
        """Retrieve the credentials for the HDInsightCompute target.

        :return: The credentials for the HDInsightCompute target
        :rtype: dict
        :raises azureml.exceptions.ComputeTargetException:
        """
        endpoint = self._mlc_endpoint + '/listKeys'
        headers = self._auth.get_authentication_header()
        params = {'api-version': MLC_WORKSPACE_API_VERSION}
        resp = ClientBase._execute_func(get_requests_session().post, endpoint, params=params, headers=headers)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ComputeTargetException('Received bad response from MLC:\n'
                                         'Response Code: {}\n'
                                         'Headers: {}\n'
                                         'Content: {}'.format(resp.status_code, resp.headers, resp.content))
        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        creds_content = json.loads(content)
        return creds_content

    def serialize(self):
        """Convert this HDInsightCompute object into a JSON serialized dictionary.

        :return: The JSON representation of this HDICompute object.
        :rtype: dict
        """
        hdinsight_properties = {'vmSize': self.vm_size, 'address': self.address, 'ssh-port': self.ssh_port}
        cluster_properties = {'computeType': self.type, 'computeLocation': self.cluster_location,
                              'description': self.description, 'resourceId': self.cluster_resource_id,
                              'provisioningErrors': self.provisioning_errors,
                              'provisioningState': self.provisioning_state, 'properties': hdinsight_properties}
        return {'id': self.id, 'name': self.name, 'tags': self.tags, 'location': self.location,
                'properties': cluster_properties}

    @staticmethod
    def deserialize(workspace, object_dict):
        """Convert a JSON object into a HDInsightCompute object.

        .. remarks::

            Raises a :class:`azureml.exceptions.ComputeTargetException` if the provided
            workspace is not the workspace the Compute is associated with.

        :param workspace: The workspace object the HDInsightCompute object is associated with.
        :type workspace: azureml.core.Workspace
        :param object_dict: A JSON object to convert to a HDInsightCompute object.
        :type object_dict: dict
        :return: The HDInsightCompute representation of the provided JSON object.
        :rtype: azureml.core.compute.hdinsight.HDInsightCompute
        :raises azureml.exceptions.ComputeTargetException:
        """
        HDInsightCompute._validate_get_payload(object_dict)
        target = HDInsightCompute(None, None)
        target._initialize(workspace, object_dict)
        return target

    @staticmethod
    def _validate_get_payload(payload):
        if 'properties' not in payload or 'computeType' not in payload['properties']:
            raise ComputeTargetException('Invalid cluster payload:\n'
                                         '{}'.format(payload))
        if payload['properties']['computeType'] != HDInsightCompute._compute_type:
            raise ComputeTargetException('Invalid cluster payload, not "{}":\n'
                                         '{}'.format(HDInsightCompute._compute_type, payload))
        for arm_key in ['location', 'id', 'tags']:
            if arm_key not in payload:
                raise ComputeTargetException('Invalid cluster payload, missing ["{}"]:\n'
                                             '{}'.format(arm_key, payload))
        for key in ['properties', 'provisioningErrors', 'description', 'provisioningState', 'resourceId']:
            if key not in payload['properties']:
                raise ComputeTargetException('Invalid cluster payload, missing ["properties"]["{}"]:\n'
                                             '{}'.format(key, payload))


class HDInsightAttachConfiguration(ComputeTargetAttachConfiguration):
    """Represents configuration parameters for attaching HDInsightCompute targets.

    Use the ``attach_configuration`` method of the
    :class:`azureml.core.compute.hdinsight.HDInsightCompute` class to
    specify attach parameters.

    :param username: The username needed to access the resource.
    :type username: str
    :param subscription_id: The Azure subscription ID
    :type subscription_id: str
    :param resource_group: Name of the resource group in which HDI cluster is located.
    :type resource_group: str
    :param cluster_name: The HDI cluster name
    :type cluster_name: str
    :param resource_id: The arm resource_id of the resource to be attached.
    :type resource_id: str
    :param address: The address of the resource to be attached.
    :type address: str
    :param ssh_port: The exposed port for the resource. Defaults to 22.
    :type ssh_port: int
    :param password: The password needed to access the resource.
    :type password: str
    :param private_key_file: The path to a file containing the private key for the resource.
    :type private_key_file: str
    :param private_key_passphrase: The private key phrase needed to access the resource.
    :type private_key_passphrase: str
    """

    def __init__(self, username, subscription_id=None, resource_group=None, cluster_name=None, resource_id=None,
                 address=None, ssh_port='22', password='', private_key_file='', private_key_passphrase=''):
        """Initialize the configuration object.

        :param username: The username needed to access the resource.
        :type username: str
        :param subscription_id: The Azure subscription ID
        :type subscription_id: str
        :param resource_group: Name of the resource group in which HDI cluster is located.
        :type resource_group: str
        :param cluster_name: The HDI cluster name
        :type cluster_name: str
        :param resource_id: The arm resource_id of the resource to be attached.
        :type resource_id: str
        :param address: The address the resource to be attached.
        :type address: str
        :param ssh_port: The exposed port for the resource. Defaults to 22.
        :type ssh_port: int
        :param password: The password needed to access the resource.
        :type password: str
        :param private_key_file: The path to a file containing the private key for the resource.
        :type private_key_file: str
        :param private_key_passphrase: The private key phrase needed to access the resource.
        :type private_key_passphrase: str
        :return: The configuration object.
        :rtype: azureml.core.compute.hdinsight.HDInsightAttachConfiguration
        """
        super(HDInsightAttachConfiguration, self).__init__(HDInsightCompute)
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.cluster_name = cluster_name
        self.resource_id = resource_id
        self.address = address
        self.ssh_port = ssh_port
        self.username = username
        self.password = password
        self.private_key_file = private_key_file
        self.private_key_passphrase = private_key_passphrase
        self.validate_configuration()

    def validate_configuration(self):
        """Check that the specified configuration values are valid.

        Raises a :class:`azureml.exceptions.ComputeTargetException` if validation fails.

        :raises azureml.exceptions.ComputeTargetException:
        """
        if not self.username:
            raise ComputeTargetException('username is not provided.')

        if self.subscription_id and self.resource_group and self.cluster_name:
            # make sure do not use other info
            if self.address:
                raise ComputeTargetException('If subscription_id, resource_group, cluster_name are provided, please '
                                             'do not provide address.')
            if self.resource_id:
                raise ComputeTargetException('If subscription_id, resource_group, cluster_name are provided, please '
                                             'do not provide resource_id.')
        elif self.resource_id:
            # resource_id is provided, validate resource_id
            resource_parts = self.resource_id.split('/')
            if len(resource_parts) != 9:
                raise ComputeTargetException('Invalid resource_id provided: {}'.format(self.resource_id))
            resource_type = resource_parts[6]
            if resource_type != 'Microsoft.HDInsight':
                raise ComputeTargetException('Invalid resource_id provided, resource type {} does not match for '
                                             'HDInsight'.format(resource_type))
            # make sure do not use other info
            if self.address:
                raise ComputeTargetException('Since resource_id is provided, please do not provide address.')
            if self.subscription_id:
                raise ComputeTargetException('Since resource_id is provided, please do not provide subscription_id.')
            if self.resource_group:
                raise ComputeTargetException('Since resource_id is provided, please do not provide resource_group.')
            if self.cluster_name:
                raise ComputeTargetException('Since resource_id is provided, please do not provide cluster_name.')
        elif self.address:
            # make sure do not use other info
            if self.resource_id:
                raise ComputeTargetException('Since address is provided, please do not provide resource_id.')
            if self.subscription_id:
                raise ComputeTargetException('Since address is provided, please do not provide subscription_id.')
            if self.resource_group:
                raise ComputeTargetException('Since address is provided, please do not provide resource_group.')
            if self.cluster_name:
                raise ComputeTargetException('Since address is provided, please do not provide cluster_name.')
        else:
            # neither resource_id nor other info is provided
            raise ComputeTargetException('Please provide subscription_id, resource_group, cluster_name or provide '
                                         'resource_id or address for HDInsight being attached.')
