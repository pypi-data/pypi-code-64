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

__all__ = ['IpSet']


class IpSet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ip_set_descriptors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpSetIpSetDescriptorArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a WAF Regional IPSet Resource for use with Application Load Balancer.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        ipset = aws.wafregional.IpSet("ipset", ip_set_descriptors=[
            aws.wafregional.IpSetIpSetDescriptorArgs(
                type="IPV4",
                value="192.0.7.0/24",
            ),
            aws.wafregional.IpSetIpSetDescriptorArgs(
                type="IPV4",
                value="10.16.16.0/16",
            ),
        ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpSetIpSetDescriptorArgs']]]] ip_set_descriptors: One or more pairs specifying the IP address type (IPV4 or IPV6) and the IP address range (in CIDR notation) from which web requests originate.
        :param pulumi.Input[str] name: The name or description of the IPSet.
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

            __props__['ip_set_descriptors'] = ip_set_descriptors
            __props__['name'] = name
            __props__['arn'] = None
        super(IpSet, __self__).__init__(
            'aws:wafregional/ipSet:IpSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            ip_set_descriptors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpSetIpSetDescriptorArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'IpSet':
        """
        Get an existing IpSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the WAF IPSet.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpSetIpSetDescriptorArgs']]]] ip_set_descriptors: One or more pairs specifying the IP address type (IPV4 or IPV6) and the IP address range (in CIDR notation) from which web requests originate.
        :param pulumi.Input[str] name: The name or description of the IPSet.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["ip_set_descriptors"] = ip_set_descriptors
        __props__["name"] = name
        return IpSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the WAF IPSet.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="ipSetDescriptors")
    def ip_set_descriptors(self) -> pulumi.Output[Optional[Sequence['outputs.IpSetIpSetDescriptor']]]:
        """
        One or more pairs specifying the IP address type (IPV4 or IPV6) and the IP address range (in CIDR notation) from which web requests originate.
        """
        return pulumi.get(self, "ip_set_descriptors")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name or description of the IPSet.
        """
        return pulumi.get(self, "name")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

