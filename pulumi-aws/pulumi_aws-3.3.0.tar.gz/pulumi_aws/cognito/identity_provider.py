# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['IdentityProvider']


class IdentityProvider(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attribute_mapping: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 idp_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 provider_details: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 provider_type: Optional[pulumi.Input[str]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a Cognito User Identity Provider resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cognito.UserPool("example", auto_verified_attributes=["email"])
        example_provider = aws.cognito.IdentityProvider("exampleProvider",
            user_pool_id=example.id,
            provider_name="Google",
            provider_type="Google",
            provider_details={
                "authorize_scopes": "email",
                "client_id": "your client_id",
                "client_secret": "your client_secret",
            },
            attribute_mapping={
                "email": "email",
                "username": "sub",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] attribute_mapping: The map of attribute mapping of user pool attributes. [AttributeMapping in AWS API documentation](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-AttributeMapping)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] idp_identifiers: The list of identity providers.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] provider_details: The map of identity details, such as access token
        :param pulumi.Input[str] provider_name: The provider name
        :param pulumi.Input[str] provider_type: The provider type.  [See AWS API for valid values](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-ProviderType)
        :param pulumi.Input[str] user_pool_id: The user pool id
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

            __props__['attribute_mapping'] = attribute_mapping
            __props__['idp_identifiers'] = idp_identifiers
            if provider_details is None:
                raise TypeError("Missing required property 'provider_details'")
            __props__['provider_details'] = provider_details
            if provider_name is None:
                raise TypeError("Missing required property 'provider_name'")
            __props__['provider_name'] = provider_name
            if provider_type is None:
                raise TypeError("Missing required property 'provider_type'")
            __props__['provider_type'] = provider_type
            if user_pool_id is None:
                raise TypeError("Missing required property 'user_pool_id'")
            __props__['user_pool_id'] = user_pool_id
        super(IdentityProvider, __self__).__init__(
            'aws:cognito/identityProvider:IdentityProvider',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attribute_mapping: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            idp_identifiers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            provider_details: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            provider_name: Optional[pulumi.Input[str]] = None,
            provider_type: Optional[pulumi.Input[str]] = None,
            user_pool_id: Optional[pulumi.Input[str]] = None) -> 'IdentityProvider':
        """
        Get an existing IdentityProvider resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] attribute_mapping: The map of attribute mapping of user pool attributes. [AttributeMapping in AWS API documentation](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-AttributeMapping)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] idp_identifiers: The list of identity providers.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] provider_details: The map of identity details, such as access token
        :param pulumi.Input[str] provider_name: The provider name
        :param pulumi.Input[str] provider_type: The provider type.  [See AWS API for valid values](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-ProviderType)
        :param pulumi.Input[str] user_pool_id: The user pool id
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["attribute_mapping"] = attribute_mapping
        __props__["idp_identifiers"] = idp_identifiers
        __props__["provider_details"] = provider_details
        __props__["provider_name"] = provider_name
        __props__["provider_type"] = provider_type
        __props__["user_pool_id"] = user_pool_id
        return IdentityProvider(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attributeMapping")
    def attribute_mapping(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The map of attribute mapping of user pool attributes. [AttributeMapping in AWS API documentation](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-AttributeMapping)
        """
        return pulumi.get(self, "attribute_mapping")

    @property
    @pulumi.getter(name="idpIdentifiers")
    def idp_identifiers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of identity providers.
        """
        return pulumi.get(self, "idp_identifiers")

    @property
    @pulumi.getter(name="providerDetails")
    def provider_details(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The map of identity details, such as access token
        """
        return pulumi.get(self, "provider_details")

    @property
    @pulumi.getter(name="providerName")
    def provider_name(self) -> pulumi.Output[str]:
        """
        The provider name
        """
        return pulumi.get(self, "provider_name")

    @property
    @pulumi.getter(name="providerType")
    def provider_type(self) -> pulumi.Output[str]:
        """
        The provider type.  [See AWS API for valid values](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html#CognitoUserPools-CreateIdentityProvider-request-ProviderType)
        """
        return pulumi.get(self, "provider_type")

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Output[str]:
        """
        The user pool id
        """
        return pulumi.get(self, "user_pool_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

