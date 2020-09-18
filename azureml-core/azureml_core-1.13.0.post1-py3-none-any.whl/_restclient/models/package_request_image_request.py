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

from .environment_image_request import EnvironmentImageRequest


class PackageRequestImageRequest(EnvironmentImageRequest):
    """Description of the package contents.

    :param driver_program: The name of the driver file.
    :type driver_program: str
    :param assets: The list of assets.
    :type assets: list[~_restclient.models.ImageAsset]
    :param model_ids: The list of model Ids.
    :type model_ids: list[str]
    :param environment: The details of the AZURE ML environment.
    :type environment: ~_restclient.models.EnvironmentImageRequestEnvironment
    """

    def __init__(self, driver_program=None, assets=None, model_ids=None, environment=None):
        super(PackageRequestImageRequest, self).__init__(driver_program=driver_program, assets=assets, model_ids=model_ids, environment=environment)
