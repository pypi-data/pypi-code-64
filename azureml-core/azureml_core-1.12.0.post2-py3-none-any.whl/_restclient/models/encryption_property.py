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


class EncryptionProperty(Model):
    """EncryptionProperty.

    :param status: Indicates whether or not the encryption is enabled for the
     workspace. Possible values include: 'Enabled', 'Disabled'
    :type status: str or ~_restclient.models.EncryptionStatus
    :param key_vault_properties: Customer Key vault properties.
    :type key_vault_properties: ~_restclient.models.KeyVaultProperties
    """

    _validation = {
        'status': {'required': True},
        'key_vault_properties': {'required': True},
    }

    _attribute_map = {
        'status': {'key': 'status', 'type': 'str'},
        'key_vault_properties': {'key': 'keyVaultProperties', 'type': 'KeyVaultProperties'},
    }

    def __init__(self, status, key_vault_properties):
        super(EncryptionProperty, self).__init__()
        self.status = status
        self.key_vault_properties = key_vault_properties
