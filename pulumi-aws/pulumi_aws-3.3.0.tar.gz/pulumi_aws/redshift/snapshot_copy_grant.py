# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['SnapshotCopyGrant']


class SnapshotCopyGrant(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 snapshot_copy_grant_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Creates a snapshot copy grant that allows AWS Redshift to encrypt copied snapshots with a customer master key from AWS KMS in a destination region.

        Note that the grant must exist in the destination region, and not in the region of the cluster.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test_snapshot_copy_grant = aws.redshift.SnapshotCopyGrant("testSnapshotCopyGrant", snapshot_copy_grant_name="my-grant")
        test_cluster = aws.redshift.Cluster("testCluster", snapshot_copy=aws.redshift.ClusterSnapshotCopyArgs(
            destination_region="us-east-2",
            grant_name=test_snapshot_copy_grant.snapshot_copy_grant_name,
        ))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kms_key_id: The unique identifier for the customer master key (CMK) that the grant applies to. Specify the key ID or the Amazon Resource Name (ARN) of the CMK. To specify a CMK in a different AWS account, you must use the key ARN. If not specified, the default key is used.
        :param pulumi.Input[str] snapshot_copy_grant_name: A friendly name for identifying the grant.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
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

            __props__['kms_key_id'] = kms_key_id
            if snapshot_copy_grant_name is None:
                raise TypeError("Missing required property 'snapshot_copy_grant_name'")
            __props__['snapshot_copy_grant_name'] = snapshot_copy_grant_name
            __props__['tags'] = tags
            __props__['arn'] = None
        super(SnapshotCopyGrant, __self__).__init__(
            'aws:redshift/snapshotCopyGrant:SnapshotCopyGrant',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            snapshot_copy_grant_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'SnapshotCopyGrant':
        """
        Get an existing SnapshotCopyGrant resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of snapshot copy grant
        :param pulumi.Input[str] kms_key_id: The unique identifier for the customer master key (CMK) that the grant applies to. Specify the key ID or the Amazon Resource Name (ARN) of the CMK. To specify a CMK in a different AWS account, you must use the key ARN. If not specified, the default key is used.
        :param pulumi.Input[str] snapshot_copy_grant_name: A friendly name for identifying the grant.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["kms_key_id"] = kms_key_id
        __props__["snapshot_copy_grant_name"] = snapshot_copy_grant_name
        __props__["tags"] = tags
        return SnapshotCopyGrant(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of snapshot copy grant
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[str]:
        """
        The unique identifier for the customer master key (CMK) that the grant applies to. Specify the key ID or the Amazon Resource Name (ARN) of the CMK. To specify a CMK in a different AWS account, you must use the key ARN. If not specified, the default key is used.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="snapshotCopyGrantName")
    def snapshot_copy_grant_name(self) -> pulumi.Output[str]:
        """
        A friendly name for identifying the grant.
        """
        return pulumi.get(self, "snapshot_copy_grant_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

