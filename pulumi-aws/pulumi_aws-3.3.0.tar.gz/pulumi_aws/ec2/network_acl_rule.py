# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['NetworkAclRule']


class NetworkAclRule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 egress: Optional[pulumi.Input[bool]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 icmp_code: Optional[pulumi.Input[str]] = None,
                 icmp_type: Optional[pulumi.Input[str]] = None,
                 ipv6_cidr_block: Optional[pulumi.Input[str]] = None,
                 network_acl_id: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 rule_action: Optional[pulumi.Input[str]] = None,
                 rule_number: Optional[pulumi.Input[int]] = None,
                 to_port: Optional[pulumi.Input[int]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Creates an entry (a rule) in a network ACL with the specified rule number.

        > **NOTE on Network ACLs and Network ACL Rules:** This provider currently
        provides both a standalone Network ACL Rule resource and a Network ACL resource with rules
        defined in-line. At this time you cannot use a Network ACL with in-line rules
        in conjunction with any Network ACL Rule resources. Doing so will cause
        a conflict of rule settings and will overwrite rules.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        bar_network_acl = aws.ec2.NetworkAcl("barNetworkAcl", vpc_id=aws_vpc["foo"]["id"])
        bar_network_acl_rule = aws.ec2.NetworkAclRule("barNetworkAclRule",
            network_acl_id=bar_network_acl.id,
            rule_number=200,
            egress=False,
            protocol="tcp",
            rule_action="allow",
            cidr_block=aws_vpc["foo"]["cidr_block"],
            from_port=22,
            to_port=22)
        ```

        > **Note:** One of either `cidr_block` or `ipv6_cidr_block` is required.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The network range to allow or deny, in CIDR notation (for example 172.16.0.0/24 ).
        :param pulumi.Input[bool] egress: Indicates whether this is an egress rule (rule is applied to traffic leaving the subnet). Default `false`.
        :param pulumi.Input[int] from_port: The from port to match.
        :param pulumi.Input[str] icmp_code: ICMP protocol: The ICMP code. Required if specifying ICMP for the protocol. e.g. -1
        :param pulumi.Input[str] icmp_type: ICMP protocol: The ICMP type. Required if specifying ICMP for the protocol. e.g. -1
        :param pulumi.Input[str] ipv6_cidr_block: The IPv6 CIDR block to allow or deny.
        :param pulumi.Input[str] network_acl_id: The ID of the network ACL.
        :param pulumi.Input[str] protocol: The protocol. A value of -1 means all protocols.
        :param pulumi.Input[str] rule_action: Indicates whether to allow or deny the traffic that matches the rule. Accepted values: `allow` | `deny`
        :param pulumi.Input[int] rule_number: The rule number for the entry (for example, 100). ACL entries are processed in ascending order by rule number.
        :param pulumi.Input[int] to_port: The to port to match.
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

            __props__['cidr_block'] = cidr_block
            __props__['egress'] = egress
            __props__['from_port'] = from_port
            __props__['icmp_code'] = icmp_code
            __props__['icmp_type'] = icmp_type
            __props__['ipv6_cidr_block'] = ipv6_cidr_block
            if network_acl_id is None:
                raise TypeError("Missing required property 'network_acl_id'")
            __props__['network_acl_id'] = network_acl_id
            if protocol is None:
                raise TypeError("Missing required property 'protocol'")
            __props__['protocol'] = protocol
            if rule_action is None:
                raise TypeError("Missing required property 'rule_action'")
            __props__['rule_action'] = rule_action
            if rule_number is None:
                raise TypeError("Missing required property 'rule_number'")
            __props__['rule_number'] = rule_number
            __props__['to_port'] = to_port
        super(NetworkAclRule, __self__).__init__(
            'aws:ec2/networkAclRule:NetworkAclRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cidr_block: Optional[pulumi.Input[str]] = None,
            egress: Optional[pulumi.Input[bool]] = None,
            from_port: Optional[pulumi.Input[int]] = None,
            icmp_code: Optional[pulumi.Input[str]] = None,
            icmp_type: Optional[pulumi.Input[str]] = None,
            ipv6_cidr_block: Optional[pulumi.Input[str]] = None,
            network_acl_id: Optional[pulumi.Input[str]] = None,
            protocol: Optional[pulumi.Input[str]] = None,
            rule_action: Optional[pulumi.Input[str]] = None,
            rule_number: Optional[pulumi.Input[int]] = None,
            to_port: Optional[pulumi.Input[int]] = None) -> 'NetworkAclRule':
        """
        Get an existing NetworkAclRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The network range to allow or deny, in CIDR notation (for example 172.16.0.0/24 ).
        :param pulumi.Input[bool] egress: Indicates whether this is an egress rule (rule is applied to traffic leaving the subnet). Default `false`.
        :param pulumi.Input[int] from_port: The from port to match.
        :param pulumi.Input[str] icmp_code: ICMP protocol: The ICMP code. Required if specifying ICMP for the protocol. e.g. -1
        :param pulumi.Input[str] icmp_type: ICMP protocol: The ICMP type. Required if specifying ICMP for the protocol. e.g. -1
        :param pulumi.Input[str] ipv6_cidr_block: The IPv6 CIDR block to allow or deny.
        :param pulumi.Input[str] network_acl_id: The ID of the network ACL.
        :param pulumi.Input[str] protocol: The protocol. A value of -1 means all protocols.
        :param pulumi.Input[str] rule_action: Indicates whether to allow or deny the traffic that matches the rule. Accepted values: `allow` | `deny`
        :param pulumi.Input[int] rule_number: The rule number for the entry (for example, 100). ACL entries are processed in ascending order by rule number.
        :param pulumi.Input[int] to_port: The to port to match.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["cidr_block"] = cidr_block
        __props__["egress"] = egress
        __props__["from_port"] = from_port
        __props__["icmp_code"] = icmp_code
        __props__["icmp_type"] = icmp_type
        __props__["ipv6_cidr_block"] = ipv6_cidr_block
        __props__["network_acl_id"] = network_acl_id
        __props__["protocol"] = protocol
        __props__["rule_action"] = rule_action
        __props__["rule_number"] = rule_number
        __props__["to_port"] = to_port
        return NetworkAclRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Output[Optional[str]]:
        """
        The network range to allow or deny, in CIDR notation (for example 172.16.0.0/24 ).
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter
    def egress(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether this is an egress rule (rule is applied to traffic leaving the subnet). Default `false`.
        """
        return pulumi.get(self, "egress")

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> pulumi.Output[Optional[int]]:
        """
        The from port to match.
        """
        return pulumi.get(self, "from_port")

    @property
    @pulumi.getter(name="icmpCode")
    def icmp_code(self) -> pulumi.Output[Optional[str]]:
        """
        ICMP protocol: The ICMP code. Required if specifying ICMP for the protocol. e.g. -1
        """
        return pulumi.get(self, "icmp_code")

    @property
    @pulumi.getter(name="icmpType")
    def icmp_type(self) -> pulumi.Output[Optional[str]]:
        """
        ICMP protocol: The ICMP type. Required if specifying ICMP for the protocol. e.g. -1
        """
        return pulumi.get(self, "icmp_type")

    @property
    @pulumi.getter(name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> pulumi.Output[Optional[str]]:
        """
        The IPv6 CIDR block to allow or deny.
        """
        return pulumi.get(self, "ipv6_cidr_block")

    @property
    @pulumi.getter(name="networkAclId")
    def network_acl_id(self) -> pulumi.Output[str]:
        """
        The ID of the network ACL.
        """
        return pulumi.get(self, "network_acl_id")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        The protocol. A value of -1 means all protocols.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="ruleAction")
    def rule_action(self) -> pulumi.Output[str]:
        """
        Indicates whether to allow or deny the traffic that matches the rule. Accepted values: `allow` | `deny`
        """
        return pulumi.get(self, "rule_action")

    @property
    @pulumi.getter(name="ruleNumber")
    def rule_number(self) -> pulumi.Output[int]:
        """
        The rule number for the entry (for example, 100). ACL entries are processed in ascending order by rule number.
        """
        return pulumi.get(self, "rule_number")

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> pulumi.Output[Optional[int]]:
        """
        The to port to match.
        """
        return pulumi.get(self, "to_port")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

