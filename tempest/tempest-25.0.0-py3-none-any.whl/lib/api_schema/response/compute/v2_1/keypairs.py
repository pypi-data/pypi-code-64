# Copyright 2014 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.lib.api_schema.response.compute.v2_1 import parameter_types

get_keypair = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'keypair': {
                'type': 'object',
                'properties': {
                    'public_key': {'type': 'string'},
                    'name': {'type': 'string'},
                    'fingerprint': {'type': 'string'},
                    'user_id': {'type': 'string'},
                    'deleted': {'type': 'boolean'},
                    'created_at': parameter_types.date_time,
                    'updated_at': parameter_types.date_time_or_null,
                    'deleted_at': parameter_types.date_time_or_null,
                    'id': {'type': 'integer'}

                },
                'additionalProperties': False,
                'required': ['public_key', 'name', 'fingerprint', 'user_id',
                             'deleted', 'created_at', 'updated_at',
                             'deleted_at', 'id']
            }
        },
        'additionalProperties': False,
        'required': ['keypair']
    }
}

create_keypair = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'keypair': {
                'type': 'object',
                'properties': {
                    'fingerprint': {'type': 'string'},
                    'name': {'type': 'string'},
                    'public_key': {'type': 'string'},
                    'user_id': {'type': 'string'},
                    'private_key': {'type': 'string'}
                },
                'additionalProperties': False,
                # When create keypair API is being called with 'Public key'
                # (Importing keypair) then, response body does not contain
                # 'private_key' So it is not defined as 'required'
                'required': ['fingerprint', 'name', 'public_key', 'user_id']
            }
        },
        'additionalProperties': False,
        'required': ['keypair']
    }
}

delete_keypair = {
    'status_code': [202],
}

list_keypairs = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'keypairs': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'keypair': {
                            'type': 'object',
                            'properties': {
                                'public_key': {'type': 'string'},
                                'name': {'type': 'string'},
                                'fingerprint': {'type': 'string'}
                            },
                            'additionalProperties': False,
                            'required': ['public_key', 'name', 'fingerprint']
                        }
                    },
                    'additionalProperties': False,
                    'required': ['keypair']
                }
            }
        },
        'additionalProperties': False,
        'required': ['keypairs']
    }
}
