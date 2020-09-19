# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Application']


class Application(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 appversion_lifecycle: Optional[pulumi.Input[pulumi.InputType['ApplicationAppversionLifecycleArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an Elastic Beanstalk Application Resource. Elastic Beanstalk allows
        you to deploy and manage applications in the AWS cloud without worrying about
        the infrastructure that runs those applications.

        This resource creates an application that has one configuration template named
        `default`, and no application versions

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        tftest = aws.elasticbeanstalk.Application("tftest",
            description="tf-test-desc",
            appversion_lifecycle=aws.elasticbeanstalk.ApplicationAppversionLifecycleArgs(
                service_role=aws_iam_role["beanstalk_service"]["arn"],
                max_count=128,
                delete_source_from_s3=True,
            ))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Short description of the application
        :param pulumi.Input[str] name: The name of the application, must be unique within your account
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of tags for the Elastic Beanstalk Application.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['appversion_lifecycle'] = appversion_lifecycle
            __props__['description'] = description
            __props__['name'] = name
            __props__['tags'] = tags
            __props__['arn'] = None
        super(Application, __self__).__init__(
            'aws:elasticbeanstalk/application:Application',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            appversion_lifecycle: Optional[pulumi.Input[pulumi.InputType['ApplicationAppversionLifecycleArgs']]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Application':
        """
        Get an existing Application resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN assigned by AWS for this Elastic Beanstalk Application.
        :param pulumi.Input[str] description: Short description of the application
        :param pulumi.Input[str] name: The name of the application, must be unique within your account
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of tags for the Elastic Beanstalk Application.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["appversion_lifecycle"] = appversion_lifecycle
        __props__["arn"] = arn
        __props__["description"] = description
        __props__["name"] = name
        __props__["tags"] = tags
        return Application(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appversionLifecycle")
    def appversion_lifecycle(self) -> pulumi.Output[Optional['outputs.ApplicationAppversionLifecycle']]:
        return pulumi.get(self, "appversion_lifecycle")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN assigned by AWS for this Elastic Beanstalk Application.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Short description of the application
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the application, must be unique within your account
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of tags for the Elastic Beanstalk Application.
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

