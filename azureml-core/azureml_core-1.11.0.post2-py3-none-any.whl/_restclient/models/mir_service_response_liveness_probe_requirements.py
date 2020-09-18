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

from .liveness_probe_requirements import LivenessProbeRequirements


class MirServiceResponseLivenessProbeRequirements(LivenessProbeRequirements):
    """The liveness probe requirements.

    :param failure_threshold: The number of failures to allow before returning
     an unhealthy status.
    :type failure_threshold: int
    :param success_threshold: The number of successful probes before returning
     a healthy status.
    :type success_threshold: int
    :param timeout_seconds: The probe timeout in seconds.
    :type timeout_seconds: int
    :param period_seconds: The length of time between probes in seconds.
    :type period_seconds: int
    :param initial_delay_seconds: The delay before the first probe in seconds.
    :type initial_delay_seconds: int
    """

    def __init__(self, failure_threshold=None, success_threshold=None, timeout_seconds=None, period_seconds=None, initial_delay_seconds=None):
        super(MirServiceResponseLivenessProbeRequirements, self).__init__(failure_threshold=failure_threshold, success_threshold=success_threshold, timeout_seconds=timeout_seconds, period_seconds=period_seconds, initial_delay_seconds=initial_delay_seconds)
