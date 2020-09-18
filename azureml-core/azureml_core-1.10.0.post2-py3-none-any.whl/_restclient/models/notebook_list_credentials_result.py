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


class NotebookListCredentialsResult(Model):
    """NotebookListCredentialsResult.

    :param primary_access_key:
    :type primary_access_key: str
    :param secondary_access_key:
    :type secondary_access_key: str
    """

    _attribute_map = {
        'primary_access_key': {'key': 'primaryAccessKey', 'type': 'str'},
        'secondary_access_key': {'key': 'secondaryAccessKey', 'type': 'str'},
    }

    def __init__(self, primary_access_key=None, secondary_access_key=None):
        super(NotebookListCredentialsResult, self).__init__()
        self.primary_access_key = primary_access_key
        self.secondary_access_key = secondary_access_key
