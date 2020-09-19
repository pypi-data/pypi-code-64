# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetFunctionResult',
    'AwaitableGetFunctionResult',
    'get_function',
]

@pulumi.output_type
class GetFunctionResult:
    """
    A collection of values returned by getFunction.
    """
    def __init__(__self__, arn=None, dead_letter_config=None, description=None, environment=None, file_system_configs=None, function_name=None, handler=None, id=None, invoke_arn=None, kms_key_arn=None, last_modified=None, layers=None, memory_size=None, qualified_arn=None, qualifier=None, reserved_concurrent_executions=None, role=None, runtime=None, source_code_hash=None, source_code_size=None, tags=None, timeout=None, tracing_config=None, version=None, vpc_config=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if dead_letter_config and not isinstance(dead_letter_config, dict):
            raise TypeError("Expected argument 'dead_letter_config' to be a dict")
        pulumi.set(__self__, "dead_letter_config", dead_letter_config)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if environment and not isinstance(environment, dict):
            raise TypeError("Expected argument 'environment' to be a dict")
        pulumi.set(__self__, "environment", environment)
        if file_system_configs and not isinstance(file_system_configs, list):
            raise TypeError("Expected argument 'file_system_configs' to be a list")
        pulumi.set(__self__, "file_system_configs", file_system_configs)
        if function_name and not isinstance(function_name, str):
            raise TypeError("Expected argument 'function_name' to be a str")
        pulumi.set(__self__, "function_name", function_name)
        if handler and not isinstance(handler, str):
            raise TypeError("Expected argument 'handler' to be a str")
        pulumi.set(__self__, "handler", handler)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if invoke_arn and not isinstance(invoke_arn, str):
            raise TypeError("Expected argument 'invoke_arn' to be a str")
        pulumi.set(__self__, "invoke_arn", invoke_arn)
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise TypeError("Expected argument 'kms_key_arn' to be a str")
        pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if last_modified and not isinstance(last_modified, str):
            raise TypeError("Expected argument 'last_modified' to be a str")
        pulumi.set(__self__, "last_modified", last_modified)
        if layers and not isinstance(layers, list):
            raise TypeError("Expected argument 'layers' to be a list")
        pulumi.set(__self__, "layers", layers)
        if memory_size and not isinstance(memory_size, int):
            raise TypeError("Expected argument 'memory_size' to be a int")
        pulumi.set(__self__, "memory_size", memory_size)
        if qualified_arn and not isinstance(qualified_arn, str):
            raise TypeError("Expected argument 'qualified_arn' to be a str")
        pulumi.set(__self__, "qualified_arn", qualified_arn)
        if qualifier and not isinstance(qualifier, str):
            raise TypeError("Expected argument 'qualifier' to be a str")
        pulumi.set(__self__, "qualifier", qualifier)
        if reserved_concurrent_executions and not isinstance(reserved_concurrent_executions, int):
            raise TypeError("Expected argument 'reserved_concurrent_executions' to be a int")
        pulumi.set(__self__, "reserved_concurrent_executions", reserved_concurrent_executions)
        if role and not isinstance(role, str):
            raise TypeError("Expected argument 'role' to be a str")
        pulumi.set(__self__, "role", role)
        if runtime and not isinstance(runtime, str):
            raise TypeError("Expected argument 'runtime' to be a str")
        pulumi.set(__self__, "runtime", runtime)
        if source_code_hash and not isinstance(source_code_hash, str):
            raise TypeError("Expected argument 'source_code_hash' to be a str")
        pulumi.set(__self__, "source_code_hash", source_code_hash)
        if source_code_size and not isinstance(source_code_size, int):
            raise TypeError("Expected argument 'source_code_size' to be a int")
        pulumi.set(__self__, "source_code_size", source_code_size)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if timeout and not isinstance(timeout, int):
            raise TypeError("Expected argument 'timeout' to be a int")
        pulumi.set(__self__, "timeout", timeout)
        if tracing_config and not isinstance(tracing_config, dict):
            raise TypeError("Expected argument 'tracing_config' to be a dict")
        pulumi.set(__self__, "tracing_config", tracing_config)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)
        if vpc_config and not isinstance(vpc_config, dict):
            raise TypeError("Expected argument 'vpc_config' to be a dict")
        pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Unqualified (no `:QUALIFIER` or `:VERSION` suffix) Amazon Resource Name (ARN) identifying your Lambda Function. See also `qualified_arn`.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deadLetterConfig")
    def dead_letter_config(self) -> 'outputs.GetFunctionDeadLetterConfigResult':
        """
        Configure the function's *dead letter queue*.
        """
        return pulumi.get(self, "dead_letter_config")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of what your Lambda Function does.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def environment(self) -> 'outputs.GetFunctionEnvironmentResult':
        """
        The Lambda environment's configuration settings.
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter(name="fileSystemConfigs")
    def file_system_configs(self) -> Sequence['outputs.GetFunctionFileSystemConfigResult']:
        """
        The connection settings for an Amazon EFS file system.
        """
        return pulumi.get(self, "file_system_configs")

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> str:
        return pulumi.get(self, "function_name")

    @property
    @pulumi.getter
    def handler(self) -> str:
        """
        The function entrypoint in your code.
        """
        return pulumi.get(self, "handler")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="invokeArn")
    def invoke_arn(self) -> str:
        """
        The ARN to be used for invoking Lambda Function from API Gateway.
        """
        return pulumi.get(self, "invoke_arn")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> str:
        """
        The ARN for the KMS encryption key.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        The date this resource was last modified.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def layers(self) -> Sequence[str]:
        """
        A list of Lambda Layer ARNs attached to your Lambda Function.
        """
        return pulumi.get(self, "layers")

    @property
    @pulumi.getter(name="memorySize")
    def memory_size(self) -> int:
        """
        Amount of memory in MB your Lambda Function can use at runtime.
        """
        return pulumi.get(self, "memory_size")

    @property
    @pulumi.getter(name="qualifiedArn")
    def qualified_arn(self) -> str:
        """
        Qualified (`:QUALIFIER` or `:VERSION` suffix) Amazon Resource Name (ARN) identifying your Lambda Function. See also `arn`.
        """
        return pulumi.get(self, "qualified_arn")

    @property
    @pulumi.getter
    def qualifier(self) -> Optional[str]:
        return pulumi.get(self, "qualifier")

    @property
    @pulumi.getter(name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> int:
        """
        The amount of reserved concurrent executions for this lambda function or `-1` if unreserved.
        """
        return pulumi.get(self, "reserved_concurrent_executions")

    @property
    @pulumi.getter
    def role(self) -> str:
        """
        IAM role attached to the Lambda Function.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def runtime(self) -> str:
        """
        The runtime environment for the Lambda function..
        """
        return pulumi.get(self, "runtime")

    @property
    @pulumi.getter(name="sourceCodeHash")
    def source_code_hash(self) -> str:
        """
        Base64-encoded representation of raw SHA-256 sum of the zip file.
        """
        return pulumi.get(self, "source_code_hash")

    @property
    @pulumi.getter(name="sourceCodeSize")
    def source_code_size(self) -> int:
        """
        The size in bytes of the function .zip file.
        """
        return pulumi.get(self, "source_code_size")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> int:
        """
        The function execution time at which Lambda should terminate the function.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter(name="tracingConfig")
    def tracing_config(self) -> 'outputs.GetFunctionTracingConfigResult':
        """
        Tracing settings of the function.
        """
        return pulumi.get(self, "tracing_config")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of the Lambda function.
        """
        return pulumi.get(self, "version")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> 'outputs.GetFunctionVpcConfigResult':
        """
        VPC configuration associated with your Lambda function.
        """
        return pulumi.get(self, "vpc_config")


class AwaitableGetFunctionResult(GetFunctionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFunctionResult(
            arn=self.arn,
            dead_letter_config=self.dead_letter_config,
            description=self.description,
            environment=self.environment,
            file_system_configs=self.file_system_configs,
            function_name=self.function_name,
            handler=self.handler,
            id=self.id,
            invoke_arn=self.invoke_arn,
            kms_key_arn=self.kms_key_arn,
            last_modified=self.last_modified,
            layers=self.layers,
            memory_size=self.memory_size,
            qualified_arn=self.qualified_arn,
            qualifier=self.qualifier,
            reserved_concurrent_executions=self.reserved_concurrent_executions,
            role=self.role,
            runtime=self.runtime,
            source_code_hash=self.source_code_hash,
            source_code_size=self.source_code_size,
            tags=self.tags,
            timeout=self.timeout,
            tracing_config=self.tracing_config,
            version=self.version,
            vpc_config=self.vpc_config)


def get_function(function_name: Optional[str] = None,
                 qualifier: Optional[str] = None,
                 tags: Optional[Mapping[str, str]] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFunctionResult:
    """
    Provides information about a Lambda Function.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    config = pulumi.Config()
    function_name = config.require("functionName")
    existing = aws.lambda.get_function(function_name=function_name)
    ```


    :param str function_name: Name of the lambda function.
    :param str qualifier: Alias name or version number of the lambda function. e.g. `$LATEST`, `my-alias`, or `1`
    """
    __args__ = dict()
    __args__['functionName'] = function_name
    __args__['qualifier'] = qualifier
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:lambda/getFunction:getFunction', __args__, opts=opts, typ=GetFunctionResult).value

    return AwaitableGetFunctionResult(
        arn=__ret__.arn,
        dead_letter_config=__ret__.dead_letter_config,
        description=__ret__.description,
        environment=__ret__.environment,
        file_system_configs=__ret__.file_system_configs,
        function_name=__ret__.function_name,
        handler=__ret__.handler,
        id=__ret__.id,
        invoke_arn=__ret__.invoke_arn,
        kms_key_arn=__ret__.kms_key_arn,
        last_modified=__ret__.last_modified,
        layers=__ret__.layers,
        memory_size=__ret__.memory_size,
        qualified_arn=__ret__.qualified_arn,
        qualifier=__ret__.qualifier,
        reserved_concurrent_executions=__ret__.reserved_concurrent_executions,
        role=__ret__.role,
        runtime=__ret__.runtime,
        source_code_hash=__ret__.source_code_hash,
        source_code_size=__ret__.source_code_size,
        tags=__ret__.tags,
        timeout=__ret__.timeout,
        tracing_config=__ret__.tracing_config,
        version=__ret__.version,
        vpc_config=__ret__.vpc_config)
