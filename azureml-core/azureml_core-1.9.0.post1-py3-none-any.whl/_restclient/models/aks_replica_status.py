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


class AKSReplicaStatus(Model):
    """AKSReplicaStatus.

    :param desired_replicas: The desired number of replicas.
    :type desired_replicas: int
    :param updated_replicas: The number of updated replicas.
    :type updated_replicas: int
    :param available_replicas: The number of available replicas.
    :type available_replicas: int
    :param error: The error details.
    :type error: ~_restclient.models.AKSReplicaStatusError
    """

    _attribute_map = {
        'desired_replicas': {'key': 'desiredReplicas', 'type': 'int'},
        'updated_replicas': {'key': 'updatedReplicas', 'type': 'int'},
        'available_replicas': {'key': 'availableReplicas', 'type': 'int'},
        'error': {'key': 'error', 'type': 'AKSReplicaStatusError'},
    }

    def __init__(self, desired_replicas=None, updated_replicas=None, available_replicas=None, error=None):
        super(AKSReplicaStatus, self).__init__()
        self.desired_replicas = desired_replicas
        self.updated_replicas = updated_replicas
        self.available_replicas = available_replicas
        self.error = error
