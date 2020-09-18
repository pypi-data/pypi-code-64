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


class MerkleDiffEntry(Model):
    """MerkleDiffEntry.

    :param operation_type: Possible values include: 'Added', 'Modified',
     'Removed'
    :type operation_type: str or ~_restclient.models.enum
    :param file_path:
    :type file_path: str
    :param is_file:
    :type is_file: bool
    :param old_file_store_id:
    :type old_file_store_id: str
    :param new_file_store_id:
    :type new_file_store_id: str
    """

    _attribute_map = {
        'operation_type': {'key': 'operationType', 'type': 'str'},
        'file_path': {'key': 'filePath', 'type': 'str'},
        'is_file': {'key': 'isFile', 'type': 'bool'},
        'old_file_store_id': {'key': 'oldFileStoreId', 'type': 'str'},
        'new_file_store_id': {'key': 'newFileStoreId', 'type': 'str'},
    }

    def __init__(self, operation_type=None, file_path=None, is_file=None, old_file_store_id=None, new_file_store_id=None):
        super(MerkleDiffEntry, self).__init__()
        self.operation_type = operation_type
        self.file_path = file_path
        self.is_file = is_file
        self.old_file_store_id = old_file_store_id
        self.new_file_store_id = new_file_store_id
