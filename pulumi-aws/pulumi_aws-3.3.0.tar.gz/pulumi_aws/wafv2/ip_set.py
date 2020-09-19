# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['IpSet']


class IpSet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ip_address_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a WAFv2 IP Set Resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.wafv2.IpSet("example",
            addresses=[
                "1.2.3.4/32",
                "5.6.7.8/32",
            ],
            description="Example IP set",
            ip_address_version="IPV4",
            scope="REGIONAL",
            tags={
                "Tag1": "Value1",
                "Tag2": "Value2",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] addresses: Contains an array of strings that specify one or more IP addresses or blocks of IP addresses in Classless Inter-Domain Routing (CIDR) notation. AWS WAF supports all address ranges for IP versions IPv4 and IPv6.
        :param pulumi.Input[str] description: A friendly description of the IP set.
        :param pulumi.Input[str] ip_address_version: Specify IPV4 or IPV6. Valid values are `IPV4` or `IPV6`.
        :param pulumi.Input[str] name: A friendly name of the IP set.
        :param pulumi.Input[str] scope: Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the Region US East (N. Virginia).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: An array of key:value pairs to associate with the resource.
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

            __props__['addresses'] = addresses
            __props__['description'] = description
            if ip_address_version is None:
                raise TypeError("Missing required property 'ip_address_version'")
            __props__['ip_address_version'] = ip_address_version
            __props__['name'] = name
            if scope is None:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['lock_token'] = None
        super(IpSet, __self__).__init__(
            'aws:wafv2/ipSet:IpSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            ip_address_version: Optional[pulumi.Input[str]] = None,
            lock_token: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            scope: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'IpSet':
        """
        Get an existing IpSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] addresses: Contains an array of strings that specify one or more IP addresses or blocks of IP addresses in Classless Inter-Domain Routing (CIDR) notation. AWS WAF supports all address ranges for IP versions IPv4 and IPv6.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) that identifies the cluster.
        :param pulumi.Input[str] description: A friendly description of the IP set.
        :param pulumi.Input[str] ip_address_version: Specify IPV4 or IPV6. Valid values are `IPV4` or `IPV6`.
        :param pulumi.Input[str] name: A friendly name of the IP set.
        :param pulumi.Input[str] scope: Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the Region US East (N. Virginia).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: An array of key:value pairs to associate with the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["addresses"] = addresses
        __props__["arn"] = arn
        __props__["description"] = description
        __props__["ip_address_version"] = ip_address_version
        __props__["lock_token"] = lock_token
        __props__["name"] = name
        __props__["scope"] = scope
        __props__["tags"] = tags
        return IpSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def addresses(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Contains an array of strings that specify one or more IP addresses or blocks of IP addresses in Classless Inter-Domain Routing (CIDR) notation. AWS WAF supports all address ranges for IP versions IPv4 and IPv6.
        """
        return pulumi.get(self, "addresses")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) that identifies the cluster.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A friendly description of the IP set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="ipAddressVersion")
    def ip_address_version(self) -> pulumi.Output[str]:
        """
        Specify IPV4 or IPV6. Valid values are `IPV4` or `IPV6`.
        """
        return pulumi.get(self, "ip_address_version")

    @property
    @pulumi.getter(name="lockToken")
    def lock_token(self) -> pulumi.Output[str]:
        return pulumi.get(self, "lock_token")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A friendly name of the IP set.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[str]:
        """
        Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the Region US East (N. Virginia).
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        An array of key:value pairs to associate with the resource.
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

