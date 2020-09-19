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

__all__ = ['Record']


class Record(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aliases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordAliasArgs']]]]] = None,
                 allow_overwrite: Optional[pulumi.Input[bool]] = None,
                 failover_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordFailoverRoutingPolicyArgs']]]]] = None,
                 geolocation_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordGeolocationRoutingPolicyArgs']]]]] = None,
                 health_check_id: Optional[pulumi.Input[str]] = None,
                 latency_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordLatencyRoutingPolicyArgs']]]]] = None,
                 multivalue_answer_routing_policy: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 records: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 set_identifier: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 weighted_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordWeightedRoutingPolicyArgs']]]]] = None,
                 zone_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a Route53 record resource.

        ## Example Usage
        ### Simple routing policy

        ```python
        import pulumi
        import pulumi_aws as aws

        www = aws.route53.Record("www",
            zone_id=aws_route53_zone["primary"]["zone_id"],
            name="www.example.com",
            type="A",
            ttl=300,
            records=[aws_eip["lb"]["public_ip"]])
        ```
        ### Weighted routing policy
        Other routing policies are configured similarly. See [AWS Route53 Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html) for details.

        ```python
        import pulumi
        import pulumi_aws as aws

        www_dev = aws.route53.Record("www-dev",
            zone_id=aws_route53_zone["primary"]["zone_id"],
            name="www",
            type="CNAME",
            ttl=5,
            weighted_routing_policies=[aws.route53.RecordWeightedRoutingPolicyArgs(
                weight=10,
            )],
            set_identifier="dev",
            records=["dev.example.com"])
        www_live = aws.route53.Record("www-live",
            zone_id=aws_route53_zone["primary"]["zone_id"],
            name="www",
            type="CNAME",
            ttl=5,
            weighted_routing_policies=[aws.route53.RecordWeightedRoutingPolicyArgs(
                weight=90,
            )],
            set_identifier="live",
            records=["live.example.com"])
        ```
        ### Alias record
        See [related part of AWS Route53 Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)
        to understand differences between alias and non-alias records.

        TTL for all alias records is [60 seconds](https://aws.amazon.com/route53/faqs/#dns_failover_do_i_need_to_adjust),
        you cannot change this, therefore `ttl` has to be omitted in alias records.

        ```python
        import pulumi
        import pulumi_aws as aws

        main = aws.elb.LoadBalancer("main",
            availability_zones=["us-east-1c"],
            listeners=[aws.elb.LoadBalancerListenerArgs(
                instance_port=80,
                instance_protocol="http",
                lb_port=80,
                lb_protocol="http",
            )])
        www = aws.route53.Record("www",
            zone_id=aws_route53_zone["primary"]["zone_id"],
            name="example.com",
            type="A",
            aliases=[aws.route53.RecordAliasArgs(
                name=main.dns_name,
                zone_id=main.zone_id,
                evaluate_target_health=True,
            )])
        ```
        ### NS and SOA Record Management

        When creating Route 53 zones, the `NS` and `SOA` records for the zone are automatically created. Enabling the `allow_overwrite` argument will allow managing these records in a single deployment without the requirement for `import`.

        ```python
        import pulumi
        import pulumi_aws as aws

        example_zone = aws.route53.Zone("exampleZone")
        example_record = aws.route53.Record("exampleRecord",
            allow_overwrite=True,
            name="test.example.com",
            ttl=30,
            type="NS",
            zone_id=example_zone.zone_id,
            records=[
                example_zone.name_servers[0],
                example_zone.name_servers[1],
                example_zone.name_servers[2],
                example_zone.name_servers[3],
            ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordAliasArgs']]]] aliases: An alias block. Conflicts with `ttl` & `records`.
               Alias record documented below.
        :param pulumi.Input[bool] allow_overwrite: Allow creation of this record to overwrite an existing record, if any. This does not affect the ability to update the record using this provider and does not prevent other resources within this provider or manual Route 53 changes outside this provider from overwriting this record. `false` by default. This configuration is not recommended for most environments.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordFailoverRoutingPolicyArgs']]]] failover_routing_policies: A block indicating the routing behavior when associated health check fails. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordGeolocationRoutingPolicyArgs']]]] geolocation_routing_policies: A block indicating a routing policy based on the geolocation of the requestor. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[str] health_check_id: The health check the record should be associated with.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordLatencyRoutingPolicyArgs']]]] latency_routing_policies: A block indicating a routing policy based on the latency between the requestor and an AWS region. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[bool] multivalue_answer_routing_policy: Set to `true` to indicate a multivalue answer routing policy. Conflicts with any other routing policy.
        :param pulumi.Input[str] name: DNS domain name for a CloudFront distribution, S3 bucket, ELB, or another resource record set in this hosted zone.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] records: A string list of records. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add `\"\"` inside the configuration string (e.g. `"first255characters\"\"morecharacters"`).
        :param pulumi.Input[str] set_identifier: Unique identifier to differentiate records with routing policies from one another. Required if using `failover`, `geolocation`, `latency`, or `weighted` routing policies documented below.
        :param pulumi.Input[int] ttl: The TTL of the record.
        :param pulumi.Input[str] type: `PRIMARY` or `SECONDARY`. A `PRIMARY` record will be served if its healthcheck is passing, otherwise the `SECONDARY` will be served. See http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring-options.html#dns-failover-failover-rrsets
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordWeightedRoutingPolicyArgs']]]] weighted_routing_policies: A block indicating a weighted routing policy. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[str] zone_id: Hosted zone ID for a CloudFront distribution, S3 bucket, ELB, or Route 53 hosted zone. See `resource_elb.zone_id` for example.
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

            __props__['aliases'] = aliases
            __props__['allow_overwrite'] = allow_overwrite
            __props__['failover_routing_policies'] = failover_routing_policies
            __props__['geolocation_routing_policies'] = geolocation_routing_policies
            __props__['health_check_id'] = health_check_id
            __props__['latency_routing_policies'] = latency_routing_policies
            __props__['multivalue_answer_routing_policy'] = multivalue_answer_routing_policy
            if name is None:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['records'] = records
            __props__['set_identifier'] = set_identifier
            __props__['ttl'] = ttl
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            __props__['weighted_routing_policies'] = weighted_routing_policies
            if zone_id is None:
                raise TypeError("Missing required property 'zone_id'")
            __props__['zone_id'] = zone_id
            __props__['fqdn'] = None
        super(Record, __self__).__init__(
            'aws:route53/record:Record',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            aliases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordAliasArgs']]]]] = None,
            allow_overwrite: Optional[pulumi.Input[bool]] = None,
            failover_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordFailoverRoutingPolicyArgs']]]]] = None,
            fqdn: Optional[pulumi.Input[str]] = None,
            geolocation_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordGeolocationRoutingPolicyArgs']]]]] = None,
            health_check_id: Optional[pulumi.Input[str]] = None,
            latency_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordLatencyRoutingPolicyArgs']]]]] = None,
            multivalue_answer_routing_policy: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            records: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            set_identifier: Optional[pulumi.Input[str]] = None,
            ttl: Optional[pulumi.Input[int]] = None,
            type: Optional[pulumi.Input[str]] = None,
            weighted_routing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordWeightedRoutingPolicyArgs']]]]] = None,
            zone_id: Optional[pulumi.Input[str]] = None) -> 'Record':
        """
        Get an existing Record resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordAliasArgs']]]] aliases: An alias block. Conflicts with `ttl` & `records`.
               Alias record documented below.
        :param pulumi.Input[bool] allow_overwrite: Allow creation of this record to overwrite an existing record, if any. This does not affect the ability to update the record using this provider and does not prevent other resources within this provider or manual Route 53 changes outside this provider from overwriting this record. `false` by default. This configuration is not recommended for most environments.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordFailoverRoutingPolicyArgs']]]] failover_routing_policies: A block indicating the routing behavior when associated health check fails. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[str] fqdn: [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) built using the zone domain and `name`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordGeolocationRoutingPolicyArgs']]]] geolocation_routing_policies: A block indicating a routing policy based on the geolocation of the requestor. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[str] health_check_id: The health check the record should be associated with.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordLatencyRoutingPolicyArgs']]]] latency_routing_policies: A block indicating a routing policy based on the latency between the requestor and an AWS region. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[bool] multivalue_answer_routing_policy: Set to `true` to indicate a multivalue answer routing policy. Conflicts with any other routing policy.
        :param pulumi.Input[str] name: DNS domain name for a CloudFront distribution, S3 bucket, ELB, or another resource record set in this hosted zone.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] records: A string list of records. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add `\"\"` inside the configuration string (e.g. `"first255characters\"\"morecharacters"`).
        :param pulumi.Input[str] set_identifier: Unique identifier to differentiate records with routing policies from one another. Required if using `failover`, `geolocation`, `latency`, or `weighted` routing policies documented below.
        :param pulumi.Input[int] ttl: The TTL of the record.
        :param pulumi.Input[str] type: `PRIMARY` or `SECONDARY`. A `PRIMARY` record will be served if its healthcheck is passing, otherwise the `SECONDARY` will be served. See http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring-options.html#dns-failover-failover-rrsets
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RecordWeightedRoutingPolicyArgs']]]] weighted_routing_policies: A block indicating a weighted routing policy. Conflicts with any other routing policy. Documented below.
        :param pulumi.Input[str] zone_id: Hosted zone ID for a CloudFront distribution, S3 bucket, ELB, or Route 53 hosted zone. See `resource_elb.zone_id` for example.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["aliases"] = aliases
        __props__["allow_overwrite"] = allow_overwrite
        __props__["failover_routing_policies"] = failover_routing_policies
        __props__["fqdn"] = fqdn
        __props__["geolocation_routing_policies"] = geolocation_routing_policies
        __props__["health_check_id"] = health_check_id
        __props__["latency_routing_policies"] = latency_routing_policies
        __props__["multivalue_answer_routing_policy"] = multivalue_answer_routing_policy
        __props__["name"] = name
        __props__["records"] = records
        __props__["set_identifier"] = set_identifier
        __props__["ttl"] = ttl
        __props__["type"] = type
        __props__["weighted_routing_policies"] = weighted_routing_policies
        __props__["zone_id"] = zone_id
        return Record(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def aliases(self) -> pulumi.Output[Optional[Sequence['outputs.RecordAlias']]]:
        """
        An alias block. Conflicts with `ttl` & `records`.
        Alias record documented below.
        """
        return pulumi.get(self, "aliases")

    @property
    @pulumi.getter(name="allowOverwrite")
    def allow_overwrite(self) -> pulumi.Output[bool]:
        """
        Allow creation of this record to overwrite an existing record, if any. This does not affect the ability to update the record using this provider and does not prevent other resources within this provider or manual Route 53 changes outside this provider from overwriting this record. `false` by default. This configuration is not recommended for most environments.
        """
        return pulumi.get(self, "allow_overwrite")

    @property
    @pulumi.getter(name="failoverRoutingPolicies")
    def failover_routing_policies(self) -> pulumi.Output[Optional[Sequence['outputs.RecordFailoverRoutingPolicy']]]:
        """
        A block indicating the routing behavior when associated health check fails. Conflicts with any other routing policy. Documented below.
        """
        return pulumi.get(self, "failover_routing_policies")

    @property
    @pulumi.getter
    def fqdn(self) -> pulumi.Output[str]:
        """
        [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name) built using the zone domain and `name`.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="geolocationRoutingPolicies")
    def geolocation_routing_policies(self) -> pulumi.Output[Optional[Sequence['outputs.RecordGeolocationRoutingPolicy']]]:
        """
        A block indicating a routing policy based on the geolocation of the requestor. Conflicts with any other routing policy. Documented below.
        """
        return pulumi.get(self, "geolocation_routing_policies")

    @property
    @pulumi.getter(name="healthCheckId")
    def health_check_id(self) -> pulumi.Output[Optional[str]]:
        """
        The health check the record should be associated with.
        """
        return pulumi.get(self, "health_check_id")

    @property
    @pulumi.getter(name="latencyRoutingPolicies")
    def latency_routing_policies(self) -> pulumi.Output[Optional[Sequence['outputs.RecordLatencyRoutingPolicy']]]:
        """
        A block indicating a routing policy based on the latency between the requestor and an AWS region. Conflicts with any other routing policy. Documented below.
        """
        return pulumi.get(self, "latency_routing_policies")

    @property
    @pulumi.getter(name="multivalueAnswerRoutingPolicy")
    def multivalue_answer_routing_policy(self) -> pulumi.Output[Optional[bool]]:
        """
        Set to `true` to indicate a multivalue answer routing policy. Conflicts with any other routing policy.
        """
        return pulumi.get(self, "multivalue_answer_routing_policy")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        DNS domain name for a CloudFront distribution, S3 bucket, ELB, or another resource record set in this hosted zone.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def records(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A string list of records. To specify a single record value longer than 255 characters such as a TXT record for DKIM, add `\"\"` inside the configuration string (e.g. `"first255characters\"\"morecharacters"`).
        """
        return pulumi.get(self, "records")

    @property
    @pulumi.getter(name="setIdentifier")
    def set_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        Unique identifier to differentiate records with routing policies from one another. Required if using `failover`, `geolocation`, `latency`, or `weighted` routing policies documented below.
        """
        return pulumi.get(self, "set_identifier")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional[int]]:
        """
        The TTL of the record.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        `PRIMARY` or `SECONDARY`. A `PRIMARY` record will be served if its healthcheck is passing, otherwise the `SECONDARY` will be served. See http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring-options.html#dns-failover-failover-rrsets
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="weightedRoutingPolicies")
    def weighted_routing_policies(self) -> pulumi.Output[Optional[Sequence['outputs.RecordWeightedRoutingPolicy']]]:
        """
        A block indicating a weighted routing policy. Conflicts with any other routing policy. Documented below.
        """
        return pulumi.get(self, "weighted_routing_policies")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Output[str]:
        """
        Hosted zone ID for a CloudFront distribution, S3 bucket, ELB, or Route 53 hosted zone. See `resource_elb.zone_id` for example.
        """
        return pulumi.get(self, "zone_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

