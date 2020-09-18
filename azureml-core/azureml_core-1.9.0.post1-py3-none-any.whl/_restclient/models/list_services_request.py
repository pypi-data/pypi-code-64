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


class ListServicesRequest(Model):
    """The  class for getting services.

    :param image_id: The Image Id.
    :type image_id: str
    :param image_digest: The Image Digest.
    :type image_digest: str
    :param image_name: The Image name.
    :type image_name: str
    :param model_id: The Model Id.
    :type model_id: str
    :param model_name: The Model Name.
    :type model_name: str
    :param name: The object name.
    :type name: str
    :param tag: The object tag.
    :type tag: str
    :param count: The number of items to retrieve in a page.
    :type count: int
    :param compute_type: The compute environment type.
    :type compute_type: str
    :param skip_token: The continuation token to retrieve the next page.
    :type skip_token: str
    :param tags: A set of tags with which to filter the returned models.
     It is a comma separated string of tags key or tags key=value
     Example: tagKey1,tagKey2,tagKey3=value3 .
    :type tags: str
    :param properties: A set of properties with which to filter the returned
     models.
     It is a comma separated string of properties key and/or properties
     key=value
     Example: propKey1,propKey2,propKey3=value3 .
    :type properties: str
    :param run_id: runId for model associated with service.
    :type run_id: str
    :param expand: Set to True to include Model details.
    :type expand: bool
    :param orderby: The option to order the response. Possible values include:
     'CreatedAtDesc', 'CreatedAtAsc', 'UpdatedAtDesc', 'UpdatedAtAsc'. Default
     value: "UpdatedAtDesc" .
    :type orderby: str or ~_restclient.models.OrderString
    """

    _attribute_map = {
        'image_id': {'key': 'imageId', 'type': 'str'},
        'image_digest': {'key': 'imageDigest', 'type': 'str'},
        'image_name': {'key': 'imageName', 'type': 'str'},
        'model_id': {'key': 'modelId', 'type': 'str'},
        'model_name': {'key': 'modelName', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'tag': {'key': 'tag', 'type': 'str'},
        'count': {'key': 'count', 'type': 'int'},
        'compute_type': {'key': 'computeType', 'type': 'str'},
        'skip_token': {'key': 'skipToken', 'type': 'str'},
        'tags': {'key': 'tags', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'str'},
        'run_id': {'key': 'runId', 'type': 'str'},
        'expand': {'key': 'expand', 'type': 'bool'},
        'orderby': {'key': 'orderby', 'type': 'OrderString'},
    }

    def __init__(self, image_id=None, image_digest=None, image_name=None, model_id=None, model_name=None, name=None, tag=None, count=None, compute_type=None, skip_token=None, tags=None, properties=None, run_id=None, expand=None, orderby="UpdatedAtDesc"):
        super(ListServicesRequest, self).__init__()
        self.image_id = image_id
        self.image_digest = image_digest
        self.image_name = image_name
        self.model_id = model_id
        self.model_name = model_name
        self.name = name
        self.tag = tag
        self.count = count
        self.compute_type = compute_type
        self.skip_token = skip_token
        self.tags = tags
        self.properties = properties
        self.run_id = run_id
        self.expand = expand
        self.orderby = orderby
