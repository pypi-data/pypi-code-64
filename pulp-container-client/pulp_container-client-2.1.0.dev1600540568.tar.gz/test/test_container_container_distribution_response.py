# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_container
from pulpcore.client.pulp_container.models.container_container_distribution_response import ContainerContainerDistributionResponse  # noqa: E501
from pulpcore.client.pulp_container.rest import ApiException

class TestContainerContainerDistributionResponse(unittest.TestCase):
    """ContainerContainerDistributionResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ContainerContainerDistributionResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_container.models.container_container_distribution_response.ContainerContainerDistributionResponse()  # noqa: E501
        if include_optional :
            return ContainerContainerDistributionResponse(
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                pulp_href = '0', 
                repository_version = '0', 
                base_path = '0', 
                content_guard = '0', 
                name = '0', 
                repository = '0', 
                registry_path = '0'
            )
        else :
            return ContainerContainerDistributionResponse(
                base_path = '0',
                name = '0',
        )

    def testContainerContainerDistributionResponse(self):
        """Test ContainerContainerDistributionResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
