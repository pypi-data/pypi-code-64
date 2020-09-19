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

import pulpcore.client.pulp_2to3_migration
from pulpcore.client.pulp_2to3_migration.models.inline_response2001 import InlineResponse2001  # noqa: E501
from pulpcore.client.pulp_2to3_migration.rest import ApiException

class TestInlineResponse2001(unittest.TestCase):
    """InlineResponse2001 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse2001
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_2to3_migration.models.inline_response2001.InlineResponse2001()  # noqa: E501
        if include_optional :
            return InlineResponse2001(
                count = 123, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulp_2to3_migration.models.pulp_2to3_migration/pulp2_content_response.pulp_2to3_migration.Pulp2ContentResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        pulp2_id = '0', 
                        pulp2_content_type_id = '0', 
                        pulp2_last_updated = 56, 
                        pulp2_storage_path = '0', 
                        downloaded = True, 
                        pulp3_content = '0', 
                        pulp3_repository_version = '0', )
                    ]
            )
        else :
            return InlineResponse2001(
        )

    def testInlineResponse2001(self):
        """Test InlineResponse2001"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
