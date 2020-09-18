# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse

from .. import models


class MachineLearningComputeOperations(object):
    """MachineLearningComputeOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: Version of Azure Machine Learning resource provider API. Constant value: "2019-06-01".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config
        self.api_version = "2019-06-01"

    def list_by_workspace(
            self, resource_group_name, workspace_name, custom_headers=None, raw=False, **operation_config):
        """Gets computes in specified workspace.

        :param resource_group_name: Name of the resource group in which
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PaginatedComputeResourcesList or ClientRawResponse if
         raw=true
        :rtype:
         ~machinelearningservicesswagger.models.PaginatedComputeResourcesList
         or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseWrapperException<machinelearningservicesswagger.models.ErrorResponseWrapperException>`
        """
        # Construct URL
        url = self.list_by_workspace.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        if self.config.compute_type is not None:
            query_parameters['compute-type'] = self._serialize.query("self.config.compute_type",
                                                                     self.config.compute_type, 'str')
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')
        if self.config.skiptoken is not None:
            query_parameters['$skiptoken'] = self._serialize.query("self.config.skiptoken",
                                                                   self.config.skiptoken, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseWrapperException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PaginatedComputeResourcesList', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    list_by_workspace.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroup/' +
                                  '{resourceGroupName}/providers/Microsoft.MachineLearningServices' +
                                  '/workspaces/{workspaceName}/computes'}

    def get(self, resource_group_name, workspace_name, compute_name,
            custom_headers=None, raw=False, **operation_config):
        """Gets compute definition by its name. Any secrets (storage keys, service
        credentials, etc) are not returned - use 'keys' nested resource to get
        them.

        :param resource_group_name: Name of the resource group in which
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param compute_name: Name of the Azure Machine Learning compute.
        :type compute_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ComputeResource or ClientRawResponse if raw=true
        :rtype: ~machinelearningservicesswagger.models.ComputeResource or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseWrapperException<machinelearningservicesswagger.models.ErrorResponseWrapperException>`
        """
        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'computeName': self._serialize.url("compute_name", compute_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseWrapperException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('ComputeResource', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroup/{resourceGroupName}' +
                    '/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/computes/{computeName}'}

    def create_or_update(self, resource_group_name, workspace_name, compute_name,
                         parameters, custom_headers=None, raw=False, **operation_config):
        """Creates or updates compute. This call will overwrite a compute if it
        exists. This is a nonrecoverable operation. If your intent is to create
        a new compute, do a GET first to verify that it does not exist yet.

        :param resource_group_name: Name of the resource group in which
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param compute_name: Name of the Azure Machine Learning compute.
        :type compute_name: str
        :param parameters: Payload with Machine Learning compute definition.
        :type parameters:
         ~machinelearningservicesswagger.models.ComputeResource
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ComputeResource or ClientRawResponse if raw=true
        :rtype: ~machinelearningservicesswagger.models.ComputeResource or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseWrapperException<machinelearningservicesswagger.models.ErrorResponseWrapperException>`
        """
        # Construct URL
        url = self.create_or_update.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'computeName': self._serialize.url("compute_name", compute_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(parameters, 'ComputeResource')

        # Construct and send request
        request = self._client.put(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200, 201]:
            raise models.ErrorResponseWrapperException(self._deserialize, response)

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('ComputeResource', response)
            header_dict = {
                'Azure-AsyncOperation': 'str',
            }
        if response.status_code == 201:
            deserialized = self._deserialize('ComputeResource', response)
            header_dict = {
                'Azure-AsyncOperation': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    create_or_update.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroup/{resourceGroupName}' +
                                 '/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}' +
                                 '/computes/{computeName}'}

    def update(self, resource_group_name, workspace_name, compute_name, parameters,
               custom_headers=None, raw=False, **operation_config):
        """Modifies an existing Machine Learning compute.

        :param resource_group_name: Name of the resource group in which
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param compute_name: Name of the Azure Machine Learning compute.
        :type compute_name: str
        :param parameters: Payload with Machine Learning compute definition.
        :type parameters:
         ~machinelearningservicesswagger.models.ComputeResource
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ComputeResource or ClientRawResponse if raw=true
        :rtype: ~machinelearningservicesswagger.models.ComputeResource or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseWrapperException<machinelearningservicesswagger.models.ErrorResponseWrapperException>`
        """
        # Construct URL
        url = self.update.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'computeName': self._serialize.url("compute_name", compute_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct body
        body_content = self._serialize.body(parameters, 'ComputeResource')

        # Construct and send request
        request = self._client.patch(url, query_parameters)
        response = self._client.send(
            request, header_parameters, body_content, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseWrapperException(self._deserialize, response)

        deserialized = None
        header_dict = {}

        if response.status_code == 200:
            deserialized = self._deserialize('ComputeResource', response)
            header_dict = {
                'Azure-AsyncOperation': 'str',
            }

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            client_raw_response.add_headers(header_dict)
            return client_raw_response

        return deserialized
    update.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroup/{resourceGroupName}/providers' +
                       '/Microsoft.MachineLearningServices/workspaces/{workspaceName}/computes/{computeName}'}

    def delete(self, resource_group_name, workspace_name, compute_name, custom_headers=None,
               raw=False, **operation_config):
        """Deletes specified Machine Learning compute.

        :param resource_group_name: Name of the resource group in which
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param compute_name: Name of the Azure Machine Learning compute.
        :type compute_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseWrapperException<machinelearningservicesswagger.models.ErrorResponseWrapperException>`
        """
        # Construct URL
        url = self.delete.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'computeName': self._serialize.url("compute_name", compute_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.delete(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200, 202, 204]:
            raise models.ErrorResponseWrapperException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            client_raw_response.add_headers({
                'Azure-AsyncOperation': 'str',
            })
            return client_raw_response
    delete.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroup/{resourceGroupName}' +
                       '/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}' +
                       '/computes/{computeName}'}

    def list_keys(self, resource_group_name, workspace_name, compute_name, custom_headers=None,
                  raw=False, **operation_config):
        """Gets secrets related to Machine Learning compute (storage keys, service
        credentials, etc).

        :param resource_group_name: Name of the resource group in which
         workspace is located.
        :type resource_group_name: str
        :param workspace_name: Name of Azure Machine Learning workspace.
        :type workspace_name: str
        :param compute_name: Name of the Azure Machine Learning compute.
        :type compute_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ComputeSecrets or ClientRawResponse if raw=true
        :rtype: ~machinelearningservicesswagger.models.ComputeSecrets or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseWrapperException<machinelearningservicesswagger.models.ErrorResponseWrapperException>`
        """
        # Construct URL
        url = self.list_keys.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'computeName': self._serialize.url("compute_name", compute_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.post(url, query_parameters)
        response = self._client.send(request, header_parameters, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseWrapperException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('ComputeSecrets', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    list_keys.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroup/{resourceGroupName}' +
                          '/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}' +
                          '/computes/{computeName}/listKeys'}
