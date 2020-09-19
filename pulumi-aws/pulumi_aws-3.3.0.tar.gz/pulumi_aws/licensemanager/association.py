# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Association']


class Association(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 license_configuration_arn: Optional[pulumi.Input[str]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a License Manager association.

        > **Note:** License configurations can also be associated with launch templates by specifying the `license_specifications` block for an `ec2.LaunchTemplate`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] license_configuration_arn: ARN of the license configuration.
        :param pulumi.Input[str] resource_arn: ARN of the resource associated with the license configuration.
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

            if license_configuration_arn is None:
                raise TypeError("Missing required property 'license_configuration_arn'")
            __props__['license_configuration_arn'] = license_configuration_arn
            if resource_arn is None:
                raise TypeError("Missing required property 'resource_arn'")
            __props__['resource_arn'] = resource_arn
        super(Association, __self__).__init__(
            'aws:licensemanager/association:Association',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            license_configuration_arn: Optional[pulumi.Input[str]] = None,
            resource_arn: Optional[pulumi.Input[str]] = None) -> 'Association':
        """
        Get an existing Association resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] license_configuration_arn: ARN of the license configuration.
        :param pulumi.Input[str] resource_arn: ARN of the resource associated with the license configuration.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["license_configuration_arn"] = license_configuration_arn
        __props__["resource_arn"] = resource_arn
        return Association(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="licenseConfigurationArn")
    def license_configuration_arn(self) -> pulumi.Output[str]:
        """
        ARN of the license configuration.
        """
        return pulumi.get(self, "license_configuration_arn")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> pulumi.Output[str]:
        """
        ARN of the resource associated with the license configuration.
        """
        return pulumi.get(self, "resource_arn")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

