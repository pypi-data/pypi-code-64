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

from pulpcore.client.pulp_container.configuration import Configuration


class PatchedcontainerContainerDistribution(object):
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
        'repository_version': 'str',
        'repository': 'str',
        'name': 'str',
        'content_guard': 'str',
        'base_path': 'str'
    }

    attribute_map = {
        'repository_version': 'repository_version',
        'repository': 'repository',
        'name': 'name',
        'content_guard': 'content_guard',
        'base_path': 'base_path'
    }

    def __init__(self, repository_version=None, repository=None, name=None, content_guard=None, base_path=None, local_vars_configuration=None):  # noqa: E501
        """PatchedcontainerContainerDistribution - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._repository_version = None
        self._repository = None
        self._name = None
        self._content_guard = None
        self._base_path = None
        self.discriminator = None

        self.repository_version = repository_version
        self.repository = repository
        if name is not None:
            self.name = name
        if content_guard is not None:
            self.content_guard = content_guard
        if base_path is not None:
            self.base_path = base_path

    @property
    def repository_version(self):
        """Gets the repository_version of this PatchedcontainerContainerDistribution.  # noqa: E501

        RepositoryVersion to be served  # noqa: E501

        :return: The repository_version of this PatchedcontainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._repository_version

    @repository_version.setter
    def repository_version(self, repository_version):
        """Sets the repository_version of this PatchedcontainerContainerDistribution.

        RepositoryVersion to be served  # noqa: E501

        :param repository_version: The repository_version of this PatchedcontainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._repository_version = repository_version

    @property
    def repository(self):
        """Gets the repository of this PatchedcontainerContainerDistribution.  # noqa: E501

        The latest RepositoryVersion for this Repository will be served.  # noqa: E501

        :return: The repository of this PatchedcontainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this PatchedcontainerContainerDistribution.

        The latest RepositoryVersion for this Repository will be served.  # noqa: E501

        :param repository: The repository of this PatchedcontainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def name(self):
        """Gets the name of this PatchedcontainerContainerDistribution.  # noqa: E501

        A unique name. Ex, `rawhide` and `stable`.  # noqa: E501

        :return: The name of this PatchedcontainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PatchedcontainerContainerDistribution.

        A unique name. Ex, `rawhide` and `stable`.  # noqa: E501

        :param name: The name of this PatchedcontainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def content_guard(self):
        """Gets the content_guard of this PatchedcontainerContainerDistribution.  # noqa: E501

        An optional content-guard. If none is specified, a default one will be used.  # noqa: E501

        :return: The content_guard of this PatchedcontainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._content_guard

    @content_guard.setter
    def content_guard(self, content_guard):
        """Sets the content_guard of this PatchedcontainerContainerDistribution.

        An optional content-guard. If none is specified, a default one will be used.  # noqa: E501

        :param content_guard: The content_guard of this PatchedcontainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._content_guard = content_guard

    @property
    def base_path(self):
        """Gets the base_path of this PatchedcontainerContainerDistribution.  # noqa: E501

        The base (relative) path component of the published url. Avoid paths that                     overlap with other distribution base paths (e.g. \"foo\" and \"foo/bar\")  # noqa: E501

        :return: The base_path of this PatchedcontainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path):
        """Sets the base_path of this PatchedcontainerContainerDistribution.

        The base (relative) path component of the published url. Avoid paths that                     overlap with other distribution base paths (e.g. \"foo\" and \"foo/bar\")  # noqa: E501

        :param base_path: The base_path of this PatchedcontainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._base_path = base_path

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
        if not isinstance(other, PatchedcontainerContainerDistribution):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatchedcontainerContainerDistribution):
            return True

        return self.to_dict() != other.to_dict()
