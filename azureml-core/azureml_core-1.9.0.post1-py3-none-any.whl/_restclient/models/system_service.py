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


class SystemService(Model):
    """A system service running on a compute.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar system_service_type: The type of this system service.
    :vartype system_service_type: str
    :ivar public_ip_address: Public IP address
    :vartype public_ip_address: str
    :ivar version: The version for this type.
    :vartype version: str
    """

    _validation = {
        'system_service_type': {'readonly': True},
        'public_ip_address': {'readonly': True},
        'version': {'readonly': True},
    }

    _attribute_map = {
        'system_service_type': {'key': 'systemServiceType', 'type': 'str'},
        'public_ip_address': {'key': 'publicIpAddress', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
    }

    def __init__(self):
        super(SystemService, self).__init__()
        self.system_service_type = None
        self.public_ip_address = None
        self.version = None
