# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Method']


class Method(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_key_required: Optional[pulumi.Input[bool]] = None,
                 authorization: Optional[pulumi.Input[str]] = None,
                 authorization_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 authorizer_id: Optional[pulumi.Input[str]] = None,
                 http_method: Optional[pulumi.Input[str]] = None,
                 request_models: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 request_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[bool]]]] = None,
                 request_validator_id: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a HTTP Method for an API Gateway Resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        my_demo_api = aws.apigateway.RestApi("myDemoAPI", description="This is my API for demonstration purposes")
        my_demo_resource = aws.apigateway.Resource("myDemoResource",
            rest_api=my_demo_api.id,
            parent_id=my_demo_api.root_resource_id,
            path_part="mydemoresource")
        my_demo_method = aws.apigateway.Method("myDemoMethod",
            rest_api=my_demo_api.id,
            resource_id=my_demo_resource.id,
            http_method="GET",
            authorization="NONE")
        ```
        ## Usage with Cognito User Pool Authorizer

        ```python
        import pulumi
        import pulumi_aws as aws

        config = pulumi.Config()
        cognito_user_pool_name = config.require_object("cognitoUserPoolName")
        this_user_pools = aws.cognito.get_user_pools(name=cognito_user_pool_name)
        this_rest_api = aws.apigateway.RestApi("thisRestApi")
        this_resource = aws.apigateway.Resource("thisResource",
            rest_api=this_rest_api.id,
            parent_id=this_rest_api.root_resource_id,
            path_part="{proxy+}")
        this_authorizer = aws.apigateway.Authorizer("thisAuthorizer",
            type="COGNITO_USER_POOLS",
            rest_api=this_rest_api.id,
            provider_arns=this_user_pools.arns)
        any = aws.apigateway.Method("any",
            rest_api=this_rest_api.id,
            resource_id=this_resource.id,
            http_method="ANY",
            authorization="COGNITO_USER_POOLS",
            authorizer_id=this_authorizer.id,
            request_parameters={
                "method.request.path.proxy": True,
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] api_key_required: Specify if the method requires an API key
        :param pulumi.Input[str] authorization: The type of authorization used for the method (`NONE`, `CUSTOM`, `AWS_IAM`, `COGNITO_USER_POOLS`)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorization_scopes: The authorization scopes used when the authorization is `COGNITO_USER_POOLS`
        :param pulumi.Input[str] authorizer_id: The authorizer id to be used when the authorization is `CUSTOM` or `COGNITO_USER_POOLS`
        :param pulumi.Input[str] http_method: The HTTP Method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `ANY`)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] request_models: A map of the API models used for the request's content type
               where key is the content type (e.g. `application/json`)
               and value is either `Error`, `Empty` (built-in models) or `apigateway.Model`'s `name`.
        :param pulumi.Input[Mapping[str, pulumi.Input[bool]]] request_parameters: A map of request parameters (from the path, query string and headers) that should be passed to the integration. The boolean value indicates whether the parameter is required (`true`) or optional (`false`).
               For example: `request_parameters = {"method.request.header.X-Some-Header" = true "method.request.querystring.some-query-param" = true}` would define that the header `X-Some-Header` and the query string `some-query-param` must be provided in the request.
        :param pulumi.Input[str] request_validator_id: The ID of a `apigateway.RequestValidator`
        :param pulumi.Input[str] resource_id: The API resource ID
        :param pulumi.Input[str] rest_api: The ID of the associated REST API
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

            __props__['api_key_required'] = api_key_required
            if authorization is None:
                raise TypeError("Missing required property 'authorization'")
            __props__['authorization'] = authorization
            __props__['authorization_scopes'] = authorization_scopes
            __props__['authorizer_id'] = authorizer_id
            if http_method is None:
                raise TypeError("Missing required property 'http_method'")
            __props__['http_method'] = http_method
            __props__['request_models'] = request_models
            __props__['request_parameters'] = request_parameters
            __props__['request_validator_id'] = request_validator_id
            if resource_id is None:
                raise TypeError("Missing required property 'resource_id'")
            __props__['resource_id'] = resource_id
            if rest_api is None:
                raise TypeError("Missing required property 'rest_api'")
            __props__['rest_api'] = rest_api
        super(Method, __self__).__init__(
            'aws:apigateway/method:Method',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_key_required: Optional[pulumi.Input[bool]] = None,
            authorization: Optional[pulumi.Input[str]] = None,
            authorization_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            authorizer_id: Optional[pulumi.Input[str]] = None,
            http_method: Optional[pulumi.Input[str]] = None,
            request_models: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            request_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[bool]]]] = None,
            request_validator_id: Optional[pulumi.Input[str]] = None,
            resource_id: Optional[pulumi.Input[str]] = None,
            rest_api: Optional[pulumi.Input[str]] = None) -> 'Method':
        """
        Get an existing Method resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] api_key_required: Specify if the method requires an API key
        :param pulumi.Input[str] authorization: The type of authorization used for the method (`NONE`, `CUSTOM`, `AWS_IAM`, `COGNITO_USER_POOLS`)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorization_scopes: The authorization scopes used when the authorization is `COGNITO_USER_POOLS`
        :param pulumi.Input[str] authorizer_id: The authorizer id to be used when the authorization is `CUSTOM` or `COGNITO_USER_POOLS`
        :param pulumi.Input[str] http_method: The HTTP Method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `ANY`)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] request_models: A map of the API models used for the request's content type
               where key is the content type (e.g. `application/json`)
               and value is either `Error`, `Empty` (built-in models) or `apigateway.Model`'s `name`.
        :param pulumi.Input[Mapping[str, pulumi.Input[bool]]] request_parameters: A map of request parameters (from the path, query string and headers) that should be passed to the integration. The boolean value indicates whether the parameter is required (`true`) or optional (`false`).
               For example: `request_parameters = {"method.request.header.X-Some-Header" = true "method.request.querystring.some-query-param" = true}` would define that the header `X-Some-Header` and the query string `some-query-param` must be provided in the request.
        :param pulumi.Input[str] request_validator_id: The ID of a `apigateway.RequestValidator`
        :param pulumi.Input[str] resource_id: The API resource ID
        :param pulumi.Input[str] rest_api: The ID of the associated REST API
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_key_required"] = api_key_required
        __props__["authorization"] = authorization
        __props__["authorization_scopes"] = authorization_scopes
        __props__["authorizer_id"] = authorizer_id
        __props__["http_method"] = http_method
        __props__["request_models"] = request_models
        __props__["request_parameters"] = request_parameters
        __props__["request_validator_id"] = request_validator_id
        __props__["resource_id"] = resource_id
        __props__["rest_api"] = rest_api
        return Method(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiKeyRequired")
    def api_key_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Specify if the method requires an API key
        """
        return pulumi.get(self, "api_key_required")

    @property
    @pulumi.getter
    def authorization(self) -> pulumi.Output[str]:
        """
        The type of authorization used for the method (`NONE`, `CUSTOM`, `AWS_IAM`, `COGNITO_USER_POOLS`)
        """
        return pulumi.get(self, "authorization")

    @property
    @pulumi.getter(name="authorizationScopes")
    def authorization_scopes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The authorization scopes used when the authorization is `COGNITO_USER_POOLS`
        """
        return pulumi.get(self, "authorization_scopes")

    @property
    @pulumi.getter(name="authorizerId")
    def authorizer_id(self) -> pulumi.Output[Optional[str]]:
        """
        The authorizer id to be used when the authorization is `CUSTOM` or `COGNITO_USER_POOLS`
        """
        return pulumi.get(self, "authorizer_id")

    @property
    @pulumi.getter(name="httpMethod")
    def http_method(self) -> pulumi.Output[str]:
        """
        The HTTP Method (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `ANY`)
        """
        return pulumi.get(self, "http_method")

    @property
    @pulumi.getter(name="requestModels")
    def request_models(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of the API models used for the request's content type
        where key is the content type (e.g. `application/json`)
        and value is either `Error`, `Empty` (built-in models) or `apigateway.Model`'s `name`.
        """
        return pulumi.get(self, "request_models")

    @property
    @pulumi.getter(name="requestParameters")
    def request_parameters(self) -> pulumi.Output[Optional[Mapping[str, bool]]]:
        """
        A map of request parameters (from the path, query string and headers) that should be passed to the integration. The boolean value indicates whether the parameter is required (`true`) or optional (`false`).
        For example: `request_parameters = {"method.request.header.X-Some-Header" = true "method.request.querystring.some-query-param" = true}` would define that the header `X-Some-Header` and the query string `some-query-param` must be provided in the request.
        """
        return pulumi.get(self, "request_parameters")

    @property
    @pulumi.getter(name="requestValidatorId")
    def request_validator_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a `apigateway.RequestValidator`
        """
        return pulumi.get(self, "request_validator_id")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Output[str]:
        """
        The API resource ID
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> pulumi.Output[str]:
        """
        The ID of the associated REST API
        """
        return pulumi.get(self, "rest_api")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

