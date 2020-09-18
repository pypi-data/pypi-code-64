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

from pulpcore.client.pulp_2to3_migration.configuration import Configuration


class Pulp2to3MigrationPulp2RepositoryResponse(object):
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
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'pulp2_object_id': 'str',
        'pulp2_repo_id': 'str',
        'pulp2_repo_type': 'str',
        'is_migrated': 'bool',
        'not_in_plan': 'bool',
        'pulp3_repository_version': 'str',
        'pulp3_remote_href': 'str',
        'pulp3_publication_href': 'str',
        'pulp3_distribution_hrefs': 'str',
        'pulp3_repository_href': 'str'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'pulp2_object_id': 'pulp2_object_id',
        'pulp2_repo_id': 'pulp2_repo_id',
        'pulp2_repo_type': 'pulp2_repo_type',
        'is_migrated': 'is_migrated',
        'not_in_plan': 'not_in_plan',
        'pulp3_repository_version': 'pulp3_repository_version',
        'pulp3_remote_href': 'pulp3_remote_href',
        'pulp3_publication_href': 'pulp3_publication_href',
        'pulp3_distribution_hrefs': 'pulp3_distribution_hrefs',
        'pulp3_repository_href': 'pulp3_repository_href'
    }

    def __init__(self, pulp_href=None, pulp_created=None, pulp2_object_id=None, pulp2_repo_id=None, pulp2_repo_type=None, is_migrated=False, not_in_plan=False, pulp3_repository_version=None, pulp3_remote_href=None, pulp3_publication_href=None, pulp3_distribution_hrefs=None, pulp3_repository_href=None, local_vars_configuration=None):  # noqa: E501
        """Pulp2to3MigrationPulp2RepositoryResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._pulp2_object_id = None
        self._pulp2_repo_id = None
        self._pulp2_repo_type = None
        self._is_migrated = None
        self._not_in_plan = None
        self._pulp3_repository_version = None
        self._pulp3_remote_href = None
        self._pulp3_publication_href = None
        self._pulp3_distribution_hrefs = None
        self._pulp3_repository_href = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        self.pulp2_object_id = pulp2_object_id
        self.pulp2_repo_id = pulp2_repo_id
        self.pulp2_repo_type = pulp2_repo_type
        if is_migrated is not None:
            self.is_migrated = is_migrated
        if not_in_plan is not None:
            self.not_in_plan = not_in_plan
        self.pulp3_repository_version = pulp3_repository_version
        if pulp3_remote_href is not None:
            self.pulp3_remote_href = pulp3_remote_href
        if pulp3_publication_href is not None:
            self.pulp3_publication_href = pulp3_publication_href
        if pulp3_distribution_hrefs is not None:
            self.pulp3_distribution_hrefs = pulp3_distribution_hrefs
        if pulp3_repository_href is not None:
            self.pulp3_repository_href = pulp3_repository_href

    @property
    def pulp_href(self):
        """Gets the pulp_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp_href: The pulp_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this Pulp2to3MigrationPulp2RepositoryResponse.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def pulp2_object_id(self):
        """Gets the pulp2_object_id of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp2_object_id of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp2_object_id

    @pulp2_object_id.setter
    def pulp2_object_id(self, pulp2_object_id):
        """Sets the pulp2_object_id of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp2_object_id: The pulp2_object_id of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and pulp2_object_id is None:  # noqa: E501
            raise ValueError("Invalid value for `pulp2_object_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                pulp2_object_id is not None and len(pulp2_object_id) > 255):
            raise ValueError("Invalid value for `pulp2_object_id`, length must be less than or equal to `255`")  # noqa: E501

        self._pulp2_object_id = pulp2_object_id

    @property
    def pulp2_repo_id(self):
        """Gets the pulp2_repo_id of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp2_repo_id of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp2_repo_id

    @pulp2_repo_id.setter
    def pulp2_repo_id(self, pulp2_repo_id):
        """Sets the pulp2_repo_id of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp2_repo_id: The pulp2_repo_id of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and pulp2_repo_id is None:  # noqa: E501
            raise ValueError("Invalid value for `pulp2_repo_id`, must not be `None`")  # noqa: E501

        self._pulp2_repo_id = pulp2_repo_id

    @property
    def pulp2_repo_type(self):
        """Gets the pulp2_repo_type of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp2_repo_type of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp2_repo_type

    @pulp2_repo_type.setter
    def pulp2_repo_type(self, pulp2_repo_type):
        """Sets the pulp2_repo_type of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp2_repo_type: The pulp2_repo_type of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and pulp2_repo_type is None:  # noqa: E501
            raise ValueError("Invalid value for `pulp2_repo_type`, must not be `None`")  # noqa: E501

        self._pulp2_repo_type = pulp2_repo_type

    @property
    def is_migrated(self):
        """Gets the is_migrated of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The is_migrated of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: bool
        """
        return self._is_migrated

    @is_migrated.setter
    def is_migrated(self, is_migrated):
        """Sets the is_migrated of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param is_migrated: The is_migrated of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: bool
        """

        self._is_migrated = is_migrated

    @property
    def not_in_plan(self):
        """Gets the not_in_plan of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The not_in_plan of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: bool
        """
        return self._not_in_plan

    @not_in_plan.setter
    def not_in_plan(self, not_in_plan):
        """Sets the not_in_plan of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param not_in_plan: The not_in_plan of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: bool
        """

        self._not_in_plan = not_in_plan

    @property
    def pulp3_repository_version(self):
        """Gets the pulp3_repository_version of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501

        RepositoryVersion to be served  # noqa: E501

        :return: The pulp3_repository_version of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp3_repository_version

    @pulp3_repository_version.setter
    def pulp3_repository_version(self, pulp3_repository_version):
        """Sets the pulp3_repository_version of this Pulp2to3MigrationPulp2RepositoryResponse.

        RepositoryVersion to be served  # noqa: E501

        :param pulp3_repository_version: The pulp3_repository_version of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """

        self._pulp3_repository_version = pulp3_repository_version

    @property
    def pulp3_remote_href(self):
        """Gets the pulp3_remote_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp3_remote_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp3_remote_href

    @pulp3_remote_href.setter
    def pulp3_remote_href(self, pulp3_remote_href):
        """Sets the pulp3_remote_href of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp3_remote_href: The pulp3_remote_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """

        self._pulp3_remote_href = pulp3_remote_href

    @property
    def pulp3_publication_href(self):
        """Gets the pulp3_publication_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp3_publication_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp3_publication_href

    @pulp3_publication_href.setter
    def pulp3_publication_href(self, pulp3_publication_href):
        """Sets the pulp3_publication_href of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp3_publication_href: The pulp3_publication_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """

        self._pulp3_publication_href = pulp3_publication_href

    @property
    def pulp3_distribution_hrefs(self):
        """Gets the pulp3_distribution_hrefs of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp3_distribution_hrefs of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp3_distribution_hrefs

    @pulp3_distribution_hrefs.setter
    def pulp3_distribution_hrefs(self, pulp3_distribution_hrefs):
        """Sets the pulp3_distribution_hrefs of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp3_distribution_hrefs: The pulp3_distribution_hrefs of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """

        self._pulp3_distribution_hrefs = pulp3_distribution_hrefs

    @property
    def pulp3_repository_href(self):
        """Gets the pulp3_repository_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501


        :return: The pulp3_repository_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp3_repository_href

    @pulp3_repository_href.setter
    def pulp3_repository_href(self, pulp3_repository_href):
        """Sets the pulp3_repository_href of this Pulp2to3MigrationPulp2RepositoryResponse.


        :param pulp3_repository_href: The pulp3_repository_href of this Pulp2to3MigrationPulp2RepositoryResponse.  # noqa: E501
        :type: str
        """

        self._pulp3_repository_href = pulp3_repository_href

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
        if not isinstance(other, Pulp2to3MigrationPulp2RepositoryResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Pulp2to3MigrationPulp2RepositoryResponse):
            return True

        return self.to_dict() != other.to_dict()
