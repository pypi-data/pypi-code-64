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

from .model_error_response import ModelErrorResponse
from msrest.exceptions import HttpOperationError


class ProfileResponseError(ModelErrorResponse):
    """The error details.

    :param code: The error code.
    :type code: str
    :param status_code: The HTTP status code.
    :type status_code: int
    :param message: The error message.
    :type message: str
    :param details: An array of error detail objects.
    :type details: list[~_restclient.models.ErrorDetails]
    :param correlation: A dictionary of information used to correlate the
     failing request.
    :type correlation: dict[str, str]
    """

    def __init__(self, code=None, status_code=None, message=None, details=None, correlation=None):
        super(ProfileResponseError, self).__init__(code=code, status_code=status_code, message=message, details=details, correlation=correlation)


class ProfileResponseErrorException(HttpOperationError):
    """Server responsed with exception of type: 'ProfileResponseError'.

    :param deserialize: A deserializer
    :param response: Server response to be deserialized.
    """

    def __init__(self, deserialize, response, *args):

        super(ProfileResponseErrorException, self).__init__(deserialize, response, 'ProfileResponseError', *args)
