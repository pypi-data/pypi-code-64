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

from .model_docker_section import ModelDockerSection


class ModelEnvironmentDefinitionDocker(ModelDockerSection):
    """The definition of a Docker container.

    :param base_image: Base image used for Docker-based runs. Mutually
     exclusive with BaseDockerfile.
    :type base_image: str
    :param base_dockerfile: Base Dockerfile used for Docker-based runs.
     Mutually exclusive with BaseImage.
    :type base_dockerfile: str
    :param base_image_registry: Image registry that contains the base image.
    :type base_image_registry:
     ~_restclient.models.ModelDockerSectionBaseImageRegistry
    """

    def __init__(self, base_image=None, base_dockerfile=None, base_image_registry=None):
        super(ModelEnvironmentDefinitionDocker, self).__init__(base_image=base_image, base_dockerfile=base_dockerfile, base_image_registry=base_image_registry)
