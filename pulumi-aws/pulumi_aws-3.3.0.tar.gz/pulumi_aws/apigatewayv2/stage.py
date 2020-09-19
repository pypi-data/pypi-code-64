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

__all__ = ['Stage']


class Stage(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_log_settings: Optional[pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']]] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 auto_deploy: Optional[pulumi.Input[bool]] = None,
                 client_certificate_id: Optional[pulumi.Input[str]] = None,
                 default_route_settings: Optional[pulumi.Input[pulumi.InputType['StageDefaultRouteSettingsArgs']]] = None,
                 deployment_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 route_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageRouteSettingArgs']]]]] = None,
                 stage_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages an Amazon API Gateway Version 2 stage.
        More information can be found in the [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api.html).

        ## Example Usage
        ### Basic

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.apigatewayv2.Stage("example", api_id=aws_apigatewayv2_api["example"]["id"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']] access_log_settings: Settings for logging access in this stage.
               Use the `apigateway.Account` resource to configure [permissions for CloudWatch Logging](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html#set-up-access-logging-permissions).
        :param pulumi.Input[str] api_id: The API identifier.
        :param pulumi.Input[bool] auto_deploy: Whether updates to an API automatically trigger a new deployment. Defaults to `false`.
        :param pulumi.Input[str] client_certificate_id: The identifier of a client certificate for the stage. Use the `apigateway.ClientCertificate` resource to configure a client certificate.
               Supported only for WebSocket APIs.
        :param pulumi.Input[pulumi.InputType['StageDefaultRouteSettingsArgs']] default_route_settings: The default route settings for the stage.
        :param pulumi.Input[str] deployment_id: The deployment identifier of the stage. Use the [`apigatewayv2.Deployment`](https://www.terraform.io/docs/providers/aws/r/apigatewayv2_deployment.html) resource to configure a deployment.
        :param pulumi.Input[str] description: The description for the stage.
        :param pulumi.Input[str] name: The name of the stage.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageRouteSettingArgs']]]] route_settings: Route settings for the stage.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] stage_variables: A map that defines the stage variables for the stage.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the stage.
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

            __props__['access_log_settings'] = access_log_settings
            if api_id is None:
                raise TypeError("Missing required property 'api_id'")
            __props__['api_id'] = api_id
            __props__['auto_deploy'] = auto_deploy
            __props__['client_certificate_id'] = client_certificate_id
            __props__['default_route_settings'] = default_route_settings
            __props__['deployment_id'] = deployment_id
            __props__['description'] = description
            __props__['name'] = name
            __props__['route_settings'] = route_settings
            __props__['stage_variables'] = stage_variables
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['execution_arn'] = None
            __props__['invoke_url'] = None
        super(Stage, __self__).__init__(
            'aws:apigatewayv2/stage:Stage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_log_settings: Optional[pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']]] = None,
            api_id: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            auto_deploy: Optional[pulumi.Input[bool]] = None,
            client_certificate_id: Optional[pulumi.Input[str]] = None,
            default_route_settings: Optional[pulumi.Input[pulumi.InputType['StageDefaultRouteSettingsArgs']]] = None,
            deployment_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            execution_arn: Optional[pulumi.Input[str]] = None,
            invoke_url: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            route_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageRouteSettingArgs']]]]] = None,
            stage_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Stage':
        """
        Get an existing Stage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StageAccessLogSettingsArgs']] access_log_settings: Settings for logging access in this stage.
               Use the `apigateway.Account` resource to configure [permissions for CloudWatch Logging](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html#set-up-access-logging-permissions).
        :param pulumi.Input[str] api_id: The API identifier.
        :param pulumi.Input[str] arn: The ARN of the stage.
        :param pulumi.Input[bool] auto_deploy: Whether updates to an API automatically trigger a new deployment. Defaults to `false`.
        :param pulumi.Input[str] client_certificate_id: The identifier of a client certificate for the stage. Use the `apigateway.ClientCertificate` resource to configure a client certificate.
               Supported only for WebSocket APIs.
        :param pulumi.Input[pulumi.InputType['StageDefaultRouteSettingsArgs']] default_route_settings: The default route settings for the stage.
        :param pulumi.Input[str] deployment_id: The deployment identifier of the stage. Use the [`apigatewayv2.Deployment`](https://www.terraform.io/docs/providers/aws/r/apigatewayv2_deployment.html) resource to configure a deployment.
        :param pulumi.Input[str] description: The description for the stage.
        :param pulumi.Input[str] execution_arn: The ARN prefix to be used in an `lambda.Permission` `source_arn` attribute.
               For WebSocket APIs this attribute can additionally be used in an `iam.Policy` to authorize access to the [`@connections` API](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html).
               See the [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-control-access-iam.html) for details.
        :param pulumi.Input[str] invoke_url: The URL to invoke the API pointing to the stage,
               e.g. `wss://z4675bid1j.execute-api.eu-west-2.amazonaws.com/example-stage`, or `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/`
        :param pulumi.Input[str] name: The name of the stage.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StageRouteSettingArgs']]]] route_settings: Route settings for the stage.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] stage_variables: A map that defines the stage variables for the stage.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the stage.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["access_log_settings"] = access_log_settings
        __props__["api_id"] = api_id
        __props__["arn"] = arn
        __props__["auto_deploy"] = auto_deploy
        __props__["client_certificate_id"] = client_certificate_id
        __props__["default_route_settings"] = default_route_settings
        __props__["deployment_id"] = deployment_id
        __props__["description"] = description
        __props__["execution_arn"] = execution_arn
        __props__["invoke_url"] = invoke_url
        __props__["name"] = name
        __props__["route_settings"] = route_settings
        __props__["stage_variables"] = stage_variables
        __props__["tags"] = tags
        return Stage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessLogSettings")
    def access_log_settings(self) -> pulumi.Output[Optional['outputs.StageAccessLogSettings']]:
        """
        Settings for logging access in this stage.
        Use the `apigateway.Account` resource to configure [permissions for CloudWatch Logging](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html#set-up-access-logging-permissions).
        """
        return pulumi.get(self, "access_log_settings")

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> pulumi.Output[str]:
        """
        The API identifier.
        """
        return pulumi.get(self, "api_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the stage.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoDeploy")
    def auto_deploy(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether updates to an API automatically trigger a new deployment. Defaults to `false`.
        """
        return pulumi.get(self, "auto_deploy")

    @property
    @pulumi.getter(name="clientCertificateId")
    def client_certificate_id(self) -> pulumi.Output[Optional[str]]:
        """
        The identifier of a client certificate for the stage. Use the `apigateway.ClientCertificate` resource to configure a client certificate.
        Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "client_certificate_id")

    @property
    @pulumi.getter(name="defaultRouteSettings")
    def default_route_settings(self) -> pulumi.Output[Optional['outputs.StageDefaultRouteSettings']]:
        """
        The default route settings for the stage.
        """
        return pulumi.get(self, "default_route_settings")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> pulumi.Output[str]:
        """
        The deployment identifier of the stage. Use the [`apigatewayv2.Deployment`](https://www.terraform.io/docs/providers/aws/r/apigatewayv2_deployment.html) resource to configure a deployment.
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description for the stage.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="executionArn")
    def execution_arn(self) -> pulumi.Output[str]:
        """
        The ARN prefix to be used in an `lambda.Permission` `source_arn` attribute.
        For WebSocket APIs this attribute can additionally be used in an `iam.Policy` to authorize access to the [`@connections` API](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html).
        See the [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-control-access-iam.html) for details.
        """
        return pulumi.get(self, "execution_arn")

    @property
    @pulumi.getter(name="invokeUrl")
    def invoke_url(self) -> pulumi.Output[str]:
        """
        The URL to invoke the API pointing to the stage,
        e.g. `wss://z4675bid1j.execute-api.eu-west-2.amazonaws.com/example-stage`, or `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/`
        """
        return pulumi.get(self, "invoke_url")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the stage.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="routeSettings")
    def route_settings(self) -> pulumi.Output[Optional[Sequence['outputs.StageRouteSetting']]]:
        """
        Route settings for the stage.
        """
        return pulumi.get(self, "route_settings")

    @property
    @pulumi.getter(name="stageVariables")
    def stage_variables(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map that defines the stage variables for the stage.
        """
        return pulumi.get(self, "stage_variables")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the stage.
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

