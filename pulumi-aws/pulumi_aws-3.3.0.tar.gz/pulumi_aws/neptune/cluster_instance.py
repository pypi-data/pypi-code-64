# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['ClusterInstance']


class ClusterInstance(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 apply_immediately: Optional[pulumi.Input[bool]] = None,
                 auto_minor_version_upgrade: Optional[pulumi.Input[bool]] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 cluster_identifier: Optional[pulumi.Input[str]] = None,
                 engine: Optional[pulumi.Input[str]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 identifier_prefix: Optional[pulumi.Input[str]] = None,
                 instance_class: Optional[pulumi.Input[str]] = None,
                 neptune_parameter_group_name: Optional[pulumi.Input[str]] = None,
                 neptune_subnet_group_name: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 preferred_backup_window: Optional[pulumi.Input[str]] = None,
                 preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
                 promotion_tier: Optional[pulumi.Input[int]] = None,
                 publicly_accessible: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A Cluster Instance Resource defines attributes that are specific to a single instance in a Neptune Cluster.

        You can simply add neptune instances and Neptune manages the replication. You can use the [count](https://www.terraform.io/docs/configuration/resources.html#count)
        meta-parameter to make multiple instances and join them all to the same Neptune Cluster, or you may specify different Cluster Instance resources with various `instance_class` sizes.

        ## Example Usage

        The following example will create a neptune cluster with two neptune instances(one writer and one reader).

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.neptune.Cluster("default",
            cluster_identifier="neptune-cluster-demo",
            engine="neptune",
            backup_retention_period=5,
            preferred_backup_window="07:00-09:00",
            skip_final_snapshot=True,
            iam_database_authentication_enabled=True,
            apply_immediately=True)
        example = []
        for range in [{"value": i} for i in range(0, 2)]:
            example.append(aws.neptune.ClusterInstance(f"example-{range['value']}",
                cluster_identifier=default.id,
                engine="neptune",
                instance_class="db.r4.large",
                apply_immediately=True))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any instance modifications
               are applied immediately, or during the next maintenance window. Default is`false`.
        :param pulumi.Input[bool] auto_minor_version_upgrade: Indicates that minor engine upgrades will be applied automatically to the instance during the maintenance window. Default is `true`.
        :param pulumi.Input[str] availability_zone: The EC2 Availability Zone that the neptune instance is created in.
        :param pulumi.Input[str] cluster_identifier: The identifier of the `neptune.Cluster` in which to launch this instance.
        :param pulumi.Input[str] engine: The name of the database engine to be used for the neptune instance. Defaults to `neptune`. Valid Values: `neptune`.
        :param pulumi.Input[str] engine_version: The neptune engine version.
        :param pulumi.Input[str] identifier: The indentifier for the neptune instance, if omitted, this provider will assign a random, unique identifier.
        :param pulumi.Input[str] identifier_prefix: Creates a unique identifier beginning with the specified prefix. Conflicts with `identifier`.
        :param pulumi.Input[str] instance_class: The instance class to use.
        :param pulumi.Input[str] neptune_parameter_group_name: The name of the neptune parameter group to associate with this instance.
        :param pulumi.Input[str] neptune_subnet_group_name: A subnet group to associate with this neptune instance. **NOTE:** This must match the `neptune_subnet_group_name` of the attached `neptune.Cluster`.
        :param pulumi.Input[int] port: The port on which the DB accepts connections. Defaults to `8182`.
        :param pulumi.Input[str] preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled. Eg: "04:00-09:00"
        :param pulumi.Input[str] preferred_maintenance_window: The window to perform maintenance in.
               Syntax: "ddd:hh24:mi-ddd:hh24:mi". Eg: "Mon:00:00-Mon:03:00".
        :param pulumi.Input[int] promotion_tier: Default 0. Failover Priority setting on instance level. The reader who has lower tier has higher priority to get promoter to writer.
        :param pulumi.Input[bool] publicly_accessible: Bool to control if instance is publicly accessible. Default is `false`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the instance.
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

            __props__['apply_immediately'] = apply_immediately
            __props__['auto_minor_version_upgrade'] = auto_minor_version_upgrade
            __props__['availability_zone'] = availability_zone
            if cluster_identifier is None:
                raise TypeError("Missing required property 'cluster_identifier'")
            __props__['cluster_identifier'] = cluster_identifier
            __props__['engine'] = engine
            __props__['engine_version'] = engine_version
            __props__['identifier'] = identifier
            __props__['identifier_prefix'] = identifier_prefix
            if instance_class is None:
                raise TypeError("Missing required property 'instance_class'")
            __props__['instance_class'] = instance_class
            __props__['neptune_parameter_group_name'] = neptune_parameter_group_name
            __props__['neptune_subnet_group_name'] = neptune_subnet_group_name
            __props__['port'] = port
            __props__['preferred_backup_window'] = preferred_backup_window
            __props__['preferred_maintenance_window'] = preferred_maintenance_window
            __props__['promotion_tier'] = promotion_tier
            __props__['publicly_accessible'] = publicly_accessible
            __props__['tags'] = tags
            __props__['address'] = None
            __props__['arn'] = None
            __props__['dbi_resource_id'] = None
            __props__['endpoint'] = None
            __props__['kms_key_arn'] = None
            __props__['storage_encrypted'] = None
            __props__['writer'] = None
        super(ClusterInstance, __self__).__init__(
            'aws:neptune/clusterInstance:ClusterInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            address: Optional[pulumi.Input[str]] = None,
            apply_immediately: Optional[pulumi.Input[bool]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            auto_minor_version_upgrade: Optional[pulumi.Input[bool]] = None,
            availability_zone: Optional[pulumi.Input[str]] = None,
            cluster_identifier: Optional[pulumi.Input[str]] = None,
            dbi_resource_id: Optional[pulumi.Input[str]] = None,
            endpoint: Optional[pulumi.Input[str]] = None,
            engine: Optional[pulumi.Input[str]] = None,
            engine_version: Optional[pulumi.Input[str]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            identifier_prefix: Optional[pulumi.Input[str]] = None,
            instance_class: Optional[pulumi.Input[str]] = None,
            kms_key_arn: Optional[pulumi.Input[str]] = None,
            neptune_parameter_group_name: Optional[pulumi.Input[str]] = None,
            neptune_subnet_group_name: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[int]] = None,
            preferred_backup_window: Optional[pulumi.Input[str]] = None,
            preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
            promotion_tier: Optional[pulumi.Input[int]] = None,
            publicly_accessible: Optional[pulumi.Input[bool]] = None,
            storage_encrypted: Optional[pulumi.Input[bool]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            writer: Optional[pulumi.Input[bool]] = None) -> 'ClusterInstance':
        """
        Get an existing ClusterInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The hostname of the instance. See also `endpoint` and `port`.
        :param pulumi.Input[bool] apply_immediately: Specifies whether any instance modifications
               are applied immediately, or during the next maintenance window. Default is`false`.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of neptune instance
        :param pulumi.Input[bool] auto_minor_version_upgrade: Indicates that minor engine upgrades will be applied automatically to the instance during the maintenance window. Default is `true`.
        :param pulumi.Input[str] availability_zone: The EC2 Availability Zone that the neptune instance is created in.
        :param pulumi.Input[str] cluster_identifier: The identifier of the `neptune.Cluster` in which to launch this instance.
        :param pulumi.Input[str] dbi_resource_id: The region-unique, immutable identifier for the neptune instance.
        :param pulumi.Input[str] endpoint: The connection endpoint in `address:port` format.
        :param pulumi.Input[str] engine: The name of the database engine to be used for the neptune instance. Defaults to `neptune`. Valid Values: `neptune`.
        :param pulumi.Input[str] engine_version: The neptune engine version.
        :param pulumi.Input[str] identifier: The indentifier for the neptune instance, if omitted, this provider will assign a random, unique identifier.
        :param pulumi.Input[str] identifier_prefix: Creates a unique identifier beginning with the specified prefix. Conflicts with `identifier`.
        :param pulumi.Input[str] instance_class: The instance class to use.
        :param pulumi.Input[str] kms_key_arn: The ARN for the KMS encryption key if one is set to the neptune cluster.
        :param pulumi.Input[str] neptune_parameter_group_name: The name of the neptune parameter group to associate with this instance.
        :param pulumi.Input[str] neptune_subnet_group_name: A subnet group to associate with this neptune instance. **NOTE:** This must match the `neptune_subnet_group_name` of the attached `neptune.Cluster`.
        :param pulumi.Input[int] port: The port on which the DB accepts connections. Defaults to `8182`.
        :param pulumi.Input[str] preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled. Eg: "04:00-09:00"
        :param pulumi.Input[str] preferred_maintenance_window: The window to perform maintenance in.
               Syntax: "ddd:hh24:mi-ddd:hh24:mi". Eg: "Mon:00:00-Mon:03:00".
        :param pulumi.Input[int] promotion_tier: Default 0. Failover Priority setting on instance level. The reader who has lower tier has higher priority to get promoter to writer.
        :param pulumi.Input[bool] publicly_accessible: Bool to control if instance is publicly accessible. Default is `false`.
        :param pulumi.Input[bool] storage_encrypted: Specifies whether the neptune cluster is encrypted.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the instance.
        :param pulumi.Input[bool] writer: Boolean indicating if this instance is writable. `False` indicates this instance is a read replica.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["address"] = address
        __props__["apply_immediately"] = apply_immediately
        __props__["arn"] = arn
        __props__["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        __props__["availability_zone"] = availability_zone
        __props__["cluster_identifier"] = cluster_identifier
        __props__["dbi_resource_id"] = dbi_resource_id
        __props__["endpoint"] = endpoint
        __props__["engine"] = engine
        __props__["engine_version"] = engine_version
        __props__["identifier"] = identifier
        __props__["identifier_prefix"] = identifier_prefix
        __props__["instance_class"] = instance_class
        __props__["kms_key_arn"] = kms_key_arn
        __props__["neptune_parameter_group_name"] = neptune_parameter_group_name
        __props__["neptune_subnet_group_name"] = neptune_subnet_group_name
        __props__["port"] = port
        __props__["preferred_backup_window"] = preferred_backup_window
        __props__["preferred_maintenance_window"] = preferred_maintenance_window
        __props__["promotion_tier"] = promotion_tier
        __props__["publicly_accessible"] = publicly_accessible
        __props__["storage_encrypted"] = storage_encrypted
        __props__["tags"] = tags
        __props__["writer"] = writer
        return ClusterInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Output[str]:
        """
        The hostname of the instance. See also `endpoint` and `port`.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="applyImmediately")
    def apply_immediately(self) -> pulumi.Output[bool]:
        """
        Specifies whether any instance modifications
        are applied immediately, or during the next maintenance window. Default is`false`.
        """
        return pulumi.get(self, "apply_immediately")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of neptune instance
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates that minor engine upgrades will be applied automatically to the instance during the maintenance window. Default is `true`.
        """
        return pulumi.get(self, "auto_minor_version_upgrade")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> pulumi.Output[str]:
        """
        The EC2 Availability Zone that the neptune instance is created in.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> pulumi.Output[str]:
        """
        The identifier of the `neptune.Cluster` in which to launch this instance.
        """
        return pulumi.get(self, "cluster_identifier")

    @property
    @pulumi.getter(name="dbiResourceId")
    def dbi_resource_id(self) -> pulumi.Output[str]:
        """
        The region-unique, immutable identifier for the neptune instance.
        """
        return pulumi.get(self, "dbi_resource_id")

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Output[str]:
        """
        The connection endpoint in `address:port` format.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def engine(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the database engine to be used for the neptune instance. Defaults to `neptune`. Valid Values: `neptune`.
        """
        return pulumi.get(self, "engine")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> pulumi.Output[str]:
        """
        The neptune engine version.
        """
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        The indentifier for the neptune instance, if omitted, this provider will assign a random, unique identifier.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="identifierPrefix")
    def identifier_prefix(self) -> pulumi.Output[str]:
        """
        Creates a unique identifier beginning with the specified prefix. Conflicts with `identifier`.
        """
        return pulumi.get(self, "identifier_prefix")

    @property
    @pulumi.getter(name="instanceClass")
    def instance_class(self) -> pulumi.Output[str]:
        """
        The instance class to use.
        """
        return pulumi.get(self, "instance_class")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> pulumi.Output[str]:
        """
        The ARN for the KMS encryption key if one is set to the neptune cluster.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter(name="neptuneParameterGroupName")
    def neptune_parameter_group_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the neptune parameter group to associate with this instance.
        """
        return pulumi.get(self, "neptune_parameter_group_name")

    @property
    @pulumi.getter(name="neptuneSubnetGroupName")
    def neptune_subnet_group_name(self) -> pulumi.Output[str]:
        """
        A subnet group to associate with this neptune instance. **NOTE:** This must match the `neptune_subnet_group_name` of the attached `neptune.Cluster`.
        """
        return pulumi.get(self, "neptune_subnet_group_name")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        """
        The port on which the DB accepts connections. Defaults to `8182`.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="preferredBackupWindow")
    def preferred_backup_window(self) -> pulumi.Output[str]:
        """
        The daily time range during which automated backups are created if automated backups are enabled. Eg: "04:00-09:00"
        """
        return pulumi.get(self, "preferred_backup_window")

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> pulumi.Output[str]:
        """
        The window to perform maintenance in.
        Syntax: "ddd:hh24:mi-ddd:hh24:mi". Eg: "Mon:00:00-Mon:03:00".
        """
        return pulumi.get(self, "preferred_maintenance_window")

    @property
    @pulumi.getter(name="promotionTier")
    def promotion_tier(self) -> pulumi.Output[Optional[int]]:
        """
        Default 0. Failover Priority setting on instance level. The reader who has lower tier has higher priority to get promoter to writer.
        """
        return pulumi.get(self, "promotion_tier")

    @property
    @pulumi.getter(name="publiclyAccessible")
    def publicly_accessible(self) -> pulumi.Output[Optional[bool]]:
        """
        Bool to control if instance is publicly accessible. Default is `false`.
        """
        return pulumi.get(self, "publicly_accessible")

    @property
    @pulumi.getter(name="storageEncrypted")
    def storage_encrypted(self) -> pulumi.Output[bool]:
        """
        Specifies whether the neptune cluster is encrypted.
        """
        return pulumi.get(self, "storage_encrypted")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the instance.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def writer(self) -> pulumi.Output[bool]:
        """
        Boolean indicating if this instance is writable. `False` indicates this instance is a read replica.
        """
        return pulumi.get(self, "writer")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

