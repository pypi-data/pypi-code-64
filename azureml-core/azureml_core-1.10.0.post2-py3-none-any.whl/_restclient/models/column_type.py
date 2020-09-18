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


class ColumnType(Model):
    """ColumnType.

    :param column_name:
    :type column_name: str
    :param type: Possible values include: 'String', 'Boolean', 'Integer',
     'Decimal', 'Date', 'Unknown', 'Error', 'Null', 'DataRow', 'List', 'Stream'
    :type type: str or ~_restclient.models.enum
    :param arguments:
    :type arguments: list[object]
    """

    _attribute_map = {
        'column_name': {'key': 'columnName', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'arguments': {'key': 'arguments', 'type': '[object]'},
    }

    def __init__(self, column_name=None, type=None, arguments=None):
        super(ColumnType, self).__init__()
        self.column_name = column_name
        self.type = type
        self.arguments = arguments
