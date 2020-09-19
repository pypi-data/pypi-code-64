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

__all__ = ['ScheduledAction']


class ScheduledAction(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 scalable_dimension: Optional[pulumi.Input[str]] = None,
                 scalable_target_action: Optional[pulumi.Input[pulumi.InputType['ScheduledActionScalableTargetActionArgs']]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 service_namespace: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an Application AutoScaling ScheduledAction resource.

        ## Example Usage
        ### DynamoDB Table Autoscaling

        ```python
        import pulumi
        import pulumi_aws as aws

        dynamodb_target = aws.appautoscaling.Target("dynamodbTarget",
            max_capacity=100,
            min_capacity=5,
            resource_id="table/tableName",
            scalable_dimension="dynamodb:table:ReadCapacityUnits",
            service_namespace="dynamodb")
        dynamodb_scheduled_action = aws.appautoscaling.ScheduledAction("dynamodbScheduledAction",
            service_namespace=dynamodb_target.service_namespace,
            resource_id=dynamodb_target.resource_id,
            scalable_dimension=dynamodb_target.scalable_dimension,
            schedule="at(2006-01-02T15:04:05)",
            scalable_target_action=aws.appautoscaling.ScheduledActionScalableTargetActionArgs(
                min_capacity=1,
                max_capacity=200,
            ))
        ```
        ### ECS Service Autoscaling

        ```python
        import pulumi
        import pulumi_aws as aws

        ecs_target = aws.appautoscaling.Target("ecsTarget",
            max_capacity=4,
            min_capacity=1,
            resource_id="service/clusterName/serviceName",
            scalable_dimension="ecs:service:DesiredCount",
            service_namespace="ecs")
        ecs_scheduled_action = aws.appautoscaling.ScheduledAction("ecsScheduledAction",
            service_namespace=ecs_target.service_namespace,
            resource_id=ecs_target.resource_id,
            scalable_dimension=ecs_target.scalable_dimension,
            schedule="at(2006-01-02T15:04:05)",
            scalable_target_action=aws.appautoscaling.ScheduledActionScalableTargetActionArgs(
                min_capacity=1,
                max_capacity=10,
            ))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] end_time: The date and time for the scheduled action to end. Specify the following format: 2006-01-02T15:04:05Z
        :param pulumi.Input[str] name: The name of the scheduled action.
        :param pulumi.Input[str] resource_id: The identifier of the resource associated with the scheduled action. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ResourceId)
        :param pulumi.Input[str] scalable_dimension: The scalable dimension. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ScalableDimension) Example: ecs:service:DesiredCount
        :param pulumi.Input[pulumi.InputType['ScheduledActionScalableTargetActionArgs']] scalable_target_action: The new minimum and maximum capacity. You can set both values or just one. See below
        :param pulumi.Input[str] schedule: The schedule for this action. The following formats are supported: At expressions - at(yyyy-mm-ddThh:mm:ss), Rate expressions - rate(valueunit), Cron expressions - cron(fields). In UTC. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-Schedule)
        :param pulumi.Input[str] service_namespace: The namespace of the AWS service. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ServiceNamespace) Example: ecs
        :param pulumi.Input[str] start_time: The date and time for the scheduled action to start. Specify the following format: 2006-01-02T15:04:05Z
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

            __props__['end_time'] = end_time
            __props__['name'] = name
            if resource_id is None:
                raise TypeError("Missing required property 'resource_id'")
            __props__['resource_id'] = resource_id
            __props__['scalable_dimension'] = scalable_dimension
            __props__['scalable_target_action'] = scalable_target_action
            __props__['schedule'] = schedule
            if service_namespace is None:
                raise TypeError("Missing required property 'service_namespace'")
            __props__['service_namespace'] = service_namespace
            __props__['start_time'] = start_time
            __props__['arn'] = None
        super(ScheduledAction, __self__).__init__(
            'aws:appautoscaling/scheduledAction:ScheduledAction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            end_time: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_id: Optional[pulumi.Input[str]] = None,
            scalable_dimension: Optional[pulumi.Input[str]] = None,
            scalable_target_action: Optional[pulumi.Input[pulumi.InputType['ScheduledActionScalableTargetActionArgs']]] = None,
            schedule: Optional[pulumi.Input[str]] = None,
            service_namespace: Optional[pulumi.Input[str]] = None,
            start_time: Optional[pulumi.Input[str]] = None) -> 'ScheduledAction':
        """
        Get an existing ScheduledAction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the scheduled action.
        :param pulumi.Input[str] end_time: The date and time for the scheduled action to end. Specify the following format: 2006-01-02T15:04:05Z
        :param pulumi.Input[str] name: The name of the scheduled action.
        :param pulumi.Input[str] resource_id: The identifier of the resource associated with the scheduled action. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ResourceId)
        :param pulumi.Input[str] scalable_dimension: The scalable dimension. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ScalableDimension) Example: ecs:service:DesiredCount
        :param pulumi.Input[pulumi.InputType['ScheduledActionScalableTargetActionArgs']] scalable_target_action: The new minimum and maximum capacity. You can set both values or just one. See below
        :param pulumi.Input[str] schedule: The schedule for this action. The following formats are supported: At expressions - at(yyyy-mm-ddThh:mm:ss), Rate expressions - rate(valueunit), Cron expressions - cron(fields). In UTC. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-Schedule)
        :param pulumi.Input[str] service_namespace: The namespace of the AWS service. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ServiceNamespace) Example: ecs
        :param pulumi.Input[str] start_time: The date and time for the scheduled action to start. Specify the following format: 2006-01-02T15:04:05Z
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["end_time"] = end_time
        __props__["name"] = name
        __props__["resource_id"] = resource_id
        __props__["scalable_dimension"] = scalable_dimension
        __props__["scalable_target_action"] = scalable_target_action
        __props__["schedule"] = schedule
        __props__["service_namespace"] = service_namespace
        __props__["start_time"] = start_time
        return ScheduledAction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the scheduled action.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        The date and time for the scheduled action to end. Specify the following format: 2006-01-02T15:04:05Z
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the scheduled action.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Output[str]:
        """
        The identifier of the resource associated with the scheduled action. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ResourceId)
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="scalableDimension")
    def scalable_dimension(self) -> pulumi.Output[Optional[str]]:
        """
        The scalable dimension. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ScalableDimension) Example: ecs:service:DesiredCount
        """
        return pulumi.get(self, "scalable_dimension")

    @property
    @pulumi.getter(name="scalableTargetAction")
    def scalable_target_action(self) -> pulumi.Output[Optional['outputs.ScheduledActionScalableTargetAction']]:
        """
        The new minimum and maximum capacity. You can set both values or just one. See below
        """
        return pulumi.get(self, "scalable_target_action")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional[str]]:
        """
        The schedule for this action. The following formats are supported: At expressions - at(yyyy-mm-ddThh:mm:ss), Rate expressions - rate(valueunit), Cron expressions - cron(fields). In UTC. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-Schedule)
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="serviceNamespace")
    def service_namespace(self) -> pulumi.Output[str]:
        """
        The namespace of the AWS service. Documentation can be found in the parameter at: [AWS Application Auto Scaling API Reference](https://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_PutScheduledAction.html#ApplicationAutoScaling-PutScheduledAction-request-ServiceNamespace) Example: ecs
        """
        return pulumi.get(self, "service_namespace")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        The date and time for the scheduled action to start. Specify the following format: 2006-01-02T15:04:05Z
        """
        return pulumi.get(self, "start_time")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

