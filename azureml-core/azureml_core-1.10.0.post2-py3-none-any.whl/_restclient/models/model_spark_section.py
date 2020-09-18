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


class ModelSparkSection(Model):
    """ModelSparkSection.

    :param repositories: The list of spark repositories.
    :type repositories: list[str]
    :param packages: The Spark packages to use.
    :type packages: list[~_restclient.models.SparkMavenPackage]
    :param precache_packages: Whether to precache the packages.
    :type precache_packages: bool
    """

    _attribute_map = {
        'repositories': {'key': 'repositories', 'type': '[str]'},
        'packages': {'key': 'packages', 'type': '[SparkMavenPackage]'},
        'precache_packages': {'key': 'precachePackages', 'type': 'bool'},
    }

    def __init__(self, repositories=None, packages=None, precache_packages=None):
        super(ModelSparkSection, self).__init__()
        self.repositories = repositories
        self.packages = packages
        self.precache_packages = precache_packages
