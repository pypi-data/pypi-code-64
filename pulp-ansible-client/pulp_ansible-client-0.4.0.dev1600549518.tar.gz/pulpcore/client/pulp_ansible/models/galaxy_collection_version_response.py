# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_ansible.configuration import Configuration


class GalaxyCollectionVersionResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'version': 'str',
        'href': 'str',
        'namespace': 'str',
        'collection': 'str',
        'artifact': 'str',
        'metadata': 'CollectionMetadataResponse'
    }

    attribute_map = {
        'version': 'version',
        'href': 'href',
        'namespace': 'namespace',
        'collection': 'collection',
        'artifact': 'artifact',
        'metadata': 'metadata'
    }

    def __init__(self, version=None, href=None, namespace=None, collection=None, artifact=None, metadata=None, local_vars_configuration=None):  # noqa: E501
        """GalaxyCollectionVersionResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._version = None
        self._href = None
        self._namespace = None
        self._collection = None
        self._artifact = None
        self._metadata = None
        self.discriminator = None

        self.version = version
        if href is not None:
            self.href = href
        if namespace is not None:
            self.namespace = namespace
        if collection is not None:
            self.collection = collection
        if artifact is not None:
            self.artifact = artifact
        self.metadata = metadata

    @property
    def version(self):
        """Gets the version of this GalaxyCollectionVersionResponse.  # noqa: E501


        :return: The version of this GalaxyCollectionVersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this GalaxyCollectionVersionResponse.


        :param version: The version of this GalaxyCollectionVersionResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def href(self):
        """Gets the href of this GalaxyCollectionVersionResponse.  # noqa: E501


        :return: The href of this GalaxyCollectionVersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this GalaxyCollectionVersionResponse.


        :param href: The href of this GalaxyCollectionVersionResponse.  # noqa: E501
        :type: str
        """

        self._href = href

    @property
    def namespace(self):
        """Gets the namespace of this GalaxyCollectionVersionResponse.  # noqa: E501


        :return: The namespace of this GalaxyCollectionVersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this GalaxyCollectionVersionResponse.


        :param namespace: The namespace of this GalaxyCollectionVersionResponse.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def collection(self):
        """Gets the collection of this GalaxyCollectionVersionResponse.  # noqa: E501


        :return: The collection of this GalaxyCollectionVersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._collection

    @collection.setter
    def collection(self, collection):
        """Sets the collection of this GalaxyCollectionVersionResponse.


        :param collection: The collection of this GalaxyCollectionVersionResponse.  # noqa: E501
        :type: str
        """

        self._collection = collection

    @property
    def artifact(self):
        """Gets the artifact of this GalaxyCollectionVersionResponse.  # noqa: E501


        :return: The artifact of this GalaxyCollectionVersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this GalaxyCollectionVersionResponse.


        :param artifact: The artifact of this GalaxyCollectionVersionResponse.  # noqa: E501
        :type: str
        """

        self._artifact = artifact

    @property
    def metadata(self):
        """Gets the metadata of this GalaxyCollectionVersionResponse.  # noqa: E501


        :return: The metadata of this GalaxyCollectionVersionResponse.  # noqa: E501
        :rtype: CollectionMetadataResponse
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this GalaxyCollectionVersionResponse.


        :param metadata: The metadata of this GalaxyCollectionVersionResponse.  # noqa: E501
        :type: CollectionMetadataResponse
        """
        if self.local_vars_configuration.client_side_validation and metadata is None:  # noqa: E501
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GalaxyCollectionVersionResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GalaxyCollectionVersionResponse):
            return True

        return self.to_dict() != other.to_dict()
