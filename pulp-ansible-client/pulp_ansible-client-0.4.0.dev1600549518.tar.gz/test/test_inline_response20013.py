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

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.models.inline_response20013 import InlineResponse20013  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException

class TestInlineResponse20013(unittest.TestCase):
    """InlineResponse20013 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse20013
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_ansible.models.inline_response20013.InlineResponse20013()  # noqa: E501
        if include_optional :
            return InlineResponse20013(
                meta = null, 
                links = null, 
                data = [
                    pulpcore.client.pulp_ansible.models.collection_response.CollectionResponse(
                        href = '0', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        namespace = '0', 
                        name = '0', 
                        deprecated = True, 
                        versions_url = '0', 
                        highest_version = pulpcore.client.pulp_ansible.models.highest_version.highest_version(), )
                    ]
            )
        else :
            return InlineResponse20013(
        )

    def testInlineResponse20013(self):
        """Test InlineResponse20013"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
