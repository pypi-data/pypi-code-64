# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ServicePrincipalCredentials(Model):
    """Service principal credentials.

    :param client_id: Client Id
    :type client_id: str
    :param client_secret: Client secret
    :type client_secret: str
    """

    _validation = {
        'client_id': {'required': True},
        'client_secret': {'required': True},
    }

    _attribute_map = {
        'client_id': {'key': 'clientId', 'type': 'str'},
        'client_secret': {'key': 'clientSecret', 'type': 'str'},
    }

    def __init__(self, client_id, client_secret):
        super(ServicePrincipalCredentials, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
