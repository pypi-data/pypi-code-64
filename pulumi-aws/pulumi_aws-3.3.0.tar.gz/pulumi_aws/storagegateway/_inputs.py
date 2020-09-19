# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'GatewaySmbActiveDirectorySettingsArgs',
    'NfsFileShareCacheAttributesArgs',
    'NfsFileShareNfsFileShareDefaultsArgs',
    'SmbFileShareCacheAttributesArgs',
]

@pulumi.input_type
class GatewaySmbActiveDirectorySettingsArgs:
    def __init__(__self__, *,
                 domain_name: pulumi.Input[str],
                 password: pulumi.Input[str],
                 username: pulumi.Input[str]):
        """
        :param pulumi.Input[str] domain_name: The name of the domain that you want the gateway to join.
        :param pulumi.Input[str] password: The password of the user who has permission to add the gateway to the Active Directory domain.
        :param pulumi.Input[str] username: The user name of user who has permission to add the gateway to the Active Directory domain.
        """
        pulumi.set(__self__, "domain_name", domain_name)
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Input[str]:
        """
        The name of the domain that you want the gateway to join.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        The password of the user who has permission to add the gateway to the Active Directory domain.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The user name of user who has permission to add the gateway to the Active Directory domain.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class NfsFileShareCacheAttributesArgs:
    def __init__(__self__, *,
                 cache_stale_timeout_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] cache_stale_timeout_in_seconds: Refreshes a file share's cache by using Time To Live (TTL).
               TTL is the length of time since the last refresh after which access to the directory would cause the file gateway
               to first refresh that directory's contents from the Amazon S3 bucket. Valid Values: 300 to 2,592,000 seconds (5 minutes to 30 days)
        """
        if cache_stale_timeout_in_seconds is not None:
            pulumi.set(__self__, "cache_stale_timeout_in_seconds", cache_stale_timeout_in_seconds)

    @property
    @pulumi.getter(name="cacheStaleTimeoutInSeconds")
    def cache_stale_timeout_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Refreshes a file share's cache by using Time To Live (TTL).
        TTL is the length of time since the last refresh after which access to the directory would cause the file gateway
        to first refresh that directory's contents from the Amazon S3 bucket. Valid Values: 300 to 2,592,000 seconds (5 minutes to 30 days)
        """
        return pulumi.get(self, "cache_stale_timeout_in_seconds")

    @cache_stale_timeout_in_seconds.setter
    def cache_stale_timeout_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cache_stale_timeout_in_seconds", value)


@pulumi.input_type
class NfsFileShareNfsFileShareDefaultsArgs:
    def __init__(__self__, *,
                 directory_mode: Optional[pulumi.Input[str]] = None,
                 file_mode: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[int]] = None,
                 owner_id: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] directory_mode: The Unix directory mode in the string form "nnnn". Defaults to `"0777"`.
        :param pulumi.Input[str] file_mode: The Unix file mode in the string form "nnnn". Defaults to `"0666"`.
        :param pulumi.Input[int] group_id: The default group ID for the file share (unless the files have another group ID specified). Defaults to `65534` (`nfsnobody`). Valid values: `0` through `4294967294`.
        :param pulumi.Input[int] owner_id: The default owner ID for the file share (unless the files have another owner ID specified). Defaults to `65534` (`nfsnobody`). Valid values: `0` through `4294967294`.
        """
        if directory_mode is not None:
            pulumi.set(__self__, "directory_mode", directory_mode)
        if file_mode is not None:
            pulumi.set(__self__, "file_mode", file_mode)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)

    @property
    @pulumi.getter(name="directoryMode")
    def directory_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The Unix directory mode in the string form "nnnn". Defaults to `"0777"`.
        """
        return pulumi.get(self, "directory_mode")

    @directory_mode.setter
    def directory_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory_mode", value)

    @property
    @pulumi.getter(name="fileMode")
    def file_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The Unix file mode in the string form "nnnn". Defaults to `"0666"`.
        """
        return pulumi.get(self, "file_mode")

    @file_mode.setter
    def file_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_mode", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[int]]:
        """
        The default group ID for the file share (unless the files have another group ID specified). Defaults to `65534` (`nfsnobody`). Valid values: `0` through `4294967294`.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[int]]:
        """
        The default owner ID for the file share (unless the files have another owner ID specified). Defaults to `65534` (`nfsnobody`). Valid values: `0` through `4294967294`.
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "owner_id", value)


@pulumi.input_type
class SmbFileShareCacheAttributesArgs:
    def __init__(__self__, *,
                 cache_stale_timeout_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] cache_stale_timeout_in_seconds: Refreshes a file share's cache by using Time To Live (TTL).
               TTL is the length of time since the last refresh after which access to the directory would cause the file gateway
               to first refresh that directory's contents from the Amazon S3 bucket. Valid Values: 300 to 2,592,000 seconds (5 minutes to 30 days)
        """
        if cache_stale_timeout_in_seconds is not None:
            pulumi.set(__self__, "cache_stale_timeout_in_seconds", cache_stale_timeout_in_seconds)

    @property
    @pulumi.getter(name="cacheStaleTimeoutInSeconds")
    def cache_stale_timeout_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Refreshes a file share's cache by using Time To Live (TTL).
        TTL is the length of time since the last refresh after which access to the directory would cause the file gateway
        to first refresh that directory's contents from the Amazon S3 bucket. Valid Values: 300 to 2,592,000 seconds (5 minutes to 30 days)
        """
        return pulumi.get(self, "cache_stale_timeout_in_seconds")

    @cache_stale_timeout_in_seconds.setter
    def cache_stale_timeout_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cache_stale_timeout_in_seconds", value)


