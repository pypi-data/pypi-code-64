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


class BatchArtifactCreateCommand(Model):
    """BatchArtifactCreateCommand.

    :param paths:
    :type paths: list[~_restclient.models.ArtifactPathDto]
    """

    _attribute_map = {
        'paths': {'key': 'paths', 'type': '[ArtifactPathDto]'},
    }

    def __init__(self, paths=None):
        super(BatchArtifactCreateCommand, self).__init__()
        self.paths = paths
