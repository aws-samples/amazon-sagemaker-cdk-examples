"""
## Amazon EC2 Auto Scaling Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

### Fleet

### Auto Scaling Group

An `AutoScalingGroup` represents a number of instances on which you run your code. You
pick the size of the fleet, the instance type and the OS image:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_ec2 as ec2

autoscaling.AutoScalingGroup(self, "ASG",
    vpc=vpc,
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
    machine_image=ec2.AmazonLinuxImage()
)
```

> NOTE: AutoScalingGroup has an property called `allowAllOutbound` (allowing the instances to contact the
> internet) which is set to `true` by default. Be sure to set this to `false`  if you don't want
> your instances to be able to start arbitrary connections.

### Machine Images (AMIs)

AMIs control the OS that gets launched when you start your EC2 instance. The EC2
library contains constructs to select the AMI you want to use.

Depending on the type of AMI, you select it a different way.

The latest version of Amazon Linux and Microsoft Windows images are
selectable by instantiating one of these classes:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Pick a Windows edition to use
windows = ec2.WindowsImage(ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE)

# Pick the right Amazon Linux edition. All arguments shown are optional
# and will default to these values when omitted.
amzn_linux = ec2.AmazonLinuxImage(
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

# For other custom (Linux) images, instantiate a `GenericLinuxImage` with
# a map giving the AMI to in for each region:

linux = ec2.GenericLinuxImage({
    "us-east-1": "ami-97785bed",
    "eu-west-1": "ami-12345678"
})
```

> NOTE: The Amazon Linux images selected will be cached in your `cdk.json`, so that your
> AutoScalingGroups don't automatically change out from under you when you're making unrelated
> changes. To update to the latest version of Amazon Linux, remove the cache entry from the `context`
> section of your `cdk.json`.
>
> We will add command-line options to make this step easier in the future.

### AutoScaling Instance Counts

AutoScalingGroups make it possible to raise and lower the number of instances in the group,
in response to (or in advance of) changes in workload.

When you create your AutoScalingGroup, you specify a `minCapacity` and a
`maxCapacity`. AutoScaling policies that respond to metrics will never go higher
or lower than the indicated capacity (but scheduled scaling actions might, see
below).

There are three ways to scale your capacity:

* **In response to a metric** (also known as step scaling); for example, you
  might want to scale out if the CPU usage across your cluster starts to rise,
  and scale in when it drops again.
* **By trying to keep a certain metric around a given value** (also known as
  target tracking scaling); you might want to automatically scale out and in to
  keep your CPU usage around 50%.
* **On a schedule**; you might want to organize your scaling around traffic
  flows you expect, by scaling out in the morning and scaling in in the
  evening.

The general pattern of autoscaling will look like this:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
    min_capacity=5,
    max_capacity=100
)

# Step scaling
auto_scaling_group.scale_on_metric(...)

# Target tracking scaling
auto_scaling_group.scale_on_cpu_utilization(...)
auto_scaling_group.scale_on_incoming_bytes(...)
auto_scaling_group.scale_on_outgoing_bytes(...)
auto_scaling_group.scale_on_request_count(...)
auto_scaling_group.scale_to_track_metric(...)

# Scheduled scaling
auto_scaling_group.scale_on_schedule(...)
```

#### Step Scaling

This type of scaling scales in and out in deterministics steps that you
configure, in response to metric values. For example, your scaling strategy to
scale in response to a metric that represents your average worker pool usage
might look like this:

```
 Scaling        -1          (no change)          +1       +3
            │        │                       │        │        │
            ├────────┼───────────────────────┼────────┼────────┤
            │        │                       │        │        │
Worker use  0%      10%                     50%       70%     100%
```

(Note that this is not necessarily a recommended scaling strategy, but it's
a possible one. You will have to determine what thresholds are right for you).

Note that in order to set up this scaling strategy, you will have to emit a
metric representing your worker utilization from your instances. After that,
you would configure the scaling something like this:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
worker_utilization_metric = cloudwatch.Metric(
    namespace="MyService",
    metric_name="WorkerUtilization"
)

capacity.scale_on_metric("ScaleToCPU",
    metric=worker_utilization_metric,
    scaling_steps=[{"upper": 10, "change": -1}, {"lower": 50, "change": +1}, {"lower": 70, "change": +3}
    ],

    # Change this to AdjustmentType.PERCENT_CHANGE_IN_CAPACITY to interpret the
    # 'change' numbers before as percentages instead of capacity counts.
    adjustment_type=autoscaling.AdjustmentType.CHANGE_IN_CAPACITY
)
```

The AutoScaling construct library will create the required CloudWatch alarms and
AutoScaling policies for you.

#### Target Tracking Scaling

This type of scaling scales in and out in order to keep a metric around a value
you prefer. There are four types of predefined metrics you can track, or you can
choose to track a custom metric. If you do choose to track a custom metric,
be aware that the metric has to represent instance utilization in some way
(AutoScaling will scale out if the metric is higher than the target, and scale
in if the metric is lower than the target).

If you configure multiple target tracking policies, AutoScaling will use the
one that yields the highest capacity.

The following example scales to keep the CPU usage of your instances around
50% utilization:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_cpu_utilization("KeepSpareCPU",
    target_utilization_percent=50
)
```

To scale on average network traffic in and out of your instances:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_incoming_bytes("LimitIngressPerInstance",
    target_bytes_per_second=10 * 1024 * 1024
)
auto_scaling_group.scale_on_outcoming_bytes("LimitEgressPerInstance",
    target_bytes_per_second=10 * 1024 * 1024
)
```

To scale on the average request count per instance (only works for
AutoScalingGroups that have been attached to Application Load
Balancers):

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_request_count("LimitRPS",
    target_requests_per_second=1000
)
```

#### Scheduled Scaling

This type of scaling is used to change capacities based on time. It works by
changing `minCapacity`, `maxCapacity` and `desiredCapacity` of the
AutoScalingGroup, and so can be used for two purposes:

* Scale in and out on a schedule by setting the `minCapacity` high or
  the `maxCapacity` low.
* Still allow the regular scaling actions to do their job, but restrict
  the range they can scale over (by setting both `minCapacity` and
  `maxCapacity` but changing their range over time).

A schedule is expressed as a cron expression. The `Schedule` class has a `cron` method to help build cron expressions.

The following example scales the fleet out in the morning, going back to natural
scaling (all the way down to 1 instance if necessary) at night:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
auto_scaling_group.scale_on_schedule("PrescaleInTheMorning",
    schedule=autoscaling.Schedule.cron(hour="8", minute="0"),
    min_capacity=20
)

auto_scaling_group.scale_on_schedule("AllowDownscalingAtNight",
    schedule=autoscaling.Schedule.cron(hour="20", minute="0"),
    min_capacity=1
)
```

### Allowing Connections

See the documentation of the `@aws-cdk/aws-ec2` package for more information
about allowing connections between resources backed by instances.

### Future work

* [ ] CloudWatch Events (impossible to add currently as the AutoScalingGroup ARN is
  necessary to make this rule and this cannot be accessed from CloudFormation).
"""
import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling_common
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_sns
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling", "1.18.0", __name__, "aws-autoscaling@1.18.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.AdjustmentTier", jsii_struct_bases=[], name_mapping={'adjustment': 'adjustment', 'lower_bound': 'lowerBound', 'upper_bound': 'upperBound'})
class AdjustmentTier():
    def __init__(self, *, adjustment: jsii.Number, lower_bound: typing.Optional[jsii.Number]=None, upper_bound: typing.Optional[jsii.Number]=None):
        """An adjustment.

        :param adjustment: What number to adjust the capacity with. The number is interpeted as an added capacity, a new fixed capacity or an added percentage depending on the AdjustmentType value of the StepScalingPolicy. Can be positive or negative.
        :param lower_bound: Lower bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is higher than this value. Default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        :param upper_bound: Upper bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is lower than this value. Default: +Infinity
        """
        self._values = {
            'adjustment': adjustment,
        }
        if lower_bound is not None: self._values["lower_bound"] = lower_bound
        if upper_bound is not None: self._values["upper_bound"] = upper_bound

    @property
    def adjustment(self) -> jsii.Number:
        """What number to adjust the capacity with.

        The number is interpeted as an added capacity, a new fixed capacity or an
        added percentage depending on the AdjustmentType value of the
        StepScalingPolicy.

        Can be positive or negative.
        """
        return self._values.get('adjustment')

    @property
    def lower_bound(self) -> typing.Optional[jsii.Number]:
        """Lower bound where this scaling tier applies.

        The scaling tier applies if the difference between the metric
        value and its alarm threshold is higher than this value.

        default
        :default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        """
        return self._values.get('lower_bound')

    @property
    def upper_bound(self) -> typing.Optional[jsii.Number]:
        """Upper bound where this scaling tier applies.

        The scaling tier applies if the difference between the metric
        value and its alarm threshold is lower than this value.

        default
        :default: +Infinity
        """
        return self._values.get('upper_bound')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AdjustmentTier(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.AdjustmentType")
class AdjustmentType(enum.Enum):
    """How adjustment numbers are interpreted."""
    CHANGE_IN_CAPACITY = "CHANGE_IN_CAPACITY"
    """Add the adjustment number to the current capacity.

    A positive number increases capacity, a negative number decreases capacity.
    """
    PERCENT_CHANGE_IN_CAPACITY = "PERCENT_CHANGE_IN_CAPACITY"
    """Add this percentage of the current capacity to itself.

    The number must be between -100 and 100; a positive number increases
    capacity and a negative number decreases it.
    """
    EXACT_CAPACITY = "EXACT_CAPACITY"
    """Make the capacity equal to the exact number given."""

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BaseTargetTrackingProps", jsii_struct_bases=[], name_mapping={'cooldown': 'cooldown', 'disable_scale_in': 'disableScaleIn', 'estimated_instance_warmup': 'estimatedInstanceWarmup'})
class BaseTargetTrackingProps():
    def __init__(self, *, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None):
        """Base interface for target tracking props.

        Contains the attributes that are common to target tracking policies,
        except the ones relating to the metric and to the scalable target.

        This interface is reused by more specific target tracking props objects.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        self._values = {
        }
        if cooldown is not None: self._values["cooldown"] = cooldown
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        return self._values.get('cooldown')

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: - Same as the cooldown.
        """
        return self._values.get('estimated_instance_warmup')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseTargetTrackingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicLifecycleHookProps", jsii_struct_bases=[], name_mapping={'lifecycle_transition': 'lifecycleTransition', 'notification_target': 'notificationTarget', 'default_result': 'defaultResult', 'heartbeat_timeout': 'heartbeatTimeout', 'lifecycle_hook_name': 'lifecycleHookName', 'notification_metadata': 'notificationMetadata', 'role': 'role'})
class BasicLifecycleHookProps():
    def __init__(self, *, lifecycle_transition: "LifecycleTransition", notification_target: "ILifecycleHookTarget", default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout: typing.Optional[aws_cdk.core.Duration]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Basic properties for a lifecycle hook.

        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        self._values = {
            'lifecycle_transition': lifecycle_transition,
            'notification_target': notification_target,
        }
        if default_result is not None: self._values["default_result"] = default_result
        if heartbeat_timeout is not None: self._values["heartbeat_timeout"] = heartbeat_timeout
        if lifecycle_hook_name is not None: self._values["lifecycle_hook_name"] = lifecycle_hook_name
        if notification_metadata is not None: self._values["notification_metadata"] = notification_metadata
        if role is not None: self._values["role"] = role

    @property
    def lifecycle_transition(self) -> "LifecycleTransition":
        """The state of the Amazon EC2 instance to which you want to attach the lifecycle hook."""
        return self._values.get('lifecycle_transition')

    @property
    def notification_target(self) -> "ILifecycleHookTarget":
        """The target of the lifecycle hook."""
        return self._values.get('notification_target')

    @property
    def default_result(self) -> typing.Optional["DefaultResult"]:
        """The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs.

        default
        :default: Continue
        """
        return self._values.get('default_result')

    @property
    def heartbeat_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum time between calls to RecordLifecycleActionHeartbeat for the hook.

        If the lifecycle hook times out, perform the action in DefaultResult.

        default
        :default: - No heartbeat timeout.
        """
        return self._values.get('heartbeat_timeout')

    @property
    def lifecycle_hook_name(self) -> typing.Optional[str]:
        """Name of the lifecycle hook.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('lifecycle_hook_name')

    @property
    def notification_metadata(self) -> typing.Optional[str]:
        """Additional data to pass to the lifecycle hook target.

        default
        :default: - No metadata.
        """
        return self._values.get('notification_metadata')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role that allows publishing to the notification target.

        default
        :default: - A role is automatically created.
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicLifecycleHookProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicScheduledActionProps", jsii_struct_bases=[], name_mapping={'schedule': 'schedule', 'desired_capacity': 'desiredCapacity', 'end_time': 'endTime', 'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'start_time': 'startTime'})
class BasicScheduledActionProps():
    def __init__(self, *, schedule: "Schedule", desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None):
        """Properties for a scheduled scaling action.

        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        self._values = {
            'schedule': schedule,
        }
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if end_time is not None: self._values["end_time"] = end_time
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if min_capacity is not None: self._values["min_capacity"] = min_capacity
        if start_time is not None: self._values["start_time"] = start_time

    @property
    def schedule(self) -> "Schedule":
        """When to perform this action.

        Supports cron expressions.

        For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            08 * * ?
        """
        return self._values.get('schedule')

    @property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """The new desired capacity.

        At the scheduled time, set the desired capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        default
        :default: - No new desired capacity.
        """
        return self._values.get('desired_capacity')

    @property
    def end_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action expires.

        default
        :default: - The rule never expires.
        """
        return self._values.get('end_time')

    @property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """The new maximum capacity.

        At the scheduled time, set the maximum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        default
        :default: - No new maximum capacity.
        """
        return self._values.get('max_capacity')

    @property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """The new minimum capacity.

        At the scheduled time, set the minimum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        default
        :default: - No new minimum capacity.
        """
        return self._values.get('min_capacity')

    @property
    def start_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action becomes active.

        default
        :default: - The rule is activate immediately.
        """
        return self._values.get('start_time')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicScheduledActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicStepScalingPolicyProps", jsii_struct_bases=[], name_mapping={'metric': 'metric', 'scaling_steps': 'scalingSteps', 'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'min_adjustment_magnitude': 'minAdjustmentMagnitude'})
class BasicStepScalingPolicyProps():
    def __init__(self, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None):
        """
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        self._values = {
            'metric': metric,
            'scaling_steps': scaling_steps,
        }
        if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
        if cooldown is not None: self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to scale on."""
        return self._values.get('metric')

    @property
    def scaling_steps(self) -> typing.List["ScalingInterval"]:
        """The intervals for scaling.

        Maps a range of metric values to a particular scaling behavior.
        """
        return self._values.get('scaling_steps')

    @property
    def adjustment_type(self) -> typing.Optional["AdjustmentType"]:
        """How the adjustment numbers inside 'intervals' are interpreted.

        default
        :default: ChangeInCapacity
        """
        return self._values.get('adjustment_type')

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Grace period after scaling activity.

        default
        :default: Default cooldown period on your AutoScalingGroup
        """
        return self._values.get('cooldown')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: Same as the cooldown
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        default
        :default: No minimum scaling effect
        """
        return self._values.get('min_adjustment_magnitude')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicStepScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicTargetTrackingScalingPolicyProps", jsii_struct_bases=[BaseTargetTrackingProps], name_mapping={'cooldown': 'cooldown', 'disable_scale_in': 'disableScaleIn', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'target_value': 'targetValue', 'custom_metric': 'customMetric', 'predefined_metric': 'predefinedMetric', 'resource_label': 'resourceLabel'})
class BasicTargetTrackingScalingPolicyProps(BaseTargetTrackingProps):
    def __init__(self, *, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None):
        """Properties for a Target Tracking policy that include the metric but exclude the target.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metric.
        :param resource_label: The resource label associated with the predefined metric. Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the format should be: app///targetgroup// Default: - No resource label.
        """
        self._values = {
            'target_value': target_value,
        }
        if cooldown is not None: self._values["cooldown"] = cooldown
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if custom_metric is not None: self._values["custom_metric"] = custom_metric
        if predefined_metric is not None: self._values["predefined_metric"] = predefined_metric
        if resource_label is not None: self._values["resource_label"] = resource_label

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        return self._values.get('cooldown')

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: - Same as the cooldown.
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def target_value(self) -> jsii.Number:
        """The target value for the metric."""
        return self._values.get('target_value')

    @property
    def custom_metric(self) -> typing.Optional[aws_cdk.aws_cloudwatch.IMetric]:
        """A custom metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No custom metric.
        """
        return self._values.get('custom_metric')

    @property
    def predefined_metric(self) -> typing.Optional["PredefinedMetric"]:
        """A predefined metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No predefined metric.
        """
        return self._values.get('predefined_metric')

    @property
    def resource_label(self) -> typing.Optional[str]:
        """The resource label associated with the predefined metric.

        Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the
        format should be:

        app///targetgroup//

        default
        :default: - No resource label.
        """
        return self._values.get('resource_label')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicTargetTrackingScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BlockDevice", jsii_struct_bases=[], name_mapping={'device_name': 'deviceName', 'volume': 'volume', 'mapping_enabled': 'mappingEnabled'})
class BlockDevice():
    def __init__(self, *, device_name: str, volume: "BlockDeviceVolume", mapping_enabled: typing.Optional[bool]=None):
        """
        :param device_name: The device name exposed to the EC2 instance.
        :param volume: Defines the block device volume, to be either an Amazon EBS volume or an ephemeral instance store volume.
        :param mapping_enabled: If false, the device mapping will be suppressed. If set to false for the root device, the instance might fail the Amazon EC2 health check. Amazon EC2 Auto Scaling launches a replacement instance if the instance fails the health check. Default: true - device mapping is left untouched
        """
        self._values = {
            'device_name': device_name,
            'volume': volume,
        }
        if mapping_enabled is not None: self._values["mapping_enabled"] = mapping_enabled

    @property
    def device_name(self) -> str:
        """The device name exposed to the EC2 instance.

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/device_naming.html

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            "/dev/sdh" , "xvdh"
        """
        return self._values.get('device_name')

    @property
    def volume(self) -> "BlockDeviceVolume":
        """Defines the block device volume, to be either an Amazon EBS volume or an ephemeral instance store volume.

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            BlockDeviceVolume.ebs(15) , BlockDeviceVolume.ephemeral(0)
        """
        return self._values.get('volume')

    @property
    def mapping_enabled(self) -> typing.Optional[bool]:
        """If false, the device mapping will be suppressed. If set to false for the root device, the instance might fail the Amazon EC2 health check. Amazon EC2 Auto Scaling launches a replacement instance if the instance fails the health check.

        default
        :default: true - device mapping is left untouched
        """
        return self._values.get('mapping_enabled')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BlockDevice(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BlockDeviceVolume(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.BlockDeviceVolume"):
    """Describes a block device mapping for an Auto Scaling group."""
    def __init__(self, ebs_device: typing.Optional["EbsDeviceProps"]=None, virtual_name: typing.Optional[str]=None) -> None:
        """
        :param ebs_device: -
        :param virtual_name: -
        """
        jsii.create(BlockDeviceVolume, self, [ebs_device, virtual_name])

    @jsii.member(jsii_name="ebs")
    @classmethod
    def ebs(cls, volume_size: jsii.Number, *, encrypted: typing.Optional[bool]=None, delete_on_termination: typing.Optional[bool]=None, iops: typing.Optional[jsii.Number]=None, volume_type: typing.Optional["EbsDeviceVolumeType"]=None) -> "BlockDeviceVolume":
        """Creates a new Elastic Block Storage device.

        :param volume_size: The volume size, in Gibibytes (GiB).
        :param options: additional device options.
        :param encrypted: Specifies whether the EBS volume is encrypted. Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption. Default: false
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume.
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        """
        options = EbsDeviceOptions(encrypted=encrypted, delete_on_termination=delete_on_termination, iops=iops, volume_type=volume_type)

        return jsii.sinvoke(cls, "ebs", [volume_size, options])

    @jsii.member(jsii_name="ebsFromSnapshot")
    @classmethod
    def ebs_from_snapshot(cls, snapshot_id: str, *, volume_size: typing.Optional[jsii.Number]=None, delete_on_termination: typing.Optional[bool]=None, iops: typing.Optional[jsii.Number]=None, volume_type: typing.Optional["EbsDeviceVolumeType"]=None) -> "BlockDeviceVolume":
        """Creates a new Elastic Block Storage device from an existing snapshot.

        :param snapshot_id: The snapshot ID of the volume to use.
        :param options: additional device options.
        :param volume_size: The volume size, in Gibibytes (GiB). If you specify volumeSize, it must be equal or greater than the size of the snapshot. Default: - The snapshot size
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume.
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        """
        options = EbsDeviceSnapshotOptions(volume_size=volume_size, delete_on_termination=delete_on_termination, iops=iops, volume_type=volume_type)

        return jsii.sinvoke(cls, "ebsFromSnapshot", [snapshot_id, options])

    @jsii.member(jsii_name="ephemeral")
    @classmethod
    def ephemeral(cls, volume_index: jsii.Number) -> "BlockDeviceVolume":
        """Creates a virtual, ephemeral device. The name will be in the form ephemeral{volumeIndex}.

        :param volume_index: the volume index. Must be equal or greater than 0
        """
        return jsii.sinvoke(cls, "ephemeral", [volume_index])

    @property
    @jsii.member(jsii_name="ebsDevice")
    def ebs_device(self) -> typing.Optional["EbsDeviceProps"]:
        return jsii.get(self, "ebsDevice")

    @property
    @jsii.member(jsii_name="virtualName")
    def virtual_name(self) -> typing.Optional[str]:
        return jsii.get(self, "virtualName")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAutoScalingGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup"):
    """A CloudFormation ``AWS::AutoScaling::AutoScalingGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
    cloudformationResource:
    :cloudformationResource:: AWS::AutoScaling::AutoScalingGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, max_size: str, min_size: str, auto_scaling_group_name: typing.Optional[str]=None, availability_zones: typing.Optional[typing.List[str]]=None, cooldown: typing.Optional[str]=None, desired_capacity: typing.Optional[str]=None, health_check_grace_period: typing.Optional[jsii.Number]=None, health_check_type: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, launch_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LaunchTemplateSpecificationProperty"]]]=None, lifecycle_hook_specification_list: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecycleHookSpecificationProperty"]]]]]=None, load_balancer_names: typing.Optional[typing.List[str]]=None, metrics_collection: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricsCollectionProperty"]]]]]=None, mixed_instances_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["MixedInstancesPolicyProperty"]]]=None, notification_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotificationConfigurationProperty"]]]]]=None, placement_group: typing.Optional[str]=None, service_linked_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagPropertyProperty"]]=None, target_group_arns: typing.Optional[typing.List[str]]=None, termination_policies: typing.Optional[typing.List[str]]=None, vpc_zone_identifier: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::AutoScaling::AutoScalingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param max_size: ``AWS::AutoScaling::AutoScalingGroup.MaxSize``.
        :param min_size: ``AWS::AutoScaling::AutoScalingGroup.MinSize``.
        :param auto_scaling_group_name: ``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.
        :param availability_zones: ``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.
        :param cooldown: ``AWS::AutoScaling::AutoScalingGroup.Cooldown``.
        :param desired_capacity: ``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.
        :param health_check_grace_period: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.
        :param health_check_type: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.
        :param instance_id: ``AWS::AutoScaling::AutoScalingGroup.InstanceId``.
        :param launch_configuration_name: ``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.
        :param launch_template: ``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.
        :param lifecycle_hook_specification_list: ``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.
        :param load_balancer_names: ``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.
        :param metrics_collection: ``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.
        :param mixed_instances_policy: ``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.
        :param notification_configurations: ``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.
        :param placement_group: ``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.
        :param service_linked_role_arn: ``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.
        :param tags: ``AWS::AutoScaling::AutoScalingGroup.Tags``.
        :param target_group_arns: ``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.
        :param termination_policies: ``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.
        :param vpc_zone_identifier: ``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.
        """
        props = CfnAutoScalingGroupProps(max_size=max_size, min_size=min_size, auto_scaling_group_name=auto_scaling_group_name, availability_zones=availability_zones, cooldown=cooldown, desired_capacity=desired_capacity, health_check_grace_period=health_check_grace_period, health_check_type=health_check_type, instance_id=instance_id, launch_configuration_name=launch_configuration_name, launch_template=launch_template, lifecycle_hook_specification_list=lifecycle_hook_specification_list, load_balancer_names=load_balancer_names, metrics_collection=metrics_collection, mixed_instances_policy=mixed_instances_policy, notification_configurations=notification_configurations, placement_group=placement_group, service_linked_role_arn=service_linked_role_arn, tags=tags, target_group_arns=target_group_arns, termination_policies=termination_policies, vpc_zone_identifier=vpc_zone_identifier)

        jsii.create(CfnAutoScalingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::AutoScaling::AutoScalingGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> str:
        """``AWS::AutoScaling::AutoScalingGroup.MaxSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-maxsize
        """
        return jsii.get(self, "maxSize")

    @max_size.setter
    def max_size(self, value: str):
        return jsii.set(self, "maxSize", value)

    @property
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> str:
        """``AWS::AutoScaling::AutoScalingGroup.MinSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-minsize
        """
        return jsii.get(self, "minSize")

    @min_size.setter
    def min_size(self, value: str):
        return jsii.set(self, "minSize", value)

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-autoscalinggroupname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter
    def auto_scaling_group_name(self, value: typing.Optional[str]):
        return jsii.set(self, "autoScalingGroupName", value)

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter
    def availability_zones(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "availabilityZones", value)

    @property
    @jsii.member(jsii_name="cooldown")
    def cooldown(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.Cooldown``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-cooldown
        """
        return jsii.get(self, "cooldown")

    @cooldown.setter
    def cooldown(self, value: typing.Optional[str]):
        return jsii.set(self, "cooldown", value)

    @property
    @jsii.member(jsii_name="desiredCapacity")
    def desired_capacity(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        """
        return jsii.get(self, "desiredCapacity")

    @desired_capacity.setter
    def desired_capacity(self, value: typing.Optional[str]):
        return jsii.set(self, "desiredCapacity", value)

    @property
    @jsii.member(jsii_name="healthCheckGracePeriod")
    def health_check_grace_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthcheckgraceperiod
        """
        return jsii.get(self, "healthCheckGracePeriod")

    @health_check_grace_period.setter
    def health_check_grace_period(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "healthCheckGracePeriod", value)

    @property
    @jsii.member(jsii_name="healthCheckType")
    def health_check_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthchecktype
        """
        return jsii.get(self, "healthCheckType")

    @health_check_type.setter
    def health_check_type(self, value: typing.Optional[str]):
        return jsii.set(self, "healthCheckType", value)

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.InstanceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-instanceid
        """
        return jsii.get(self, "instanceId")

    @instance_id.setter
    def instance_id(self, value: typing.Optional[str]):
        return jsii.set(self, "instanceId", value)

    @property
    @jsii.member(jsii_name="launchConfigurationName")
    def launch_configuration_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchconfigurationname
        """
        return jsii.get(self, "launchConfigurationName")

    @launch_configuration_name.setter
    def launch_configuration_name(self, value: typing.Optional[str]):
        return jsii.set(self, "launchConfigurationName", value)

    @property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LaunchTemplateSpecificationProperty"]]]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchtemplate
        """
        return jsii.get(self, "launchTemplate")

    @launch_template.setter
    def launch_template(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LaunchTemplateSpecificationProperty"]]]):
        return jsii.set(self, "launchTemplate", value)

    @property
    @jsii.member(jsii_name="lifecycleHookSpecificationList")
    def lifecycle_hook_specification_list(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecycleHookSpecificationProperty"]]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecificationlist
        """
        return jsii.get(self, "lifecycleHookSpecificationList")

    @lifecycle_hook_specification_list.setter
    def lifecycle_hook_specification_list(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecycleHookSpecificationProperty"]]]]]):
        return jsii.set(self, "lifecycleHookSpecificationList", value)

    @property
    @jsii.member(jsii_name="loadBalancerNames")
    def load_balancer_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-loadbalancernames
        """
        return jsii.get(self, "loadBalancerNames")

    @load_balancer_names.setter
    def load_balancer_names(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "loadBalancerNames", value)

    @property
    @jsii.member(jsii_name="metricsCollection")
    def metrics_collection(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricsCollectionProperty"]]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-metricscollection
        """
        return jsii.get(self, "metricsCollection")

    @metrics_collection.setter
    def metrics_collection(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MetricsCollectionProperty"]]]]]):
        return jsii.set(self, "metricsCollection", value)

    @property
    @jsii.member(jsii_name="mixedInstancesPolicy")
    def mixed_instances_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["MixedInstancesPolicyProperty"]]]:
        """``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-mixedinstancespolicy
        """
        return jsii.get(self, "mixedInstancesPolicy")

    @mixed_instances_policy.setter
    def mixed_instances_policy(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["MixedInstancesPolicyProperty"]]]):
        return jsii.set(self, "mixedInstancesPolicy", value)

    @property
    @jsii.member(jsii_name="notificationConfigurations")
    def notification_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotificationConfigurationProperty"]]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        """
        return jsii.get(self, "notificationConfigurations")

    @notification_configurations.setter
    def notification_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotificationConfigurationProperty"]]]]]):
        return jsii.set(self, "notificationConfigurations", value)

    @property
    @jsii.member(jsii_name="placementGroup")
    def placement_group(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-placementgroup
        """
        return jsii.get(self, "placementGroup")

    @placement_group.setter
    def placement_group(self, value: typing.Optional[str]):
        return jsii.set(self, "placementGroup", value)

    @property
    @jsii.member(jsii_name="serviceLinkedRoleArn")
    def service_linked_role_arn(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-servicelinkedrolearn
        """
        return jsii.get(self, "serviceLinkedRoleArn")

    @service_linked_role_arn.setter
    def service_linked_role_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "serviceLinkedRoleArn", value)

    @property
    @jsii.member(jsii_name="targetGroupArns")
    def target_group_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-targetgrouparns
        """
        return jsii.get(self, "targetGroupArns")

    @target_group_arns.setter
    def target_group_arns(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "targetGroupArns", value)

    @property
    @jsii.member(jsii_name="terminationPolicies")
    def termination_policies(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-termpolicy
        """
        return jsii.get(self, "terminationPolicies")

    @termination_policies.setter
    def termination_policies(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "terminationPolicies", value)

    @property
    @jsii.member(jsii_name="vpcZoneIdentifier")
    def vpc_zone_identifier(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-vpczoneidentifier
        """
        return jsii.get(self, "vpcZoneIdentifier")

    @vpc_zone_identifier.setter
    def vpc_zone_identifier(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "vpcZoneIdentifier", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.InstancesDistributionProperty", jsii_struct_bases=[], name_mapping={'on_demand_allocation_strategy': 'onDemandAllocationStrategy', 'on_demand_base_capacity': 'onDemandBaseCapacity', 'on_demand_percentage_above_base_capacity': 'onDemandPercentageAboveBaseCapacity', 'spot_allocation_strategy': 'spotAllocationStrategy', 'spot_instance_pools': 'spotInstancePools', 'spot_max_price': 'spotMaxPrice'})
    class InstancesDistributionProperty():
        def __init__(self, *, on_demand_allocation_strategy: typing.Optional[str]=None, on_demand_base_capacity: typing.Optional[jsii.Number]=None, on_demand_percentage_above_base_capacity: typing.Optional[jsii.Number]=None, spot_allocation_strategy: typing.Optional[str]=None, spot_instance_pools: typing.Optional[jsii.Number]=None, spot_max_price: typing.Optional[str]=None):
            """
            :param on_demand_allocation_strategy: ``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandAllocationStrategy``.
            :param on_demand_base_capacity: ``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandBaseCapacity``.
            :param on_demand_percentage_above_base_capacity: ``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandPercentageAboveBaseCapacity``.
            :param spot_allocation_strategy: ``CfnAutoScalingGroup.InstancesDistributionProperty.SpotAllocationStrategy``.
            :param spot_instance_pools: ``CfnAutoScalingGroup.InstancesDistributionProperty.SpotInstancePools``.
            :param spot_max_price: ``CfnAutoScalingGroup.InstancesDistributionProperty.SpotMaxPrice``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html
            """
            self._values = {
            }
            if on_demand_allocation_strategy is not None: self._values["on_demand_allocation_strategy"] = on_demand_allocation_strategy
            if on_demand_base_capacity is not None: self._values["on_demand_base_capacity"] = on_demand_base_capacity
            if on_demand_percentage_above_base_capacity is not None: self._values["on_demand_percentage_above_base_capacity"] = on_demand_percentage_above_base_capacity
            if spot_allocation_strategy is not None: self._values["spot_allocation_strategy"] = spot_allocation_strategy
            if spot_instance_pools is not None: self._values["spot_instance_pools"] = spot_instance_pools
            if spot_max_price is not None: self._values["spot_max_price"] = spot_max_price

        @property
        def on_demand_allocation_strategy(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandAllocationStrategy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandallocationstrategy
            """
            return self._values.get('on_demand_allocation_strategy')

        @property
        def on_demand_base_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandBaseCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandbasecapacity
            """
            return self._values.get('on_demand_base_capacity')

        @property
        def on_demand_percentage_above_base_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandPercentageAboveBaseCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandpercentageabovebasecapacity
            """
            return self._values.get('on_demand_percentage_above_base_capacity')

        @property
        def spot_allocation_strategy(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotAllocationStrategy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotallocationstrategy
            """
            return self._values.get('spot_allocation_strategy')

        @property
        def spot_instance_pools(self) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotInstancePools``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotinstancepools
            """
            return self._values.get('spot_instance_pools')

        @property
        def spot_max_price(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotMaxPrice``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotmaxprice
            """
            return self._values.get('spot_max_price')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InstancesDistributionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateOverridesProperty", jsii_struct_bases=[], name_mapping={'instance_type': 'instanceType'})
    class LaunchTemplateOverridesProperty():
        def __init__(self, *, instance_type: typing.Optional[str]=None):
            """
            :param instance_type: ``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.InstanceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html
            """
            self._values = {
            }
            if instance_type is not None: self._values["instance_type"] = instance_type

        @property
        def instance_type(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.InstanceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-instancetype
            """
            return self._values.get('instance_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LaunchTemplateOverridesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateProperty", jsii_struct_bases=[], name_mapping={'launch_template_specification': 'launchTemplateSpecification', 'overrides': 'overrides'})
    class LaunchTemplateProperty():
        def __init__(self, *, launch_template_specification: typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"], overrides: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateOverridesProperty"]]]]]=None):
            """
            :param launch_template_specification: ``CfnAutoScalingGroup.LaunchTemplateProperty.LaunchTemplateSpecification``.
            :param overrides: ``CfnAutoScalingGroup.LaunchTemplateProperty.Overrides``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html
            """
            self._values = {
                'launch_template_specification': launch_template_specification,
            }
            if overrides is not None: self._values["overrides"] = overrides

        @property
        def launch_template_specification(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]:
            """``CfnAutoScalingGroup.LaunchTemplateProperty.LaunchTemplateSpecification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html#cfn-as-group-launchtemplate
            """
            return self._values.get('launch_template_specification')

        @property
        def overrides(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateOverridesProperty"]]]]]:
            """``CfnAutoScalingGroup.LaunchTemplateProperty.Overrides``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html#cfn-as-mixedinstancespolicy-overrides
            """
            return self._values.get('overrides')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LaunchTemplateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateSpecificationProperty", jsii_struct_bases=[], name_mapping={'version': 'version', 'launch_template_id': 'launchTemplateId', 'launch_template_name': 'launchTemplateName'})
    class LaunchTemplateSpecificationProperty():
        def __init__(self, *, version: str, launch_template_id: typing.Optional[str]=None, launch_template_name: typing.Optional[str]=None):
            """
            :param version: ``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.Version``.
            :param launch_template_id: ``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateId``.
            :param launch_template_name: ``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html
            """
            self._values = {
                'version': version,
            }
            if launch_template_id is not None: self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None: self._values["launch_template_name"] = launch_template_name

        @property
        def version(self) -> str:
            """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-version
            """
            return self._values.get('version')

        @property
        def launch_template_id(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplateid
            """
            return self._values.get('launch_template_id')

        @property
        def launch_template_name(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplatename
            """
            return self._values.get('launch_template_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LaunchTemplateSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LifecycleHookSpecificationProperty", jsii_struct_bases=[], name_mapping={'lifecycle_hook_name': 'lifecycleHookName', 'lifecycle_transition': 'lifecycleTransition', 'default_result': 'defaultResult', 'heartbeat_timeout': 'heartbeatTimeout', 'notification_metadata': 'notificationMetadata', 'notification_target_arn': 'notificationTargetArn', 'role_arn': 'roleArn'})
    class LifecycleHookSpecificationProperty():
        def __init__(self, *, lifecycle_hook_name: str, lifecycle_transition: str, default_result: typing.Optional[str]=None, heartbeat_timeout: typing.Optional[jsii.Number]=None, notification_metadata: typing.Optional[str]=None, notification_target_arn: typing.Optional[str]=None, role_arn: typing.Optional[str]=None):
            """
            :param lifecycle_hook_name: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleHookName``.
            :param lifecycle_transition: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleTransition``.
            :param default_result: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.DefaultResult``.
            :param heartbeat_timeout: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.HeartbeatTimeout``.
            :param notification_metadata: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationMetadata``.
            :param notification_target_arn: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationTargetARN``.
            :param role_arn: ``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.RoleARN``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html
            """
            self._values = {
                'lifecycle_hook_name': lifecycle_hook_name,
                'lifecycle_transition': lifecycle_transition,
            }
            if default_result is not None: self._values["default_result"] = default_result
            if heartbeat_timeout is not None: self._values["heartbeat_timeout"] = heartbeat_timeout
            if notification_metadata is not None: self._values["notification_metadata"] = notification_metadata
            if notification_target_arn is not None: self._values["notification_target_arn"] = notification_target_arn
            if role_arn is not None: self._values["role_arn"] = role_arn

        @property
        def lifecycle_hook_name(self) -> str:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleHookName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecyclehookname
            """
            return self._values.get('lifecycle_hook_name')

        @property
        def lifecycle_transition(self) -> str:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleTransition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecycletransition
            """
            return self._values.get('lifecycle_transition')

        @property
        def default_result(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.DefaultResult``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-defaultresult
            """
            return self._values.get('default_result')

        @property
        def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.HeartbeatTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-heartbeattimeout
            """
            return self._values.get('heartbeat_timeout')

        @property
        def notification_metadata(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationMetadata``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationmetadata
            """
            return self._values.get('notification_metadata')

        @property
        def notification_target_arn(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationTargetARN``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationtargetarn
            """
            return self._values.get('notification_target_arn')

        @property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.RoleARN``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-rolearn
            """
            return self._values.get('role_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LifecycleHookSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MetricsCollectionProperty", jsii_struct_bases=[], name_mapping={'granularity': 'granularity', 'metrics': 'metrics'})
    class MetricsCollectionProperty():
        def __init__(self, *, granularity: str, metrics: typing.Optional[typing.List[str]]=None):
            """
            :param granularity: ``CfnAutoScalingGroup.MetricsCollectionProperty.Granularity``.
            :param metrics: ``CfnAutoScalingGroup.MetricsCollectionProperty.Metrics``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html
            """
            self._values = {
                'granularity': granularity,
            }
            if metrics is not None: self._values["metrics"] = metrics

        @property
        def granularity(self) -> str:
            """``CfnAutoScalingGroup.MetricsCollectionProperty.Granularity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html#cfn-as-metricscollection-granularity
            """
            return self._values.get('granularity')

        @property
        def metrics(self) -> typing.Optional[typing.List[str]]:
            """``CfnAutoScalingGroup.MetricsCollectionProperty.Metrics``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html#cfn-as-metricscollection-metrics
            """
            return self._values.get('metrics')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricsCollectionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MixedInstancesPolicyProperty", jsii_struct_bases=[], name_mapping={'launch_template': 'launchTemplate', 'instances_distribution': 'instancesDistribution'})
    class MixedInstancesPolicyProperty():
        def __init__(self, *, launch_template: typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateProperty"], instances_distribution: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAutoScalingGroup.InstancesDistributionProperty"]]]=None):
            """
            :param launch_template: ``CfnAutoScalingGroup.MixedInstancesPolicyProperty.LaunchTemplate``.
            :param instances_distribution: ``CfnAutoScalingGroup.MixedInstancesPolicyProperty.InstancesDistribution``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html
            """
            self._values = {
                'launch_template': launch_template,
            }
            if instances_distribution is not None: self._values["instances_distribution"] = instances_distribution

        @property
        def launch_template(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LaunchTemplateProperty"]:
            """``CfnAutoScalingGroup.MixedInstancesPolicyProperty.LaunchTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html#cfn-as-mixedinstancespolicy-launchtemplate
            """
            return self._values.get('launch_template')

        @property
        def instances_distribution(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAutoScalingGroup.InstancesDistributionProperty"]]]:
            """``CfnAutoScalingGroup.MixedInstancesPolicyProperty.InstancesDistribution``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html#cfn-as-mixedinstancespolicy-instancesdistribution
            """
            return self._values.get('instances_distribution')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MixedInstancesPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.NotificationConfigurationProperty", jsii_struct_bases=[], name_mapping={'topic_arn': 'topicArn', 'notification_types': 'notificationTypes'})
    class NotificationConfigurationProperty():
        def __init__(self, *, topic_arn: str, notification_types: typing.Optional[typing.List[str]]=None):
            """
            :param topic_arn: ``CfnAutoScalingGroup.NotificationConfigurationProperty.TopicARN``.
            :param notification_types: ``CfnAutoScalingGroup.NotificationConfigurationProperty.NotificationTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html
            """
            self._values = {
                'topic_arn': topic_arn,
            }
            if notification_types is not None: self._values["notification_types"] = notification_types

        @property
        def topic_arn(self) -> str:
            """``CfnAutoScalingGroup.NotificationConfigurationProperty.TopicARN``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html#cfn-autoscaling-autoscalinggroup-notificationconfigurations-topicarn
            """
            return self._values.get('topic_arn')

        @property
        def notification_types(self) -> typing.Optional[typing.List[str]]:
            """``CfnAutoScalingGroup.NotificationConfigurationProperty.NotificationTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html#cfn-as-group-notificationconfigurations-notificationtypes
            """
            return self._values.get('notification_types')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotificationConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.TagPropertyProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'propagate_at_launch': 'propagateAtLaunch', 'value': 'value'})
    class TagPropertyProperty():
        def __init__(self, *, key: str, propagate_at_launch: typing.Union[bool, aws_cdk.core.IResolvable], value: str):
            """
            :param key: ``CfnAutoScalingGroup.TagPropertyProperty.Key``.
            :param propagate_at_launch: ``CfnAutoScalingGroup.TagPropertyProperty.PropagateAtLaunch``.
            :param value: ``CfnAutoScalingGroup.TagPropertyProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html
            """
            self._values = {
                'key': key,
                'propagate_at_launch': propagate_at_launch,
                'value': value,
            }

        @property
        def key(self) -> str:
            """``CfnAutoScalingGroup.TagPropertyProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-Key
            """
            return self._values.get('key')

        @property
        def propagate_at_launch(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnAutoScalingGroup.TagPropertyProperty.PropagateAtLaunch``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-PropagateAtLaunch
            """
            return self._values.get('propagate_at_launch')

        @property
        def value(self) -> str:
            """``CfnAutoScalingGroup.TagPropertyProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-Value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagPropertyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroupProps", jsii_struct_bases=[], name_mapping={'max_size': 'maxSize', 'min_size': 'minSize', 'auto_scaling_group_name': 'autoScalingGroupName', 'availability_zones': 'availabilityZones', 'cooldown': 'cooldown', 'desired_capacity': 'desiredCapacity', 'health_check_grace_period': 'healthCheckGracePeriod', 'health_check_type': 'healthCheckType', 'instance_id': 'instanceId', 'launch_configuration_name': 'launchConfigurationName', 'launch_template': 'launchTemplate', 'lifecycle_hook_specification_list': 'lifecycleHookSpecificationList', 'load_balancer_names': 'loadBalancerNames', 'metrics_collection': 'metricsCollection', 'mixed_instances_policy': 'mixedInstancesPolicy', 'notification_configurations': 'notificationConfigurations', 'placement_group': 'placementGroup', 'service_linked_role_arn': 'serviceLinkedRoleArn', 'tags': 'tags', 'target_group_arns': 'targetGroupArns', 'termination_policies': 'terminationPolicies', 'vpc_zone_identifier': 'vpcZoneIdentifier'})
class CfnAutoScalingGroupProps():
    def __init__(self, *, max_size: str, min_size: str, auto_scaling_group_name: typing.Optional[str]=None, availability_zones: typing.Optional[typing.List[str]]=None, cooldown: typing.Optional[str]=None, desired_capacity: typing.Optional[str]=None, health_check_grace_period: typing.Optional[jsii.Number]=None, health_check_type: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, launch_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]]]=None, lifecycle_hook_specification_list: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LifecycleHookSpecificationProperty"]]]]]=None, load_balancer_names: typing.Optional[typing.List[str]]=None, metrics_collection: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MetricsCollectionProperty"]]]]]=None, mixed_instances_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAutoScalingGroup.MixedInstancesPolicyProperty"]]]=None, notification_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.NotificationConfigurationProperty"]]]]]=None, placement_group: typing.Optional[str]=None, service_linked_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnAutoScalingGroup.TagPropertyProperty"]]=None, target_group_arns: typing.Optional[typing.List[str]]=None, termination_policies: typing.Optional[typing.List[str]]=None, vpc_zone_identifier: typing.Optional[typing.List[str]]=None):
        """Properties for defining a ``AWS::AutoScaling::AutoScalingGroup``.

        :param max_size: ``AWS::AutoScaling::AutoScalingGroup.MaxSize``.
        :param min_size: ``AWS::AutoScaling::AutoScalingGroup.MinSize``.
        :param auto_scaling_group_name: ``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.
        :param availability_zones: ``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.
        :param cooldown: ``AWS::AutoScaling::AutoScalingGroup.Cooldown``.
        :param desired_capacity: ``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.
        :param health_check_grace_period: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.
        :param health_check_type: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.
        :param instance_id: ``AWS::AutoScaling::AutoScalingGroup.InstanceId``.
        :param launch_configuration_name: ``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.
        :param launch_template: ``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.
        :param lifecycle_hook_specification_list: ``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.
        :param load_balancer_names: ``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.
        :param metrics_collection: ``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.
        :param mixed_instances_policy: ``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.
        :param notification_configurations: ``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.
        :param placement_group: ``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.
        :param service_linked_role_arn: ``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.
        :param tags: ``AWS::AutoScaling::AutoScalingGroup.Tags``.
        :param target_group_arns: ``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.
        :param termination_policies: ``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.
        :param vpc_zone_identifier: ``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
        """
        self._values = {
            'max_size': max_size,
            'min_size': min_size,
        }
        if auto_scaling_group_name is not None: self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if availability_zones is not None: self._values["availability_zones"] = availability_zones
        if cooldown is not None: self._values["cooldown"] = cooldown
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if health_check_type is not None: self._values["health_check_type"] = health_check_type
        if instance_id is not None: self._values["instance_id"] = instance_id
        if launch_configuration_name is not None: self._values["launch_configuration_name"] = launch_configuration_name
        if launch_template is not None: self._values["launch_template"] = launch_template
        if lifecycle_hook_specification_list is not None: self._values["lifecycle_hook_specification_list"] = lifecycle_hook_specification_list
        if load_balancer_names is not None: self._values["load_balancer_names"] = load_balancer_names
        if metrics_collection is not None: self._values["metrics_collection"] = metrics_collection
        if mixed_instances_policy is not None: self._values["mixed_instances_policy"] = mixed_instances_policy
        if notification_configurations is not None: self._values["notification_configurations"] = notification_configurations
        if placement_group is not None: self._values["placement_group"] = placement_group
        if service_linked_role_arn is not None: self._values["service_linked_role_arn"] = service_linked_role_arn
        if tags is not None: self._values["tags"] = tags
        if target_group_arns is not None: self._values["target_group_arns"] = target_group_arns
        if termination_policies is not None: self._values["termination_policies"] = termination_policies
        if vpc_zone_identifier is not None: self._values["vpc_zone_identifier"] = vpc_zone_identifier

    @property
    def max_size(self) -> str:
        """``AWS::AutoScaling::AutoScalingGroup.MaxSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-maxsize
        """
        return self._values.get('max_size')

    @property
    def min_size(self) -> str:
        """``AWS::AutoScaling::AutoScalingGroup.MinSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-minsize
        """
        return self._values.get('min_size')

    @property
    def auto_scaling_group_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-autoscalinggroupname
        """
        return self._values.get('auto_scaling_group_name')

    @property
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-availabilityzones
        """
        return self._values.get('availability_zones')

    @property
    def cooldown(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.Cooldown``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-cooldown
        """
        return self._values.get('cooldown')

    @property
    def desired_capacity(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        """
        return self._values.get('desired_capacity')

    @property
    def health_check_grace_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthcheckgraceperiod
        """
        return self._values.get('health_check_grace_period')

    @property
    def health_check_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthchecktype
        """
        return self._values.get('health_check_type')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.InstanceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-instanceid
        """
        return self._values.get('instance_id')

    @property
    def launch_configuration_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchconfigurationname
        """
        return self._values.get('launch_configuration_name')

    @property
    def launch_template(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]]]:
        """``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchtemplate
        """
        return self._values.get('launch_template')

    @property
    def lifecycle_hook_specification_list(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.LifecycleHookSpecificationProperty"]]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecificationlist
        """
        return self._values.get('lifecycle_hook_specification_list')

    @property
    def load_balancer_names(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-loadbalancernames
        """
        return self._values.get('load_balancer_names')

    @property
    def metrics_collection(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.MetricsCollectionProperty"]]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-metricscollection
        """
        return self._values.get('metrics_collection')

    @property
    def mixed_instances_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnAutoScalingGroup.MixedInstancesPolicyProperty"]]]:
        """``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-mixedinstancespolicy
        """
        return self._values.get('mixed_instances_policy')

    @property
    def notification_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAutoScalingGroup.NotificationConfigurationProperty"]]]]]:
        """``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        """
        return self._values.get('notification_configurations')

    @property
    def placement_group(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-placementgroup
        """
        return self._values.get('placement_group')

    @property
    def service_linked_role_arn(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-servicelinkedrolearn
        """
        return self._values.get('service_linked_role_arn')

    @property
    def tags(self) -> typing.Optional[typing.List["CfnAutoScalingGroup.TagPropertyProperty"]]:
        """``AWS::AutoScaling::AutoScalingGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-tags
        """
        return self._values.get('tags')

    @property
    def target_group_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-targetgrouparns
        """
        return self._values.get('target_group_arns')

    @property
    def termination_policies(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-termpolicy
        """
        return self._values.get('termination_policies')

    @property
    def vpc_zone_identifier(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-vpczoneidentifier
        """
        return self._values.get('vpc_zone_identifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAutoScalingGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLaunchConfiguration(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration"):
    """A CloudFormation ``AWS::AutoScaling::LaunchConfiguration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
    cloudformationResource:
    :cloudformationResource:: AWS::AutoScaling::LaunchConfiguration
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, image_id: str, instance_type: str, associate_public_ip_address: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, block_device_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "BlockDeviceMappingProperty"]]]]]=None, classic_link_vpc_id: typing.Optional[str]=None, classic_link_vpc_security_groups: typing.Optional[typing.List[str]]=None, ebs_optimized: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, iam_instance_profile: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, instance_monitoring: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, kernel_id: typing.Optional[str]=None, key_name: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, placement_tenancy: typing.Optional[str]=None, ram_disk_id: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, spot_price: typing.Optional[str]=None, user_data: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::AutoScaling::LaunchConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param image_id: ``AWS::AutoScaling::LaunchConfiguration.ImageId``.
        :param instance_type: ``AWS::AutoScaling::LaunchConfiguration.InstanceType``.
        :param associate_public_ip_address: ``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.
        :param block_device_mappings: ``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.
        :param classic_link_vpc_id: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.
        :param classic_link_vpc_security_groups: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.
        :param ebs_optimized: ``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.
        :param iam_instance_profile: ``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.
        :param instance_id: ``AWS::AutoScaling::LaunchConfiguration.InstanceId``.
        :param instance_monitoring: ``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.
        :param kernel_id: ``AWS::AutoScaling::LaunchConfiguration.KernelId``.
        :param key_name: ``AWS::AutoScaling::LaunchConfiguration.KeyName``.
        :param launch_configuration_name: ``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.
        :param placement_tenancy: ``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.
        :param ram_disk_id: ``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.
        :param security_groups: ``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.
        :param spot_price: ``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.
        :param user_data: ``AWS::AutoScaling::LaunchConfiguration.UserData``.
        """
        props = CfnLaunchConfigurationProps(image_id=image_id, instance_type=instance_type, associate_public_ip_address=associate_public_ip_address, block_device_mappings=block_device_mappings, classic_link_vpc_id=classic_link_vpc_id, classic_link_vpc_security_groups=classic_link_vpc_security_groups, ebs_optimized=ebs_optimized, iam_instance_profile=iam_instance_profile, instance_id=instance_id, instance_monitoring=instance_monitoring, kernel_id=kernel_id, key_name=key_name, launch_configuration_name=launch_configuration_name, placement_tenancy=placement_tenancy, ram_disk_id=ram_disk_id, security_groups=security_groups, spot_price=spot_price, user_data=user_data)

        jsii.create(CfnLaunchConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """``AWS::AutoScaling::LaunchConfiguration.ImageId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-imageid
        """
        return jsii.get(self, "imageId")

    @image_id.setter
    def image_id(self, value: str):
        return jsii.set(self, "imageId", value)

    @property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> str:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancetype
        """
        return jsii.get(self, "instanceType")

    @instance_type.setter
    def instance_type(self, value: str):
        return jsii.set(self, "instanceType", value)

    @property
    @jsii.member(jsii_name="associatePublicIpAddress")
    def associate_public_ip_address(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cf-as-launchconfig-associatepubip
        """
        return jsii.get(self, "associatePublicIpAddress")

    @associate_public_ip_address.setter
    def associate_public_ip_address(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "associatePublicIpAddress", value)

    @property
    @jsii.member(jsii_name="blockDeviceMappings")
    def block_device_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "BlockDeviceMappingProperty"]]]]]:
        """``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-blockdevicemappings
        """
        return jsii.get(self, "blockDeviceMappings")

    @block_device_mappings.setter
    def block_device_mappings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "BlockDeviceMappingProperty"]]]]]):
        return jsii.set(self, "blockDeviceMappings", value)

    @property
    @jsii.member(jsii_name="classicLinkVpcId")
    def classic_link_vpc_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcid
        """
        return jsii.get(self, "classicLinkVpcId")

    @classic_link_vpc_id.setter
    def classic_link_vpc_id(self, value: typing.Optional[str]):
        return jsii.set(self, "classicLinkVpcId", value)

    @property
    @jsii.member(jsii_name="classicLinkVpcSecurityGroups")
    def classic_link_vpc_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcsecuritygroups
        """
        return jsii.get(self, "classicLinkVpcSecurityGroups")

    @classic_link_vpc_security_groups.setter
    def classic_link_vpc_security_groups(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "classicLinkVpcSecurityGroups", value)

    @property
    @jsii.member(jsii_name="ebsOptimized")
    def ebs_optimized(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ebsoptimized
        """
        return jsii.get(self, "ebsOptimized")

    @ebs_optimized.setter
    def ebs_optimized(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "ebsOptimized", value)

    @property
    @jsii.member(jsii_name="iamInstanceProfile")
    def iam_instance_profile(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-iaminstanceprofile
        """
        return jsii.get(self, "iamInstanceProfile")

    @iam_instance_profile.setter
    def iam_instance_profile(self, value: typing.Optional[str]):
        return jsii.set(self, "iamInstanceProfile", value)

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instanceid
        """
        return jsii.get(self, "instanceId")

    @instance_id.setter
    def instance_id(self, value: typing.Optional[str]):
        return jsii.set(self, "instanceId", value)

    @property
    @jsii.member(jsii_name="instanceMonitoring")
    def instance_monitoring(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancemonitoring
        """
        return jsii.get(self, "instanceMonitoring")

    @instance_monitoring.setter
    def instance_monitoring(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "instanceMonitoring", value)

    @property
    @jsii.member(jsii_name="kernelId")
    def kernel_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.KernelId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-kernelid
        """
        return jsii.get(self, "kernelId")

    @kernel_id.setter
    def kernel_id(self, value: typing.Optional[str]):
        return jsii.set(self, "kernelId", value)

    @property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.KeyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-keyname
        """
        return jsii.get(self, "keyName")

    @key_name.setter
    def key_name(self, value: typing.Optional[str]):
        return jsii.set(self, "keyName", value)

    @property
    @jsii.member(jsii_name="launchConfigurationName")
    def launch_configuration_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-autoscaling-launchconfig-launchconfigurationname
        """
        return jsii.get(self, "launchConfigurationName")

    @launch_configuration_name.setter
    def launch_configuration_name(self, value: typing.Optional[str]):
        return jsii.set(self, "launchConfigurationName", value)

    @property
    @jsii.member(jsii_name="placementTenancy")
    def placement_tenancy(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-placementtenancy
        """
        return jsii.get(self, "placementTenancy")

    @placement_tenancy.setter
    def placement_tenancy(self, value: typing.Optional[str]):
        return jsii.set(self, "placementTenancy", value)

    @property
    @jsii.member(jsii_name="ramDiskId")
    def ram_disk_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ramdiskid
        """
        return jsii.get(self, "ramDiskId")

    @ram_disk_id.setter
    def ram_disk_id(self, value: typing.Optional[str]):
        return jsii.set(self, "ramDiskId", value)

    @property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter
    def security_groups(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "securityGroups", value)

    @property
    @jsii.member(jsii_name="spotPrice")
    def spot_price(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-spotprice
        """
        return jsii.get(self, "spotPrice")

    @spot_price.setter
    def spot_price(self, value: typing.Optional[str]):
        return jsii.set(self, "spotPrice", value)

    @property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.UserData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-userdata
        """
        return jsii.get(self, "userData")

    @user_data.setter
    def user_data(self, value: typing.Optional[str]):
        return jsii.set(self, "userData", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceMappingProperty", jsii_struct_bases=[], name_mapping={'device_name': 'deviceName', 'ebs': 'ebs', 'no_device': 'noDevice', 'virtual_name': 'virtualName'})
    class BlockDeviceMappingProperty():
        def __init__(self, *, device_name: str, ebs: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLaunchConfiguration.BlockDeviceProperty"]]]=None, no_device: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, virtual_name: typing.Optional[str]=None):
            """
            :param device_name: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.DeviceName``.
            :param ebs: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.Ebs``.
            :param no_device: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.NoDevice``.
            :param virtual_name: ``CfnLaunchConfiguration.BlockDeviceMappingProperty.VirtualName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html
            """
            self._values = {
                'device_name': device_name,
            }
            if ebs is not None: self._values["ebs"] = ebs
            if no_device is not None: self._values["no_device"] = no_device
            if virtual_name is not None: self._values["virtual_name"] = virtual_name

        @property
        def device_name(self) -> str:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.DeviceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-devicename
            """
            return self._values.get('device_name')

        @property
        def ebs(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLaunchConfiguration.BlockDeviceProperty"]]]:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.Ebs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-ebs
            """
            return self._values.get('ebs')

        @property
        def no_device(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.NoDevice``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-nodevice
            """
            return self._values.get('no_device')

        @property
        def virtual_name(self) -> typing.Optional[str]:
            """``CfnLaunchConfiguration.BlockDeviceMappingProperty.VirtualName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-virtualname
            """
            return self._values.get('virtual_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BlockDeviceMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceProperty", jsii_struct_bases=[], name_mapping={'delete_on_termination': 'deleteOnTermination', 'encrypted': 'encrypted', 'iops': 'iops', 'snapshot_id': 'snapshotId', 'volume_size': 'volumeSize', 'volume_type': 'volumeType'})
    class BlockDeviceProperty():
        def __init__(self, *, delete_on_termination: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, iops: typing.Optional[jsii.Number]=None, snapshot_id: typing.Optional[str]=None, volume_size: typing.Optional[jsii.Number]=None, volume_type: typing.Optional[str]=None):
            """
            :param delete_on_termination: ``CfnLaunchConfiguration.BlockDeviceProperty.DeleteOnTermination``.
            :param encrypted: ``CfnLaunchConfiguration.BlockDeviceProperty.Encrypted``.
            :param iops: ``CfnLaunchConfiguration.BlockDeviceProperty.Iops``.
            :param snapshot_id: ``CfnLaunchConfiguration.BlockDeviceProperty.SnapshotId``.
            :param volume_size: ``CfnLaunchConfiguration.BlockDeviceProperty.VolumeSize``.
            :param volume_type: ``CfnLaunchConfiguration.BlockDeviceProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html
            """
            self._values = {
            }
            if delete_on_termination is not None: self._values["delete_on_termination"] = delete_on_termination
            if encrypted is not None: self._values["encrypted"] = encrypted
            if iops is not None: self._values["iops"] = iops
            if snapshot_id is not None: self._values["snapshot_id"] = snapshot_id
            if volume_size is not None: self._values["volume_size"] = volume_size
            if volume_type is not None: self._values["volume_type"] = volume_type

        @property
        def delete_on_termination(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.DeleteOnTermination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-deleteonterm
            """
            return self._values.get('delete_on_termination')

        @property
        def encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.Encrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-encrypted
            """
            return self._values.get('encrypted')

        @property
        def iops(self) -> typing.Optional[jsii.Number]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.Iops``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-iops
            """
            return self._values.get('iops')

        @property
        def snapshot_id(self) -> typing.Optional[str]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.SnapshotId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-snapshotid
            """
            return self._values.get('snapshot_id')

        @property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.VolumeSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-volumesize
            """
            return self._values.get('volume_size')

        @property
        def volume_type(self) -> typing.Optional[str]:
            """``CfnLaunchConfiguration.BlockDeviceProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-volumetype
            """
            return self._values.get('volume_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BlockDeviceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfigurationProps", jsii_struct_bases=[], name_mapping={'image_id': 'imageId', 'instance_type': 'instanceType', 'associate_public_ip_address': 'associatePublicIpAddress', 'block_device_mappings': 'blockDeviceMappings', 'classic_link_vpc_id': 'classicLinkVpcId', 'classic_link_vpc_security_groups': 'classicLinkVpcSecurityGroups', 'ebs_optimized': 'ebsOptimized', 'iam_instance_profile': 'iamInstanceProfile', 'instance_id': 'instanceId', 'instance_monitoring': 'instanceMonitoring', 'kernel_id': 'kernelId', 'key_name': 'keyName', 'launch_configuration_name': 'launchConfigurationName', 'placement_tenancy': 'placementTenancy', 'ram_disk_id': 'ramDiskId', 'security_groups': 'securityGroups', 'spot_price': 'spotPrice', 'user_data': 'userData'})
class CfnLaunchConfigurationProps():
    def __init__(self, *, image_id: str, instance_type: str, associate_public_ip_address: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, block_device_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.BlockDeviceMappingProperty"]]]]]=None, classic_link_vpc_id: typing.Optional[str]=None, classic_link_vpc_security_groups: typing.Optional[typing.List[str]]=None, ebs_optimized: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, iam_instance_profile: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, instance_monitoring: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, kernel_id: typing.Optional[str]=None, key_name: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, placement_tenancy: typing.Optional[str]=None, ram_disk_id: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, spot_price: typing.Optional[str]=None, user_data: typing.Optional[str]=None):
        """Properties for defining a ``AWS::AutoScaling::LaunchConfiguration``.

        :param image_id: ``AWS::AutoScaling::LaunchConfiguration.ImageId``.
        :param instance_type: ``AWS::AutoScaling::LaunchConfiguration.InstanceType``.
        :param associate_public_ip_address: ``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.
        :param block_device_mappings: ``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.
        :param classic_link_vpc_id: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.
        :param classic_link_vpc_security_groups: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.
        :param ebs_optimized: ``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.
        :param iam_instance_profile: ``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.
        :param instance_id: ``AWS::AutoScaling::LaunchConfiguration.InstanceId``.
        :param instance_monitoring: ``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.
        :param kernel_id: ``AWS::AutoScaling::LaunchConfiguration.KernelId``.
        :param key_name: ``AWS::AutoScaling::LaunchConfiguration.KeyName``.
        :param launch_configuration_name: ``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.
        :param placement_tenancy: ``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.
        :param ram_disk_id: ``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.
        :param security_groups: ``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.
        :param spot_price: ``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.
        :param user_data: ``AWS::AutoScaling::LaunchConfiguration.UserData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
        """
        self._values = {
            'image_id': image_id,
            'instance_type': instance_type,
        }
        if associate_public_ip_address is not None: self._values["associate_public_ip_address"] = associate_public_ip_address
        if block_device_mappings is not None: self._values["block_device_mappings"] = block_device_mappings
        if classic_link_vpc_id is not None: self._values["classic_link_vpc_id"] = classic_link_vpc_id
        if classic_link_vpc_security_groups is not None: self._values["classic_link_vpc_security_groups"] = classic_link_vpc_security_groups
        if ebs_optimized is not None: self._values["ebs_optimized"] = ebs_optimized
        if iam_instance_profile is not None: self._values["iam_instance_profile"] = iam_instance_profile
        if instance_id is not None: self._values["instance_id"] = instance_id
        if instance_monitoring is not None: self._values["instance_monitoring"] = instance_monitoring
        if kernel_id is not None: self._values["kernel_id"] = kernel_id
        if key_name is not None: self._values["key_name"] = key_name
        if launch_configuration_name is not None: self._values["launch_configuration_name"] = launch_configuration_name
        if placement_tenancy is not None: self._values["placement_tenancy"] = placement_tenancy
        if ram_disk_id is not None: self._values["ram_disk_id"] = ram_disk_id
        if security_groups is not None: self._values["security_groups"] = security_groups
        if spot_price is not None: self._values["spot_price"] = spot_price
        if user_data is not None: self._values["user_data"] = user_data

    @property
    def image_id(self) -> str:
        """``AWS::AutoScaling::LaunchConfiguration.ImageId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-imageid
        """
        return self._values.get('image_id')

    @property
    def instance_type(self) -> str:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancetype
        """
        return self._values.get('instance_type')

    @property
    def associate_public_ip_address(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cf-as-launchconfig-associatepubip
        """
        return self._values.get('associate_public_ip_address')

    @property
    def block_device_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLaunchConfiguration.BlockDeviceMappingProperty"]]]]]:
        """``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-blockdevicemappings
        """
        return self._values.get('block_device_mappings')

    @property
    def classic_link_vpc_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcid
        """
        return self._values.get('classic_link_vpc_id')

    @property
    def classic_link_vpc_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcsecuritygroups
        """
        return self._values.get('classic_link_vpc_security_groups')

    @property
    def ebs_optimized(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ebsoptimized
        """
        return self._values.get('ebs_optimized')

    @property
    def iam_instance_profile(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-iaminstanceprofile
        """
        return self._values.get('iam_instance_profile')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instanceid
        """
        return self._values.get('instance_id')

    @property
    def instance_monitoring(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancemonitoring
        """
        return self._values.get('instance_monitoring')

    @property
    def kernel_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.KernelId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-kernelid
        """
        return self._values.get('kernel_id')

    @property
    def key_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.KeyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-keyname
        """
        return self._values.get('key_name')

    @property
    def launch_configuration_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-autoscaling-launchconfig-launchconfigurationname
        """
        return self._values.get('launch_configuration_name')

    @property
    def placement_tenancy(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-placementtenancy
        """
        return self._values.get('placement_tenancy')

    @property
    def ram_disk_id(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ramdiskid
        """
        return self._values.get('ram_disk_id')

    @property
    def security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-securitygroups
        """
        return self._values.get('security_groups')

    @property
    def spot_price(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-spotprice
        """
        return self._values.get('spot_price')

    @property
    def user_data(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LaunchConfiguration.UserData``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-userdata
        """
        return self._values.get('user_data')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLaunchConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLifecycleHook(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHook"):
    """A CloudFormation ``AWS::AutoScaling::LifecycleHook``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html
    cloudformationResource:
    :cloudformationResource:: AWS::AutoScaling::LifecycleHook
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group_name: str, lifecycle_transition: str, default_result: typing.Optional[str]=None, heartbeat_timeout: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, notification_target_arn: typing.Optional[str]=None, role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::AutoScaling::LifecycleHook``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param auto_scaling_group_name: ``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.
        :param lifecycle_transition: ``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.
        :param default_result: ``AWS::AutoScaling::LifecycleHook.DefaultResult``.
        :param heartbeat_timeout: ``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.
        :param lifecycle_hook_name: ``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.
        :param notification_metadata: ``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.
        :param notification_target_arn: ``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.
        :param role_arn: ``AWS::AutoScaling::LifecycleHook.RoleARN``.
        """
        props = CfnLifecycleHookProps(auto_scaling_group_name=auto_scaling_group_name, lifecycle_transition=lifecycle_transition, default_result=default_result, heartbeat_timeout=heartbeat_timeout, lifecycle_hook_name=lifecycle_hook_name, notification_metadata=notification_metadata, notification_target_arn=notification_target_arn, role_arn=role_arn)

        jsii.create(CfnLifecycleHook, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-autoscalinggroupname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter
    def auto_scaling_group_name(self, value: str):
        return jsii.set(self, "autoScalingGroupName", value)

    @property
    @jsii.member(jsii_name="lifecycleTransition")
    def lifecycle_transition(self) -> str:
        """``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-lifecycletransition
        """
        return jsii.get(self, "lifecycleTransition")

    @lifecycle_transition.setter
    def lifecycle_transition(self, value: str):
        return jsii.set(self, "lifecycleTransition", value)

    @property
    @jsii.member(jsii_name="defaultResult")
    def default_result(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.DefaultResult``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-defaultresult
        """
        return jsii.get(self, "defaultResult")

    @default_result.setter
    def default_result(self, value: typing.Optional[str]):
        return jsii.set(self, "defaultResult", value)

    @property
    @jsii.member(jsii_name="heartbeatTimeout")
    def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-heartbeattimeout
        """
        return jsii.get(self, "heartbeatTimeout")

    @heartbeat_timeout.setter
    def heartbeat_timeout(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "heartbeatTimeout", value)

    @property
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-autoscaling-lifecyclehook-lifecyclehookname
        """
        return jsii.get(self, "lifecycleHookName")

    @lifecycle_hook_name.setter
    def lifecycle_hook_name(self, value: typing.Optional[str]):
        return jsii.set(self, "lifecycleHookName", value)

    @property
    @jsii.member(jsii_name="notificationMetadata")
    def notification_metadata(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationmetadata
        """
        return jsii.get(self, "notificationMetadata")

    @notification_metadata.setter
    def notification_metadata(self, value: typing.Optional[str]):
        return jsii.set(self, "notificationMetadata", value)

    @property
    @jsii.member(jsii_name="notificationTargetArn")
    def notification_target_arn(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationtargetarn
        """
        return jsii.get(self, "notificationTargetArn")

    @notification_target_arn.setter
    def notification_target_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "notificationTargetArn", value)

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.RoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "roleArn", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHookProps", jsii_struct_bases=[], name_mapping={'auto_scaling_group_name': 'autoScalingGroupName', 'lifecycle_transition': 'lifecycleTransition', 'default_result': 'defaultResult', 'heartbeat_timeout': 'heartbeatTimeout', 'lifecycle_hook_name': 'lifecycleHookName', 'notification_metadata': 'notificationMetadata', 'notification_target_arn': 'notificationTargetArn', 'role_arn': 'roleArn'})
class CfnLifecycleHookProps():
    def __init__(self, *, auto_scaling_group_name: str, lifecycle_transition: str, default_result: typing.Optional[str]=None, heartbeat_timeout: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, notification_target_arn: typing.Optional[str]=None, role_arn: typing.Optional[str]=None):
        """Properties for defining a ``AWS::AutoScaling::LifecycleHook``.

        :param auto_scaling_group_name: ``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.
        :param lifecycle_transition: ``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.
        :param default_result: ``AWS::AutoScaling::LifecycleHook.DefaultResult``.
        :param heartbeat_timeout: ``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.
        :param lifecycle_hook_name: ``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.
        :param notification_metadata: ``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.
        :param notification_target_arn: ``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.
        :param role_arn: ``AWS::AutoScaling::LifecycleHook.RoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html
        """
        self._values = {
            'auto_scaling_group_name': auto_scaling_group_name,
            'lifecycle_transition': lifecycle_transition,
        }
        if default_result is not None: self._values["default_result"] = default_result
        if heartbeat_timeout is not None: self._values["heartbeat_timeout"] = heartbeat_timeout
        if lifecycle_hook_name is not None: self._values["lifecycle_hook_name"] = lifecycle_hook_name
        if notification_metadata is not None: self._values["notification_metadata"] = notification_metadata
        if notification_target_arn is not None: self._values["notification_target_arn"] = notification_target_arn
        if role_arn is not None: self._values["role_arn"] = role_arn

    @property
    def auto_scaling_group_name(self) -> str:
        """``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-autoscalinggroupname
        """
        return self._values.get('auto_scaling_group_name')

    @property
    def lifecycle_transition(self) -> str:
        """``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-lifecycletransition
        """
        return self._values.get('lifecycle_transition')

    @property
    def default_result(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.DefaultResult``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-defaultresult
        """
        return self._values.get('default_result')

    @property
    def heartbeat_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-heartbeattimeout
        """
        return self._values.get('heartbeat_timeout')

    @property
    def lifecycle_hook_name(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-autoscaling-lifecyclehook-lifecyclehookname
        """
        return self._values.get('lifecycle_hook_name')

    @property
    def notification_metadata(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationmetadata
        """
        return self._values.get('notification_metadata')

    @property
    def notification_target_arn(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationtargetarn
        """
        return self._values.get('notification_target_arn')

    @property
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::LifecycleHook.RoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-rolearn
        """
        return self._values.get('role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLifecycleHookProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScalingPolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy"):
    """A CloudFormation ``AWS::AutoScaling::ScalingPolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html
    cloudformationResource:
    :cloudformationResource:: AWS::AutoScaling::ScalingPolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group_name: str, adjustment_type: typing.Optional[str]=None, cooldown: typing.Optional[str]=None, estimated_instance_warmup: typing.Optional[jsii.Number]=None, metric_aggregation_type: typing.Optional[str]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, policy_type: typing.Optional[str]=None, scaling_adjustment: typing.Optional[jsii.Number]=None, step_adjustments: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StepAdjustmentProperty"]]]]]=None, target_tracking_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TargetTrackingConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::AutoScaling::ScalingPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param auto_scaling_group_name: ``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.
        :param adjustment_type: ``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.
        :param cooldown: ``AWS::AutoScaling::ScalingPolicy.Cooldown``.
        :param estimated_instance_warmup: ``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.
        :param metric_aggregation_type: ``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.
        :param min_adjustment_magnitude: ``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.
        :param policy_type: ``AWS::AutoScaling::ScalingPolicy.PolicyType``.
        :param scaling_adjustment: ``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.
        :param step_adjustments: ``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.
        :param target_tracking_configuration: ``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.
        """
        props = CfnScalingPolicyProps(auto_scaling_group_name=auto_scaling_group_name, adjustment_type=adjustment_type, cooldown=cooldown, estimated_instance_warmup=estimated_instance_warmup, metric_aggregation_type=metric_aggregation_type, min_adjustment_magnitude=min_adjustment_magnitude, policy_type=policy_type, scaling_adjustment=scaling_adjustment, step_adjustments=step_adjustments, target_tracking_configuration=target_tracking_configuration)

        jsii.create(CfnScalingPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-autoscalinggroupname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter
    def auto_scaling_group_name(self, value: str):
        return jsii.set(self, "autoScalingGroupName", value)

    @property
    @jsii.member(jsii_name="adjustmentType")
    def adjustment_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-adjustmenttype
        """
        return jsii.get(self, "adjustmentType")

    @adjustment_type.setter
    def adjustment_type(self, value: typing.Optional[str]):
        return jsii.set(self, "adjustmentType", value)

    @property
    @jsii.member(jsii_name="cooldown")
    def cooldown(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.Cooldown``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-cooldown
        """
        return jsii.get(self, "cooldown")

    @cooldown.setter
    def cooldown(self, value: typing.Optional[str]):
        return jsii.set(self, "cooldown", value)

    @property
    @jsii.member(jsii_name="estimatedInstanceWarmup")
    def estimated_instance_warmup(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-estimatedinstancewarmup
        """
        return jsii.get(self, "estimatedInstanceWarmup")

    @estimated_instance_warmup.setter
    def estimated_instance_warmup(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "estimatedInstanceWarmup", value)

    @property
    @jsii.member(jsii_name="metricAggregationType")
    def metric_aggregation_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-metricaggregationtype
        """
        return jsii.get(self, "metricAggregationType")

    @metric_aggregation_type.setter
    def metric_aggregation_type(self, value: typing.Optional[str]):
        return jsii.set(self, "metricAggregationType", value)

    @property
    @jsii.member(jsii_name="minAdjustmentMagnitude")
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-minadjustmentmagnitude
        """
        return jsii.get(self, "minAdjustmentMagnitude")

    @min_adjustment_magnitude.setter
    def min_adjustment_magnitude(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "minAdjustmentMagnitude", value)

    @property
    @jsii.member(jsii_name="policyType")
    def policy_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.PolicyType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-policytype
        """
        return jsii.get(self, "policyType")

    @policy_type.setter
    def policy_type(self, value: typing.Optional[str]):
        return jsii.set(self, "policyType", value)

    @property
    @jsii.member(jsii_name="scalingAdjustment")
    def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-scalingadjustment
        """
        return jsii.get(self, "scalingAdjustment")

    @scaling_adjustment.setter
    def scaling_adjustment(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "scalingAdjustment", value)

    @property
    @jsii.member(jsii_name="stepAdjustments")
    def step_adjustments(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StepAdjustmentProperty"]]]]]:
        """``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-stepadjustments
        """
        return jsii.get(self, "stepAdjustments")

    @step_adjustments.setter
    def step_adjustments(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StepAdjustmentProperty"]]]]]):
        return jsii.set(self, "stepAdjustments", value)

    @property
    @jsii.member(jsii_name="targetTrackingConfiguration")
    def target_tracking_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TargetTrackingConfigurationProperty"]]]:
        """``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration
        """
        return jsii.get(self, "targetTrackingConfiguration")

    @target_tracking_configuration.setter
    def target_tracking_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TargetTrackingConfigurationProperty"]]]):
        return jsii.set(self, "targetTrackingConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.CustomizedMetricSpecificationProperty", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'namespace': 'namespace', 'statistic': 'statistic', 'dimensions': 'dimensions', 'unit': 'unit'})
    class CustomizedMetricSpecificationProperty():
        def __init__(self, *, metric_name: str, namespace: str, statistic: str, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.MetricDimensionProperty"]]]]]=None, unit: typing.Optional[str]=None):
            """
            :param metric_name: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.
            :param namespace: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.
            :param statistic: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.
            :param dimensions: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Dimensions``.
            :param unit: ``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html
            """
            self._values = {
                'metric_name': metric_name,
                'namespace': namespace,
                'statistic': statistic,
            }
            if dimensions is not None: self._values["dimensions"] = dimensions
            if unit is not None: self._values["unit"] = unit

        @property
        def metric_name(self) -> str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-metricname
            """
            return self._values.get('metric_name')

        @property
        def namespace(self) -> str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-namespace
            """
            return self._values.get('namespace')

        @property
        def statistic(self) -> str:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-statistic
            """
            return self._values.get('statistic')

        @property
        def dimensions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.MetricDimensionProperty"]]]]]:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Dimensions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-dimensions
            """
            return self._values.get('dimensions')

        @property
        def unit(self) -> typing.Optional[str]:
            """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-unit
            """
            return self._values.get('unit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CustomizedMetricSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.MetricDimensionProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class MetricDimensionProperty():
        def __init__(self, *, name: str, value: str):
            """
            :param name: ``CfnScalingPolicy.MetricDimensionProperty.Name``.
            :param value: ``CfnScalingPolicy.MetricDimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html
            """
            self._values = {
                'name': name,
                'value': value,
            }

        @property
        def name(self) -> str:
            """``CfnScalingPolicy.MetricDimensionProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-name
            """
            return self._values.get('name')

        @property
        def value(self) -> str:
            """``CfnScalingPolicy.MetricDimensionProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricDimensionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty", jsii_struct_bases=[], name_mapping={'predefined_metric_type': 'predefinedMetricType', 'resource_label': 'resourceLabel'})
    class PredefinedMetricSpecificationProperty():
        def __init__(self, *, predefined_metric_type: str, resource_label: typing.Optional[str]=None):
            """
            :param predefined_metric_type: ``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.
            :param resource_label: ``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html
            """
            self._values = {
                'predefined_metric_type': predefined_metric_type,
            }
            if resource_label is not None: self._values["resource_label"] = resource_label

        @property
        def predefined_metric_type(self) -> str:
            """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-predefinedmetrictype
            """
            return self._values.get('predefined_metric_type')

        @property
        def resource_label(self) -> typing.Optional[str]:
            """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-resourcelabel
            """
            return self._values.get('resource_label')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PredefinedMetricSpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.StepAdjustmentProperty", jsii_struct_bases=[], name_mapping={'scaling_adjustment': 'scalingAdjustment', 'metric_interval_lower_bound': 'metricIntervalLowerBound', 'metric_interval_upper_bound': 'metricIntervalUpperBound'})
    class StepAdjustmentProperty():
        def __init__(self, *, scaling_adjustment: jsii.Number, metric_interval_lower_bound: typing.Optional[jsii.Number]=None, metric_interval_upper_bound: typing.Optional[jsii.Number]=None):
            """
            :param scaling_adjustment: ``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.
            :param metric_interval_lower_bound: ``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.
            :param metric_interval_upper_bound: ``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html
            """
            self._values = {
                'scaling_adjustment': scaling_adjustment,
            }
            if metric_interval_lower_bound is not None: self._values["metric_interval_lower_bound"] = metric_interval_lower_bound
            if metric_interval_upper_bound is not None: self._values["metric_interval_upper_bound"] = metric_interval_upper_bound

        @property
        def scaling_adjustment(self) -> jsii.Number:
            """``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-scalingadjustment
            """
            return self._values.get('scaling_adjustment')

        @property
        def metric_interval_lower_bound(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervallowerbound
            """
            return self._values.get('metric_interval_lower_bound')

        @property
        def metric_interval_upper_bound(self) -> typing.Optional[jsii.Number]:
            """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervalupperbound
            """
            return self._values.get('metric_interval_upper_bound')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StepAdjustmentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.TargetTrackingConfigurationProperty", jsii_struct_bases=[], name_mapping={'target_value': 'targetValue', 'customized_metric_specification': 'customizedMetricSpecification', 'disable_scale_in': 'disableScaleIn', 'predefined_metric_specification': 'predefinedMetricSpecification'})
    class TargetTrackingConfigurationProperty():
        def __init__(self, *, target_value: jsii.Number, customized_metric_specification: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.CustomizedMetricSpecificationProperty"]]]=None, disable_scale_in: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, predefined_metric_specification: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.PredefinedMetricSpecificationProperty"]]]=None):
            """
            :param target_value: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.TargetValue``.
            :param customized_metric_specification: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.CustomizedMetricSpecification``.
            :param disable_scale_in: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.DisableScaleIn``.
            :param predefined_metric_specification: ``CfnScalingPolicy.TargetTrackingConfigurationProperty.PredefinedMetricSpecification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html
            """
            self._values = {
                'target_value': target_value,
            }
            if customized_metric_specification is not None: self._values["customized_metric_specification"] = customized_metric_specification
            if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
            if predefined_metric_specification is not None: self._values["predefined_metric_specification"] = predefined_metric_specification

        @property
        def target_value(self) -> jsii.Number:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.TargetValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-targetvalue
            """
            return self._values.get('target_value')

        @property
        def customized_metric_specification(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.CustomizedMetricSpecificationProperty"]]]:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.CustomizedMetricSpecification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-customizedmetricspecification
            """
            return self._values.get('customized_metric_specification')

        @property
        def disable_scale_in(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.DisableScaleIn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-disablescalein
            """
            return self._values.get('disable_scale_in')

        @property
        def predefined_metric_specification(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.PredefinedMetricSpecificationProperty"]]]:
            """``CfnScalingPolicy.TargetTrackingConfigurationProperty.PredefinedMetricSpecification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-predefinedmetricspecification
            """
            return self._values.get('predefined_metric_specification')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetTrackingConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicyProps", jsii_struct_bases=[], name_mapping={'auto_scaling_group_name': 'autoScalingGroupName', 'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'metric_aggregation_type': 'metricAggregationType', 'min_adjustment_magnitude': 'minAdjustmentMagnitude', 'policy_type': 'policyType', 'scaling_adjustment': 'scalingAdjustment', 'step_adjustments': 'stepAdjustments', 'target_tracking_configuration': 'targetTrackingConfiguration'})
class CfnScalingPolicyProps():
    def __init__(self, *, auto_scaling_group_name: str, adjustment_type: typing.Optional[str]=None, cooldown: typing.Optional[str]=None, estimated_instance_warmup: typing.Optional[jsii.Number]=None, metric_aggregation_type: typing.Optional[str]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, policy_type: typing.Optional[str]=None, scaling_adjustment: typing.Optional[jsii.Number]=None, step_adjustments: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.StepAdjustmentProperty"]]]]]=None, target_tracking_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.TargetTrackingConfigurationProperty"]]]=None):
        """Properties for defining a ``AWS::AutoScaling::ScalingPolicy``.

        :param auto_scaling_group_name: ``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.
        :param adjustment_type: ``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.
        :param cooldown: ``AWS::AutoScaling::ScalingPolicy.Cooldown``.
        :param estimated_instance_warmup: ``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.
        :param metric_aggregation_type: ``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.
        :param min_adjustment_magnitude: ``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.
        :param policy_type: ``AWS::AutoScaling::ScalingPolicy.PolicyType``.
        :param scaling_adjustment: ``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.
        :param step_adjustments: ``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.
        :param target_tracking_configuration: ``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html
        """
        self._values = {
            'auto_scaling_group_name': auto_scaling_group_name,
        }
        if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
        if cooldown is not None: self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if metric_aggregation_type is not None: self._values["metric_aggregation_type"] = metric_aggregation_type
        if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude
        if policy_type is not None: self._values["policy_type"] = policy_type
        if scaling_adjustment is not None: self._values["scaling_adjustment"] = scaling_adjustment
        if step_adjustments is not None: self._values["step_adjustments"] = step_adjustments
        if target_tracking_configuration is not None: self._values["target_tracking_configuration"] = target_tracking_configuration

    @property
    def auto_scaling_group_name(self) -> str:
        """``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-autoscalinggroupname
        """
        return self._values.get('auto_scaling_group_name')

    @property
    def adjustment_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-adjustmenttype
        """
        return self._values.get('adjustment_type')

    @property
    def cooldown(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.Cooldown``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-cooldown
        """
        return self._values.get('cooldown')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-estimatedinstancewarmup
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def metric_aggregation_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-metricaggregationtype
        """
        return self._values.get('metric_aggregation_type')

    @property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-minadjustmentmagnitude
        """
        return self._values.get('min_adjustment_magnitude')

    @property
    def policy_type(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScalingPolicy.PolicyType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-policytype
        """
        return self._values.get('policy_type')

    @property
    def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-scalingadjustment
        """
        return self._values.get('scaling_adjustment')

    @property
    def step_adjustments(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnScalingPolicy.StepAdjustmentProperty"]]]]]:
        """``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-stepadjustments
        """
        return self._values.get('step_adjustments')

    @property
    def target_tracking_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnScalingPolicy.TargetTrackingConfigurationProperty"]]]:
        """``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration
        """
        return self._values.get('target_tracking_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScheduledAction(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledAction"):
    """A CloudFormation ``AWS::AutoScaling::ScheduledAction``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html
    cloudformationResource:
    :cloudformationResource:: AWS::AutoScaling::ScheduledAction
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group_name: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[str]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None, recurrence: typing.Optional[str]=None, start_time: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::AutoScaling::ScheduledAction``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param auto_scaling_group_name: ``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.
        :param desired_capacity: ``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.
        :param end_time: ``AWS::AutoScaling::ScheduledAction.EndTime``.
        :param max_size: ``AWS::AutoScaling::ScheduledAction.MaxSize``.
        :param min_size: ``AWS::AutoScaling::ScheduledAction.MinSize``.
        :param recurrence: ``AWS::AutoScaling::ScheduledAction.Recurrence``.
        :param start_time: ``AWS::AutoScaling::ScheduledAction.StartTime``.
        """
        props = CfnScheduledActionProps(auto_scaling_group_name=auto_scaling_group_name, desired_capacity=desired_capacity, end_time=end_time, max_size=max_size, min_size=min_size, recurrence=recurrence, start_time=start_time)

        jsii.create(CfnScheduledAction, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-asgname
        """
        return jsii.get(self, "autoScalingGroupName")

    @auto_scaling_group_name.setter
    def auto_scaling_group_name(self, value: str):
        return jsii.set(self, "autoScalingGroupName", value)

    @property
    @jsii.member(jsii_name="desiredCapacity")
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-desiredcapacity
        """
        return jsii.get(self, "desiredCapacity")

    @desired_capacity.setter
    def desired_capacity(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "desiredCapacity", value)

    @property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScheduledAction.EndTime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-endtime
        """
        return jsii.get(self, "endTime")

    @end_time.setter
    def end_time(self, value: typing.Optional[str]):
        return jsii.set(self, "endTime", value)

    @property
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MaxSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-maxsize
        """
        return jsii.get(self, "maxSize")

    @max_size.setter
    def max_size(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "maxSize", value)

    @property
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MinSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-minsize
        """
        return jsii.get(self, "minSize")

    @min_size.setter
    def min_size(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "minSize", value)

    @property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScheduledAction.Recurrence``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-recurrence
        """
        return jsii.get(self, "recurrence")

    @recurrence.setter
    def recurrence(self, value: typing.Optional[str]):
        return jsii.set(self, "recurrence", value)

    @property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScheduledAction.StartTime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-starttime
        """
        return jsii.get(self, "startTime")

    @start_time.setter
    def start_time(self, value: typing.Optional[str]):
        return jsii.set(self, "startTime", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledActionProps", jsii_struct_bases=[], name_mapping={'auto_scaling_group_name': 'autoScalingGroupName', 'desired_capacity': 'desiredCapacity', 'end_time': 'endTime', 'max_size': 'maxSize', 'min_size': 'minSize', 'recurrence': 'recurrence', 'start_time': 'startTime'})
class CfnScheduledActionProps():
    def __init__(self, *, auto_scaling_group_name: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[str]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None, recurrence: typing.Optional[str]=None, start_time: typing.Optional[str]=None):
        """Properties for defining a ``AWS::AutoScaling::ScheduledAction``.

        :param auto_scaling_group_name: ``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.
        :param desired_capacity: ``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.
        :param end_time: ``AWS::AutoScaling::ScheduledAction.EndTime``.
        :param max_size: ``AWS::AutoScaling::ScheduledAction.MaxSize``.
        :param min_size: ``AWS::AutoScaling::ScheduledAction.MinSize``.
        :param recurrence: ``AWS::AutoScaling::ScheduledAction.Recurrence``.
        :param start_time: ``AWS::AutoScaling::ScheduledAction.StartTime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html
        """
        self._values = {
            'auto_scaling_group_name': auto_scaling_group_name,
        }
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if end_time is not None: self._values["end_time"] = end_time
        if max_size is not None: self._values["max_size"] = max_size
        if min_size is not None: self._values["min_size"] = min_size
        if recurrence is not None: self._values["recurrence"] = recurrence
        if start_time is not None: self._values["start_time"] = start_time

    @property
    def auto_scaling_group_name(self) -> str:
        """``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-asgname
        """
        return self._values.get('auto_scaling_group_name')

    @property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-desiredcapacity
        """
        return self._values.get('desired_capacity')

    @property
    def end_time(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScheduledAction.EndTime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-endtime
        """
        return self._values.get('end_time')

    @property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MaxSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-maxsize
        """
        return self._values.get('max_size')

    @property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::AutoScaling::ScheduledAction.MinSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-minsize
        """
        return self._values.get('min_size')

    @property
    def recurrence(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScheduledAction.Recurrence``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-recurrence
        """
        return self._values.get('recurrence')

    @property
    def start_time(self) -> typing.Optional[str]:
        """``AWS::AutoScaling::ScheduledAction.StartTime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-starttime
        """
        return self._values.get('start_time')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnScheduledActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CommonAutoScalingGroupProps", jsii_struct_bases=[], name_mapping={'allow_all_outbound': 'allowAllOutbound', 'associate_public_ip_address': 'associatePublicIpAddress', 'cooldown': 'cooldown', 'desired_capacity': 'desiredCapacity', 'health_check': 'healthCheck', 'ignore_unmodified_size_properties': 'ignoreUnmodifiedSizeProperties', 'key_name': 'keyName', 'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'notifications_topic': 'notificationsTopic', 'replacing_update_min_successful_instances_percent': 'replacingUpdateMinSuccessfulInstancesPercent', 'resource_signal_count': 'resourceSignalCount', 'resource_signal_timeout': 'resourceSignalTimeout', 'rolling_update_configuration': 'rollingUpdateConfiguration', 'spot_price': 'spotPrice', 'update_type': 'updateType', 'vpc_subnets': 'vpcSubnets'})
class CommonAutoScalingGroupProps():
    def __init__(self, *, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional["RollingUpdateConfiguration"]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional["UpdateType"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None):
        """Basic properties of an AutoScalingGroup, except the exact machines to run and where they should run.

        Constructs that want to create AutoScalingGroups can inherit
        this interface and specialize the essential parts in various ways.

        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. Default: 1
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        """
        if isinstance(rolling_update_configuration, dict): rolling_update_configuration = RollingUpdateConfiguration(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
        }
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if associate_public_ip_address is not None: self._values["associate_public_ip_address"] = associate_public_ip_address
        if cooldown is not None: self._values["cooldown"] = cooldown
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if health_check is not None: self._values["health_check"] = health_check
        if ignore_unmodified_size_properties is not None: self._values["ignore_unmodified_size_properties"] = ignore_unmodified_size_properties
        if key_name is not None: self._values["key_name"] = key_name
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if min_capacity is not None: self._values["min_capacity"] = min_capacity
        if notifications_topic is not None: self._values["notifications_topic"] = notifications_topic
        if replacing_update_min_successful_instances_percent is not None: self._values["replacing_update_min_successful_instances_percent"] = replacing_update_min_successful_instances_percent
        if resource_signal_count is not None: self._values["resource_signal_count"] = resource_signal_count
        if resource_signal_timeout is not None: self._values["resource_signal_timeout"] = resource_signal_timeout
        if rolling_update_configuration is not None: self._values["rolling_update_configuration"] = rolling_update_configuration
        if spot_price is not None: self._values["spot_price"] = spot_price
        if update_type is not None: self._values["update_type"] = update_type
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether the instances can initiate connections to anywhere by default.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @property
    def associate_public_ip_address(self) -> typing.Optional[bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        default
        :default: - Use subnet setting.
        """
        return self._values.get('associate_public_ip_address')

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Default scaling cooldown for this AutoScalingGroup.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('cooldown')

    @property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of instances in the fleet.

        default
        :default: 1
        """
        return self._values.get('desired_capacity')

    @property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Configuration for health checks.

        default
        :default: - HealthCheck.ec2 with no grace period
        """
        return self._values.get('health_check')

    @property
    def ignore_unmodified_size_properties(self) -> typing.Optional[bool]:
        """If the ASG has scheduled actions, don't reset unchanged group sizes.

        Only used if the ASG has scheduled actions (which may scale your ASG up
        or down regardless of cdk deployments). If true, the size of the group
        will only be reset if it has been changed in the CDK app. If false, the
        sizes will always be changed back to what they were in the CDK app
        on deployment.

        default
        :default: true
        """
        return self._values.get('ignore_unmodified_size_properties')

    @property
    def key_name(self) -> typing.Optional[str]:
        """Name of SSH keypair to grant access to instances.

        default
        :default: - No SSH access will be possible.
        """
        return self._values.get('key_name')

    @property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        default
        :default: desiredCapacity
        """
        return self._values.get('max_capacity')

    @property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        default
        :default: 1
        """
        return self._values.get('min_capacity')

    @property
    def notifications_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """SNS topic to send notifications about fleet changes.

        default
        :default: - No fleet change notifications will be sent.
        """
        return self._values.get('notifications_topic')

    @property
    def replacing_update_min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Configuration for replacing updates.

        Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
        many instances must signal success for the update to succeed.

        default
        :default: minSuccessfulInstancesPercent
        """
        return self._values.get('replacing_update_min_successful_instances_percent')

    @property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        default
        :default: 1
        """
        return self._values.get('resource_signal_count')

    @property
    def resource_signal_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('resource_signal_timeout')

    @property
    def rolling_update_configuration(self) -> typing.Optional["RollingUpdateConfiguration"]:
        """Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        default
        :default: - RollingUpdateConfiguration with defaults.
        """
        return self._values.get('rolling_update_configuration')

    @property
    def spot_price(self) -> typing.Optional[str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        default
        :default: none
        """
        return self._values.get('spot_price')

    @property
    def update_type(self) -> typing.Optional["UpdateType"]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        default
        :default: UpdateType.None
        """
        return self._values.get('update_type')

    @property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place instances within the VPC.

        default
        :default: - All Private subnets.
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonAutoScalingGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroupProps", jsii_struct_bases=[CommonAutoScalingGroupProps], name_mapping={'allow_all_outbound': 'allowAllOutbound', 'associate_public_ip_address': 'associatePublicIpAddress', 'cooldown': 'cooldown', 'desired_capacity': 'desiredCapacity', 'health_check': 'healthCheck', 'ignore_unmodified_size_properties': 'ignoreUnmodifiedSizeProperties', 'key_name': 'keyName', 'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'notifications_topic': 'notificationsTopic', 'replacing_update_min_successful_instances_percent': 'replacingUpdateMinSuccessfulInstancesPercent', 'resource_signal_count': 'resourceSignalCount', 'resource_signal_timeout': 'resourceSignalTimeout', 'rolling_update_configuration': 'rollingUpdateConfiguration', 'spot_price': 'spotPrice', 'update_type': 'updateType', 'vpc_subnets': 'vpcSubnets', 'instance_type': 'instanceType', 'machine_image': 'machineImage', 'vpc': 'vpc', 'block_devices': 'blockDevices', 'role': 'role', 'user_data': 'userData'})
class AutoScalingGroupProps(CommonAutoScalingGroupProps):
    def __init__(self, *, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional["RollingUpdateConfiguration"]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional["UpdateType"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, instance_type: aws_cdk.aws_ec2.InstanceType, machine_image: aws_cdk.aws_ec2.IMachineImage, vpc: aws_cdk.aws_ec2.IVpc, block_devices: typing.Optional[typing.List["BlockDevice"]]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, user_data: typing.Optional[aws_cdk.aws_ec2.UserData]=None):
        """Properties of a Fleet.

        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. Default: 1
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        :param instance_type: Type of instance to launch.
        :param machine_image: AMI to launch.
        :param vpc: VPC to launch these instances in.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: A role will automatically be created, it can be accessed via the ``role`` property
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        """
        if isinstance(rolling_update_configuration, dict): rolling_update_configuration = RollingUpdateConfiguration(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'instance_type': instance_type,
            'machine_image': machine_image,
            'vpc': vpc,
        }
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if associate_public_ip_address is not None: self._values["associate_public_ip_address"] = associate_public_ip_address
        if cooldown is not None: self._values["cooldown"] = cooldown
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if health_check is not None: self._values["health_check"] = health_check
        if ignore_unmodified_size_properties is not None: self._values["ignore_unmodified_size_properties"] = ignore_unmodified_size_properties
        if key_name is not None: self._values["key_name"] = key_name
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if min_capacity is not None: self._values["min_capacity"] = min_capacity
        if notifications_topic is not None: self._values["notifications_topic"] = notifications_topic
        if replacing_update_min_successful_instances_percent is not None: self._values["replacing_update_min_successful_instances_percent"] = replacing_update_min_successful_instances_percent
        if resource_signal_count is not None: self._values["resource_signal_count"] = resource_signal_count
        if resource_signal_timeout is not None: self._values["resource_signal_timeout"] = resource_signal_timeout
        if rolling_update_configuration is not None: self._values["rolling_update_configuration"] = rolling_update_configuration
        if spot_price is not None: self._values["spot_price"] = spot_price
        if update_type is not None: self._values["update_type"] = update_type
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if block_devices is not None: self._values["block_devices"] = block_devices
        if role is not None: self._values["role"] = role
        if user_data is not None: self._values["user_data"] = user_data

    @property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether the instances can initiate connections to anywhere by default.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @property
    def associate_public_ip_address(self) -> typing.Optional[bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        default
        :default: - Use subnet setting.
        """
        return self._values.get('associate_public_ip_address')

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Default scaling cooldown for this AutoScalingGroup.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('cooldown')

    @property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of instances in the fleet.

        default
        :default: 1
        """
        return self._values.get('desired_capacity')

    @property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Configuration for health checks.

        default
        :default: - HealthCheck.ec2 with no grace period
        """
        return self._values.get('health_check')

    @property
    def ignore_unmodified_size_properties(self) -> typing.Optional[bool]:
        """If the ASG has scheduled actions, don't reset unchanged group sizes.

        Only used if the ASG has scheduled actions (which may scale your ASG up
        or down regardless of cdk deployments). If true, the size of the group
        will only be reset if it has been changed in the CDK app. If false, the
        sizes will always be changed back to what they were in the CDK app
        on deployment.

        default
        :default: true
        """
        return self._values.get('ignore_unmodified_size_properties')

    @property
    def key_name(self) -> typing.Optional[str]:
        """Name of SSH keypair to grant access to instances.

        default
        :default: - No SSH access will be possible.
        """
        return self._values.get('key_name')

    @property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        default
        :default: desiredCapacity
        """
        return self._values.get('max_capacity')

    @property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        default
        :default: 1
        """
        return self._values.get('min_capacity')

    @property
    def notifications_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """SNS topic to send notifications about fleet changes.

        default
        :default: - No fleet change notifications will be sent.
        """
        return self._values.get('notifications_topic')

    @property
    def replacing_update_min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Configuration for replacing updates.

        Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
        many instances must signal success for the update to succeed.

        default
        :default: minSuccessfulInstancesPercent
        """
        return self._values.get('replacing_update_min_successful_instances_percent')

    @property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        default
        :default: 1
        """
        return self._values.get('resource_signal_count')

    @property
    def resource_signal_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('resource_signal_timeout')

    @property
    def rolling_update_configuration(self) -> typing.Optional["RollingUpdateConfiguration"]:
        """Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        default
        :default: - RollingUpdateConfiguration with defaults.
        """
        return self._values.get('rolling_update_configuration')

    @property
    def spot_price(self) -> typing.Optional[str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        default
        :default: none
        """
        return self._values.get('spot_price')

    @property
    def update_type(self) -> typing.Optional["UpdateType"]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        default
        :default: UpdateType.None
        """
        return self._values.get('update_type')

    @property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place instances within the VPC.

        default
        :default: - All Private subnets.
        """
        return self._values.get('vpc_subnets')

    @property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """Type of instance to launch."""
        return self._values.get('instance_type')

    @property
    def machine_image(self) -> aws_cdk.aws_ec2.IMachineImage:
        """AMI to launch."""
        return self._values.get('machine_image')

    @property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch these instances in."""
        return self._values.get('vpc')

    @property
    def block_devices(self) -> typing.Optional[typing.List["BlockDevice"]]:
        """Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        default
        :default: - Uses the block device mapping of the AMI

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        """
        return self._values.get('block_devices')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role to associate with the instance profile assigned to this Auto Scaling Group.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        default
        :default: A role will automatically be created, it can be accessed via the ``role`` property

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            role = iam.Role(self, "MyRole",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
            )
        """
        return self._values.get('role')

    @property
    def user_data(self) -> typing.Optional[aws_cdk.aws_ec2.UserData]:
        """Specific UserData to use.

        The UserData may still be mutated after creation.

        default
        :default:

        - A UserData object appropriate for the MachineImage's
          Operating System is created.
        """
        return self._values.get('user_data')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AutoScalingGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CpuUtilizationScalingProps", jsii_struct_bases=[BaseTargetTrackingProps], name_mapping={'cooldown': 'cooldown', 'disable_scale_in': 'disableScaleIn', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'target_utilization_percent': 'targetUtilizationPercent'})
class CpuUtilizationScalingProps(BaseTargetTrackingProps):
    def __init__(self, *, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, target_utilization_percent: jsii.Number):
        """Properties for enabling scaling based on CPU utilization.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_utilization_percent: Target average CPU utilization across the task.
        """
        self._values = {
            'target_utilization_percent': target_utilization_percent,
        }
        if cooldown is not None: self._values["cooldown"] = cooldown
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        return self._values.get('cooldown')

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: - Same as the cooldown.
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def target_utilization_percent(self) -> jsii.Number:
        """Target average CPU utilization across the task."""
        return self._values.get('target_utilization_percent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CpuUtilizationScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CronOptions", jsii_struct_bases=[], name_mapping={'day': 'day', 'hour': 'hour', 'minute': 'minute', 'month': 'month', 'week_day': 'weekDay'})
class CronOptions():
    def __init__(self, *, day: typing.Optional[str]=None, hour: typing.Optional[str]=None, minute: typing.Optional[str]=None, month: typing.Optional[str]=None, week_day: typing.Optional[str]=None):
        """Options to configure a cron expression.

        All fields are strings so you can use complex expresions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week

        see
        :see: http://crontab.org/
        """
        self._values = {
        }
        if day is not None: self._values["day"] = day
        if hour is not None: self._values["hour"] = hour
        if minute is not None: self._values["minute"] = minute
        if month is not None: self._values["month"] = month
        if week_day is not None: self._values["week_day"] = week_day

    @property
    def day(self) -> typing.Optional[str]:
        """The day of the month to run this rule at.

        default
        :default: - Every day of the month
        """
        return self._values.get('day')

    @property
    def hour(self) -> typing.Optional[str]:
        """The hour to run this rule at.

        default
        :default: - Every hour
        """
        return self._values.get('hour')

    @property
    def minute(self) -> typing.Optional[str]:
        """The minute to run this rule at.

        default
        :default: - Every minute
        """
        return self._values.get('minute')

    @property
    def month(self) -> typing.Optional[str]:
        """The month to run this rule at.

        default
        :default: - Every month
        """
        return self._values.get('month')

    @property
    def week_day(self) -> typing.Optional[str]:
        """The day of the week to run this rule at.

        default
        :default: - Any day of the week
        """
        return self._values.get('week_day')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CronOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.DefaultResult")
class DefaultResult(enum.Enum):
    CONTINUE = "CONTINUE"
    ABANDON = "ABANDON"

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceOptionsBase", jsii_struct_bases=[], name_mapping={'delete_on_termination': 'deleteOnTermination', 'iops': 'iops', 'volume_type': 'volumeType'})
class EbsDeviceOptionsBase():
    def __init__(self, *, delete_on_termination: typing.Optional[bool]=None, iops: typing.Optional[jsii.Number]=None, volume_type: typing.Optional["EbsDeviceVolumeType"]=None):
        """
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume.
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        """
        self._values = {
        }
        if delete_on_termination is not None: self._values["delete_on_termination"] = delete_on_termination
        if iops is not None: self._values["iops"] = iops
        if volume_type is not None: self._values["volume_type"] = volume_type

    @property
    def delete_on_termination(self) -> typing.Optional[bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        default
        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        return self._values.get('delete_on_termination')

    @property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('iops')

    @property
    def volume_type(self) -> typing.Optional["EbsDeviceVolumeType"]:
        """The EBS volume type.

        default
        :default: {@link EbsDeviceVolumeType.GP2}

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('volume_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EbsDeviceOptionsBase(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceOptions", jsii_struct_bases=[EbsDeviceOptionsBase], name_mapping={'delete_on_termination': 'deleteOnTermination', 'iops': 'iops', 'volume_type': 'volumeType', 'encrypted': 'encrypted'})
class EbsDeviceOptions(EbsDeviceOptionsBase):
    def __init__(self, *, delete_on_termination: typing.Optional[bool]=None, iops: typing.Optional[jsii.Number]=None, volume_type: typing.Optional["EbsDeviceVolumeType"]=None, encrypted: typing.Optional[bool]=None):
        """
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume.
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        :param encrypted: Specifies whether the EBS volume is encrypted. Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption. Default: false
        """
        self._values = {
        }
        if delete_on_termination is not None: self._values["delete_on_termination"] = delete_on_termination
        if iops is not None: self._values["iops"] = iops
        if volume_type is not None: self._values["volume_type"] = volume_type
        if encrypted is not None: self._values["encrypted"] = encrypted

    @property
    def delete_on_termination(self) -> typing.Optional[bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        default
        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        return self._values.get('delete_on_termination')

    @property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('iops')

    @property
    def volume_type(self) -> typing.Optional["EbsDeviceVolumeType"]:
        """The EBS volume type.

        default
        :default: {@link EbsDeviceVolumeType.GP2}

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('volume_type')

    @property
    def encrypted(self) -> typing.Optional[bool]:
        """Specifies whether the EBS volume is encrypted. Encrypted EBS volumes can only be attached to instances that support Amazon EBS encryption.

        default
        :default: false

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html#EBSEncryption_supported_instances
        """
        return self._values.get('encrypted')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EbsDeviceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceSnapshotOptions", jsii_struct_bases=[EbsDeviceOptionsBase], name_mapping={'delete_on_termination': 'deleteOnTermination', 'iops': 'iops', 'volume_type': 'volumeType', 'volume_size': 'volumeSize'})
class EbsDeviceSnapshotOptions(EbsDeviceOptionsBase):
    def __init__(self, *, delete_on_termination: typing.Optional[bool]=None, iops: typing.Optional[jsii.Number]=None, volume_type: typing.Optional["EbsDeviceVolumeType"]=None, volume_size: typing.Optional[jsii.Number]=None):
        """
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume.
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        :param volume_size: The volume size, in Gibibytes (GiB). If you specify volumeSize, it must be equal or greater than the size of the snapshot. Default: - The snapshot size
        """
        self._values = {
        }
        if delete_on_termination is not None: self._values["delete_on_termination"] = delete_on_termination
        if iops is not None: self._values["iops"] = iops
        if volume_type is not None: self._values["volume_type"] = volume_type
        if volume_size is not None: self._values["volume_size"] = volume_size

    @property
    def delete_on_termination(self) -> typing.Optional[bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        default
        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        return self._values.get('delete_on_termination')

    @property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('iops')

    @property
    def volume_type(self) -> typing.Optional["EbsDeviceVolumeType"]:
        """The EBS volume type.

        default
        :default: {@link EbsDeviceVolumeType.GP2}

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('volume_type')

    @property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        """The volume size, in Gibibytes (GiB).

        If you specify volumeSize, it must be equal or greater than the size of the snapshot.

        default
        :default: - The snapshot size
        """
        return self._values.get('volume_size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EbsDeviceSnapshotOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceProps", jsii_struct_bases=[EbsDeviceSnapshotOptions], name_mapping={'delete_on_termination': 'deleteOnTermination', 'iops': 'iops', 'volume_type': 'volumeType', 'volume_size': 'volumeSize', 'snapshot_id': 'snapshotId'})
class EbsDeviceProps(EbsDeviceSnapshotOptions):
    def __init__(self, *, delete_on_termination: typing.Optional[bool]=None, iops: typing.Optional[jsii.Number]=None, volume_type: typing.Optional["EbsDeviceVolumeType"]=None, volume_size: typing.Optional[jsii.Number]=None, snapshot_id: typing.Optional[str]=None):
        """
        :param delete_on_termination: Indicates whether to delete the volume when the instance is terminated. Default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        :param iops: The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1} The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume.
        :param volume_type: The EBS volume type. Default: {@link EbsDeviceVolumeType.GP2}
        :param volume_size: The volume size, in Gibibytes (GiB). If you specify volumeSize, it must be equal or greater than the size of the snapshot. Default: - The snapshot size
        :param snapshot_id: 
        """
        self._values = {
        }
        if delete_on_termination is not None: self._values["delete_on_termination"] = delete_on_termination
        if iops is not None: self._values["iops"] = iops
        if volume_type is not None: self._values["volume_type"] = volume_type
        if volume_size is not None: self._values["volume_size"] = volume_size
        if snapshot_id is not None: self._values["snapshot_id"] = snapshot_id

    @property
    def delete_on_termination(self) -> typing.Optional[bool]:
        """Indicates whether to delete the volume when the instance is terminated.

        default
        :default: - true for Amazon EC2 Auto Scaling, false otherwise (e.g. EBS)
        """
        return self._values.get('delete_on_termination')

    @property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for {@link volumeType}: {@link EbsDeviceVolumeType.IO1}

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('iops')

    @property
    def volume_type(self) -> typing.Optional["EbsDeviceVolumeType"]:
        """The EBS volume type.

        default
        :default: {@link EbsDeviceVolumeType.GP2}

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        """
        return self._values.get('volume_type')

    @property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        """The volume size, in Gibibytes (GiB).

        If you specify volumeSize, it must be equal or greater than the size of the snapshot.

        default
        :default: - The snapshot size
        """
        return self._values.get('volume_size')

    @property
    def snapshot_id(self) -> typing.Optional[str]:
        return self._values.get('snapshot_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EbsDeviceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.EbsDeviceVolumeType")
class EbsDeviceVolumeType(enum.Enum):
    """Supported EBS volume types for {@link AutoScalingGroupProps.blockDevices}."""
    STANDARD = "STANDARD"
    """Magnetic."""
    IO1 = "IO1"
    """Provisioned IOPS SSD."""
    GP2 = "GP2"
    """General Purpose SSD."""
    ST1 = "ST1"
    """Throughput Optimized HDD."""
    SC1 = "SC1"
    """Cold HDD."""

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.Ec2HealthCheckOptions", jsii_struct_bases=[], name_mapping={'grace': 'grace'})
class Ec2HealthCheckOptions():
    def __init__(self, *, grace: typing.Optional[aws_cdk.core.Duration]=None):
        """EC2 Heath check options.

        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. Default: Duration.seconds(0)
        """
        self._values = {
        }
        if grace is not None: self._values["grace"] = grace

    @property
    def grace(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service.

        default
        :default: Duration.seconds(0)
        """
        return self._values.get('grace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ec2HealthCheckOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.ElbHealthCheckOptions", jsii_struct_bases=[], name_mapping={'grace': 'grace'})
class ElbHealthCheckOptions():
    def __init__(self, *, grace: aws_cdk.core.Duration):
        """ELB Heath check options.

        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. This option is required for ELB health checks.
        """
        self._values = {
            'grace': grace,
        }

    @property
    def grace(self) -> aws_cdk.core.Duration:
        """Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service.

        This option is required for ELB health checks.
        """
        return self._values.get('grace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ElbHealthCheckOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class HealthCheck(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.HealthCheck"):
    """Health check settings."""
    @jsii.member(jsii_name="ec2")
    @classmethod
    def ec2(cls, *, grace: typing.Optional[aws_cdk.core.Duration]=None) -> "HealthCheck":
        """Use EC2 for health checks.

        :param options: EC2 health check options.
        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. Default: Duration.seconds(0)
        """
        options = Ec2HealthCheckOptions(grace=grace)

        return jsii.sinvoke(cls, "ec2", [options])

    @jsii.member(jsii_name="elb")
    @classmethod
    def elb(cls, *, grace: aws_cdk.core.Duration) -> "HealthCheck":
        """Use ELB for health checks. It considers the instance unhealthy if it fails either the EC2 status checks or the load balancer health checks.

        :param options: ELB health check options.
        :param grace: Specified the time Auto Scaling waits before checking the health status of an EC2 instance that has come into service. This option is required for ELB health checks.
        """
        options = ElbHealthCheckOptions(grace=grace)

        return jsii.sinvoke(cls, "elb", [options])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")

    @property
    @jsii.member(jsii_name="gracePeriod")
    def grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        return jsii.get(self, "gracePeriod")


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.IAutoScalingGroup")
class IAutoScalingGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    """An AutoScalingGroup."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IAutoScalingGroupProxy

    @property
    @jsii.member(jsii_name="autoScalingGroupArn")
    def auto_scaling_group_arn(self) -> str:
        """The arn of the AutoScalingGroup.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """The name of the AutoScalingGroup.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: "ILifecycleHookTarget", default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout: typing.Optional[aws_cdk.core.Duration]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        :param id: -
        :param props: -
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        ...

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        :param id: -
        :param props: -
        :param target_utilization_percent: Target average CPU utilization across the task.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        :param id: -
        :param props: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        :param id: -
        :param props: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        ...

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        :param id: -
        :param props: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: "Schedule", desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        """Scale out or in based on time.

        :param id: -
        :param props: -
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        ...

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, target_value: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param props: -
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...


class _IAutoScalingGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """An AutoScalingGroup."""
    __jsii_type__ = "@aws-cdk/aws-autoscaling.IAutoScalingGroup"
    @property
    @jsii.member(jsii_name="autoScalingGroupArn")
    def auto_scaling_group_arn(self) -> str:
        """The arn of the AutoScalingGroup.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "autoScalingGroupArn")

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """The name of the AutoScalingGroup.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "autoScalingGroupName")

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: "ILifecycleHookTarget", default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout: typing.Optional[aws_cdk.core.Duration]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        :param id: -
        :param props: -
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props = BasicLifecycleHookProps(lifecycle_transition=lifecycle_transition, notification_target=notification_target, default_result=default_result, heartbeat_timeout=heartbeat_timeout, lifecycle_hook_name=lifecycle_hook_name, notification_metadata=notification_metadata, role=role)

        return jsii.invoke(self, "addLifecycleHook", [id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        :param id: -
        :param props: -
        :param target_utilization_percent: Target average CPU utilization across the task.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = CpuUtilizationScalingProps(target_utilization_percent=target_utilization_percent, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        :param id: -
        :param props: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(target_bytes_per_second=target_bytes_per_second, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        :param id: -
        :param props: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = BasicStepScalingPolicyProps(metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, estimated_instance_warmup=estimated_instance_warmup, min_adjustment_magnitude=min_adjustment_magnitude)

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        :param id: -
        :param props: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(target_bytes_per_second=target_bytes_per_second, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: "Schedule", desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        """Scale out or in based on time.

        :param id: -
        :param props: -
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props = BasicScheduledActionProps(schedule=schedule, desired_capacity=desired_capacity, end_time=end_time, max_capacity=max_capacity, min_capacity=min_capacity, start_time=start_time)

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, target_value: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param props: -
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = MetricTargetTrackingProps(metric=metric, target_value=target_value, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])


@jsii.implements(aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget, aws_cdk.aws_iam.IGrantable, IAutoScalingGroup)
class AutoScalingGroup(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroup"):
    """A Fleet represents a managed set of EC2 instances.

    The Fleet models a number of AutoScalingGroups, a launch configuration, a
    security group and an instance role.

    It allows adding arbitrary commands to the startup scripts of the instances
    in the fleet.

    The ASG spans all availability zones.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, machine_image: aws_cdk.aws_ec2.IMachineImage, vpc: aws_cdk.aws_ec2.IVpc, block_devices: typing.Optional[typing.List["BlockDevice"]]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, user_data: typing.Optional[aws_cdk.aws_ec2.UserData]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional["RollingUpdateConfiguration"]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional["UpdateType"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param instance_type: Type of instance to launch.
        :param machine_image: AMI to launch.
        :param vpc: VPC to launch these instances in.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: A role will automatically be created, it can be accessed via the ``role`` property
        :param user_data: Specific UserData to use. The UserData may still be mutated after creation. Default: - A UserData object appropriate for the MachineImage's Operating System is created.
        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. Default: 1
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        """
        props = AutoScalingGroupProps(instance_type=instance_type, machine_image=machine_image, vpc=vpc, block_devices=block_devices, role=role, user_data=user_data, allow_all_outbound=allow_all_outbound, associate_public_ip_address=associate_public_ip_address, cooldown=cooldown, desired_capacity=desired_capacity, health_check=health_check, ignore_unmodified_size_properties=ignore_unmodified_size_properties, key_name=key_name, max_capacity=max_capacity, min_capacity=min_capacity, notifications_topic=notifications_topic, replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent, resource_signal_count=resource_signal_count, resource_signal_timeout=resource_signal_timeout, rolling_update_configuration=rolling_update_configuration, spot_price=spot_price, update_type=update_type, vpc_subnets=vpc_subnets)

        jsii.create(AutoScalingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromAutoScalingGroupName")
    @classmethod
    def from_auto_scaling_group_name(cls, scope: aws_cdk.core.Construct, id: str, auto_scaling_group_name: str) -> "IAutoScalingGroup":
        """
        :param scope: -
        :param id: -
        :param auto_scaling_group_name: -
        """
        return jsii.sinvoke(cls, "fromAutoScalingGroupName", [scope, id, auto_scaling_group_name])

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: "ILifecycleHookTarget", default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout: typing.Optional[aws_cdk.core.Duration]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        :param id: -
        :param props: -
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props = BasicLifecycleHookProps(lifecycle_transition=lifecycle_transition, notification_target=notification_target, default_result=default_result, heartbeat_timeout=heartbeat_timeout, lifecycle_hook_name=lifecycle_hook_name, notification_metadata=notification_metadata, role=role)

        return jsii.invoke(self, "addLifecycleHook", [id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(self, security_group: aws_cdk.aws_ec2.ISecurityGroup) -> None:
        """Add the security group to all instances via the launch configuration security groups array.

        :param security_group: : The security group to add.
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM role assumed by instances of this fleet.

        :param statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *commands: str) -> None:
        """Add command to the startup script of fleet instances. The command must be in the scripting language supported by the fleet's OS (i.e. Linux/Windows).

        :param commands: -
        """
        return jsii.invoke(self, "addUserData", [*commands])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Attach to ELBv2 Application Target Group.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> None:
        """Attach to a classic load balancer.

        :param load_balancer: -
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Attach to ELBv2 Application Target Group.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        :param id: -
        :param props: -
        :param target_utilization_percent: Target average CPU utilization across the task.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = CpuUtilizationScalingProps(target_utilization_percent=target_utilization_percent, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        :param id: -
        :param props: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(target_bytes_per_second=target_bytes_per_second, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        :param id: -
        :param props: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = BasicStepScalingPolicyProps(metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, estimated_instance_warmup=estimated_instance_warmup, min_adjustment_magnitude=min_adjustment_magnitude)

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        :param id: -
        :param props: -
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = NetworkUtilizationScalingProps(target_bytes_per_second=target_bytes_per_second, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(self, id: str, *, target_requests_per_second: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target request handling rate.

        The AutoScalingGroup must have been attached to an Application Load Balancer
        in order to be able to call this.

        :param id: -
        :param props: -
        :param target_requests_per_second: Target average requests/seconds on each instance.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = RequestCountScalingProps(target_requests_per_second=target_requests_per_second, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: "Schedule", desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        """Scale out or in based on time.

        :param id: -
        :param props: -
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props = BasicScheduledActionProps(schedule=schedule, desired_capacity=desired_capacity, end_time=end_time, max_capacity=max_capacity, min_capacity=min_capacity, start_time=start_time)

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, target_value: jsii.Number, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        :param id: -
        :param props: -
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = MetricTargetTrackingProps(metric=metric, target_value=target_value, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])

    @property
    @jsii.member(jsii_name="autoScalingGroupArn")
    def auto_scaling_group_arn(self) -> str:
        """Arn of the AutoScalingGroup."""
        return jsii.get(self, "autoScalingGroupArn")

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """Name of the AutoScalingGroup."""
        return jsii.get(self, "autoScalingGroupName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Allows specify security group connections for instances of this fleet."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> aws_cdk.aws_ec2.OperatingSystemType:
        """The type of OS instances of this fleet are running."""
        return jsii.get(self, "osType")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The IAM role assumed by instances of this fleet."""
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> aws_cdk.aws_ec2.UserData:
        """UserData for the instances."""
        return jsii.get(self, "userData")

    @property
    @jsii.member(jsii_name="spotPrice")
    def spot_price(self) -> typing.Optional[str]:
        """The maximum spot price configured for thie autoscaling group.

        ``undefined``
        indicates that this group uses on-demand capacity.
        """
        return jsii.get(self, "spotPrice")

    @property
    @jsii.member(jsii_name="albTargetGroup")
    def _alb_target_group(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup]:
        return jsii.get(self, "albTargetGroup")

    @_alb_target_group.setter
    def _alb_target_group(self, value: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup]):
        return jsii.set(self, "albTargetGroup", value)


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.ILifecycleHook")
class ILifecycleHook(aws_cdk.core.IResource, jsii.compat.Protocol):
    """A basic lifecycle hook object."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookProxy

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role for the lifecycle hook to execute."""
        ...


class _ILifecycleHookProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """A basic lifecycle hook object."""
    __jsii_type__ = "@aws-cdk/aws-autoscaling.ILifecycleHook"
    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role for the lifecycle hook to execute."""
        return jsii.get(self, "role")


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.ILifecycleHookTarget")
class ILifecycleHookTarget(jsii.compat.Protocol):
    """Interface for autoscaling lifecycle hook targets."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookTargetProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, lifecycle_hook: "ILifecycleHook") -> "LifecycleHookTargetConfig":
        """Called when this object is used as the target of a lifecycle hook.

        :param scope: -
        :param lifecycle_hook: -
        """
        ...


class _ILifecycleHookTargetProxy():
    """Interface for autoscaling lifecycle hook targets."""
    __jsii_type__ = "@aws-cdk/aws-autoscaling.ILifecycleHookTarget"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, lifecycle_hook: "ILifecycleHook") -> "LifecycleHookTargetConfig":
        """Called when this object is used as the target of a lifecycle hook.

        :param scope: -
        :param lifecycle_hook: -
        """
        return jsii.invoke(self, "bind", [scope, lifecycle_hook])


@jsii.implements(ILifecycleHook)
class LifecycleHook(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.LifecycleHook"):
    """Define a life cycle hook."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", lifecycle_transition: "LifecycleTransition", notification_target: "ILifecycleHookTarget", default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout: typing.Optional[aws_cdk.core.Duration]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param auto_scaling_group: The AutoScalingGroup to add the lifecycle hook to.
        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props = LifecycleHookProps(auto_scaling_group=auto_scaling_group, lifecycle_transition=lifecycle_transition, notification_target=notification_target, default_result=default_result, heartbeat_timeout=heartbeat_timeout, lifecycle_hook_name=lifecycle_hook_name, notification_metadata=notification_metadata, role=role)

        jsii.create(LifecycleHook, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> str:
        """The name of this lifecycle hook.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "lifecycleHookName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role that allows the ASG to publish to the notification target."""
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.LifecycleHookProps", jsii_struct_bases=[BasicLifecycleHookProps], name_mapping={'lifecycle_transition': 'lifecycleTransition', 'notification_target': 'notificationTarget', 'default_result': 'defaultResult', 'heartbeat_timeout': 'heartbeatTimeout', 'lifecycle_hook_name': 'lifecycleHookName', 'notification_metadata': 'notificationMetadata', 'role': 'role', 'auto_scaling_group': 'autoScalingGroup'})
class LifecycleHookProps(BasicLifecycleHookProps):
    def __init__(self, *, lifecycle_transition: "LifecycleTransition", notification_target: "ILifecycleHookTarget", default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout: typing.Optional[aws_cdk.core.Duration]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, auto_scaling_group: "IAutoScalingGroup"):
        """Properties for a Lifecycle hook.

        :param lifecycle_transition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
        :param notification_target: The target of the lifecycle hook.
        :param default_result: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
        :param heartbeat_timeout: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
        :param lifecycle_hook_name: Name of the lifecycle hook. Default: - Automatically generated name.
        :param notification_metadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
        :param role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        :param auto_scaling_group: The AutoScalingGroup to add the lifecycle hook to.
        """
        self._values = {
            'lifecycle_transition': lifecycle_transition,
            'notification_target': notification_target,
            'auto_scaling_group': auto_scaling_group,
        }
        if default_result is not None: self._values["default_result"] = default_result
        if heartbeat_timeout is not None: self._values["heartbeat_timeout"] = heartbeat_timeout
        if lifecycle_hook_name is not None: self._values["lifecycle_hook_name"] = lifecycle_hook_name
        if notification_metadata is not None: self._values["notification_metadata"] = notification_metadata
        if role is not None: self._values["role"] = role

    @property
    def lifecycle_transition(self) -> "LifecycleTransition":
        """The state of the Amazon EC2 instance to which you want to attach the lifecycle hook."""
        return self._values.get('lifecycle_transition')

    @property
    def notification_target(self) -> "ILifecycleHookTarget":
        """The target of the lifecycle hook."""
        return self._values.get('notification_target')

    @property
    def default_result(self) -> typing.Optional["DefaultResult"]:
        """The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs.

        default
        :default: Continue
        """
        return self._values.get('default_result')

    @property
    def heartbeat_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum time between calls to RecordLifecycleActionHeartbeat for the hook.

        If the lifecycle hook times out, perform the action in DefaultResult.

        default
        :default: - No heartbeat timeout.
        """
        return self._values.get('heartbeat_timeout')

    @property
    def lifecycle_hook_name(self) -> typing.Optional[str]:
        """Name of the lifecycle hook.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('lifecycle_hook_name')

    @property
    def notification_metadata(self) -> typing.Optional[str]:
        """Additional data to pass to the lifecycle hook target.

        default
        :default: - No metadata.
        """
        return self._values.get('notification_metadata')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The role that allows publishing to the notification target.

        default
        :default: - A role is automatically created.
        """
        return self._values.get('role')

    @property
    def auto_scaling_group(self) -> "IAutoScalingGroup":
        """The AutoScalingGroup to add the lifecycle hook to."""
        return self._values.get('auto_scaling_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LifecycleHookProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.LifecycleHookTargetConfig", jsii_struct_bases=[], name_mapping={'notification_target_arn': 'notificationTargetArn'})
class LifecycleHookTargetConfig():
    def __init__(self, *, notification_target_arn: str):
        """Properties to add the target to a lifecycle hook.

        :param notification_target_arn: The ARN to use as the notification target.
        """
        self._values = {
            'notification_target_arn': notification_target_arn,
        }

    @property
    def notification_target_arn(self) -> str:
        """The ARN to use as the notification target."""
        return self._values.get('notification_target_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LifecycleHookTargetConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.LifecycleTransition")
class LifecycleTransition(enum.Enum):
    """What instance transition to attach the hook to."""
    INSTANCE_LAUNCHING = "INSTANCE_LAUNCHING"
    """Execute the hook when an instance is about to be added."""
    INSTANCE_TERMINATING = "INSTANCE_TERMINATING"
    """Execute the hook when an instance is about to be terminated."""

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.MetricAggregationType")
class MetricAggregationType(enum.Enum):
    """How the scaling metric is going to be aggregated."""
    AVERAGE = "AVERAGE"
    """Average."""
    MINIMUM = "MINIMUM"
    """Minimum."""
    MAXIMUM = "MAXIMUM"
    """Maximum."""

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.MetricTargetTrackingProps", jsii_struct_bases=[BaseTargetTrackingProps], name_mapping={'cooldown': 'cooldown', 'disable_scale_in': 'disableScaleIn', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'metric': 'metric', 'target_value': 'targetValue'})
class MetricTargetTrackingProps(BaseTargetTrackingProps):
    def __init__(self, *, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, metric: aws_cdk.aws_cloudwatch.IMetric, target_value: jsii.Number):
        """Properties for enabling tracking of an arbitrary metric.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
        :param target_value: Value to keep the metric around.
        """
        self._values = {
            'metric': metric,
            'target_value': target_value,
        }
        if cooldown is not None: self._values["cooldown"] = cooldown
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        return self._values.get('cooldown')

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: - Same as the cooldown.
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to track.

        The metric must represent a utilization, so that if it's higher than the
        target value, your ASG should scale out, and if it's lower it should
        scale in.
        """
        return self._values.get('metric')

    @property
    def target_value(self) -> jsii.Number:
        """Value to keep the metric around."""
        return self._values.get('target_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricTargetTrackingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.NetworkUtilizationScalingProps", jsii_struct_bases=[BaseTargetTrackingProps], name_mapping={'cooldown': 'cooldown', 'disable_scale_in': 'disableScaleIn', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'target_bytes_per_second': 'targetBytesPerSecond'})
class NetworkUtilizationScalingProps(BaseTargetTrackingProps):
    def __init__(self, *, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, target_bytes_per_second: jsii.Number):
        """Properties for enabling scaling based on network utilization.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_bytes_per_second: Target average bytes/seconds on each instance.
        """
        self._values = {
            'target_bytes_per_second': target_bytes_per_second,
        }
        if cooldown is not None: self._values["cooldown"] = cooldown
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        return self._values.get('cooldown')

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: - Same as the cooldown.
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def target_bytes_per_second(self) -> jsii.Number:
        """Target average bytes/seconds on each instance."""
        return self._values.get('target_bytes_per_second')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkUtilizationScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.PredefinedMetric")
class PredefinedMetric(enum.Enum):
    """One of the predefined autoscaling metrics."""
    ASG_AVERAGE_CPU_UTILIZATION = "ASG_AVERAGE_CPU_UTILIZATION"
    """Average CPU utilization of the Auto Scaling group."""
    ASG_AVERAGE_NETWORK_IN = "ASG_AVERAGE_NETWORK_IN"
    """Average number of bytes received on all network interfaces by the Auto Scaling group."""
    ASG_AVERAGE_NETWORK_OUT = "ASG_AVERAGE_NETWORK_OUT"
    """Average number of bytes sent out on all network interfaces by the Auto Scaling group."""
    ALB_REQUEST_COUNT_PER_TARGET = "ALB_REQUEST_COUNT_PER_TARGET"
    """Number of requests completed per target in an Application Load Balancer target group.

    Specify the ALB to look at in the ``resourceLabel`` field.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.RequestCountScalingProps", jsii_struct_bases=[BaseTargetTrackingProps], name_mapping={'cooldown': 'cooldown', 'disable_scale_in': 'disableScaleIn', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'target_requests_per_second': 'targetRequestsPerSecond'})
class RequestCountScalingProps(BaseTargetTrackingProps):
    def __init__(self, *, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, target_requests_per_second: jsii.Number):
        """Properties for enabling scaling based on request/second.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_requests_per_second: Target average requests/seconds on each instance.
        """
        self._values = {
            'target_requests_per_second': target_requests_per_second,
        }
        if cooldown is not None: self._values["cooldown"] = cooldown
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        return self._values.get('cooldown')

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: - Same as the cooldown.
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def target_requests_per_second(self) -> jsii.Number:
        """Target average requests/seconds on each instance."""
        return self._values.get('target_requests_per_second')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RequestCountScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.RollingUpdateConfiguration", jsii_struct_bases=[], name_mapping={'max_batch_size': 'maxBatchSize', 'min_instances_in_service': 'minInstancesInService', 'min_successful_instances_percent': 'minSuccessfulInstancesPercent', 'pause_time': 'pauseTime', 'suspend_processes': 'suspendProcesses', 'wait_on_resource_signals': 'waitOnResourceSignals'})
class RollingUpdateConfiguration():
    def __init__(self, *, max_batch_size: typing.Optional[jsii.Number]=None, min_instances_in_service: typing.Optional[jsii.Number]=None, min_successful_instances_percent: typing.Optional[jsii.Number]=None, pause_time: typing.Optional[aws_cdk.core.Duration]=None, suspend_processes: typing.Optional[typing.List["ScalingProcess"]]=None, wait_on_resource_signals: typing.Optional[bool]=None):
        """Additional settings when a rolling update is selected.

        :param max_batch_size: The maximum number of instances that AWS CloudFormation updates at once. Default: 1
        :param min_instances_in_service: The minimum number of instances that must be in service before more instances are replaced. This number affects the speed of the replacement. Default: 0
        :param min_successful_instances_percent: The percentage of instances that must signal success for an update to succeed. If an instance doesn't send a signal within the time specified in the pauseTime property, AWS CloudFormation assumes that the instance wasn't updated. This number affects the success of the replacement. If you specify this property, you must also enable the waitOnResourceSignals and pauseTime properties. Default: 100
        :param pause_time: The pause time after making a change to a batch of instances. This is intended to give those instances time to start software applications. Specify PauseTime in the ISO8601 duration format (in the format PT#H#M#S, where each # is the number of hours, minutes, and seconds, respectively). The maximum PauseTime is one hour (PT1H). Default: Duration.minutes(5) if the waitOnResourceSignals property is true, otherwise 0
        :param suspend_processes: Specifies the Auto Scaling processes to suspend during a stack update. Suspending processes prevents Auto Scaling from interfering with a stack update. Default: HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
        :param wait_on_resource_signals: Specifies whether the Auto Scaling group waits on signals from new instances during an update. AWS CloudFormation must receive a signal from each new instance within the specified PauseTime before continuing the update. To have instances wait for an Elastic Load Balancing health check before they signal success, add a health-check verification by using the cfn-init helper script. For an example, see the verify_instance_health command in the Auto Scaling rolling updates sample template. Default: true if you specified the minSuccessfulInstancesPercent property, false otherwise
        """
        self._values = {
        }
        if max_batch_size is not None: self._values["max_batch_size"] = max_batch_size
        if min_instances_in_service is not None: self._values["min_instances_in_service"] = min_instances_in_service
        if min_successful_instances_percent is not None: self._values["min_successful_instances_percent"] = min_successful_instances_percent
        if pause_time is not None: self._values["pause_time"] = pause_time
        if suspend_processes is not None: self._values["suspend_processes"] = suspend_processes
        if wait_on_resource_signals is not None: self._values["wait_on_resource_signals"] = wait_on_resource_signals

    @property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        """The maximum number of instances that AWS CloudFormation updates at once.

        default
        :default: 1
        """
        return self._values.get('max_batch_size')

    @property
    def min_instances_in_service(self) -> typing.Optional[jsii.Number]:
        """The minimum number of instances that must be in service before more instances are replaced.

        This number affects the speed of the replacement.

        default
        :default: 0
        """
        return self._values.get('min_instances_in_service')

    @property
    def min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """The percentage of instances that must signal success for an update to succeed.

        If an instance doesn't send a signal within the time specified in the
        pauseTime property, AWS CloudFormation assumes that the instance wasn't
        updated.

        This number affects the success of the replacement.

        If you specify this property, you must also enable the
        waitOnResourceSignals and pauseTime properties.

        default
        :default: 100
        """
        return self._values.get('min_successful_instances_percent')

    @property
    def pause_time(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The pause time after making a change to a batch of instances.

        This is intended to give those instances time to start software applications.

        Specify PauseTime in the ISO8601 duration format (in the format
        PT#H#M#S, where each # is the number of hours, minutes, and seconds,
        respectively). The maximum PauseTime is one hour (PT1H).

        default
        :default: Duration.minutes(5) if the waitOnResourceSignals property is true, otherwise 0
        """
        return self._values.get('pause_time')

    @property
    def suspend_processes(self) -> typing.Optional[typing.List["ScalingProcess"]]:
        """Specifies the Auto Scaling processes to suspend during a stack update.

        Suspending processes prevents Auto Scaling from interfering with a stack
        update.

        default
        :default: HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
        """
        return self._values.get('suspend_processes')

    @property
    def wait_on_resource_signals(self) -> typing.Optional[bool]:
        """Specifies whether the Auto Scaling group waits on signals from new instances during an update.

        AWS CloudFormation must receive a signal from each new instance within
        the specified PauseTime before continuing the update.

        To have instances wait for an Elastic Load Balancing health check before
        they signal success, add a health-check verification by using the
        cfn-init helper script. For an example, see the verify_instance_health
        command in the Auto Scaling rolling updates sample template.

        default
        :default: true if you specified the minSuccessfulInstancesPercent property, false otherwise
        """
        return self._values.get('wait_on_resource_signals')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RollingUpdateConfiguration(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.ScalingInterval", jsii_struct_bases=[], name_mapping={'change': 'change', 'lower': 'lower', 'upper': 'upper'})
class ScalingInterval():
    def __init__(self, *, change: jsii.Number, lower: typing.Optional[jsii.Number]=None, upper: typing.Optional[jsii.Number]=None):
        """A range of metric values in which to apply a certain scaling operation.

        :param change: The capacity adjustment to apply in this interval. The number is interpreted differently based on AdjustmentType: - ChangeInCapacity: add the adjustment to the current capacity. The number can be positive or negative. - PercentChangeInCapacity: add or remove the given percentage of the current capacity to itself. The number can be in the range [-100..100]. - ExactCapacity: set the capacity to this number. The number must be positive.
        :param lower: The lower bound of the interval. The scaling adjustment will be applied if the metric is higher than this value. Default: Threshold automatically derived from neighbouring intervals
        :param upper: The upper bound of the interval. The scaling adjustment will be applied if the metric is lower than this value. Default: Threshold automatically derived from neighbouring intervals
        """
        self._values = {
            'change': change,
        }
        if lower is not None: self._values["lower"] = lower
        if upper is not None: self._values["upper"] = upper

    @property
    def change(self) -> jsii.Number:
        """The capacity adjustment to apply in this interval.

        The number is interpreted differently based on AdjustmentType:

        - ChangeInCapacity: add the adjustment to the current capacity.
          The number can be positive or negative.
        - PercentChangeInCapacity: add or remove the given percentage of the current
          capacity to itself. The number can be in the range [-100..100].
        - ExactCapacity: set the capacity to this number. The number must
          be positive.
        """
        return self._values.get('change')

    @property
    def lower(self) -> typing.Optional[jsii.Number]:
        """The lower bound of the interval.

        The scaling adjustment will be applied if the metric is higher than this value.

        default
        :default: Threshold automatically derived from neighbouring intervals
        """
        return self._values.get('lower')

    @property
    def upper(self) -> typing.Optional[jsii.Number]:
        """The upper bound of the interval.

        The scaling adjustment will be applied if the metric is lower than this value.

        default
        :default: Threshold automatically derived from neighbouring intervals
        """
        return self._values.get('upper')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScalingInterval(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.ScalingProcess")
class ScalingProcess(enum.Enum):
    LAUNCH = "LAUNCH"
    TERMINATE = "TERMINATE"
    HEALTH_CHECK = "HEALTH_CHECK"
    REPLACE_UNHEALTHY = "REPLACE_UNHEALTHY"
    AZ_REBALANCE = "AZ_REBALANCE"
    ALARM_NOTIFICATION = "ALARM_NOTIFICATION"
    SCHEDULED_ACTIONS = "SCHEDULED_ACTIONS"
    ADD_TO_LOAD_BALANCER = "ADD_TO_LOAD_BALANCER"

class Schedule(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-autoscaling.Schedule"):
    """Schedule for scheduled scaling actions."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ScheduleProxy

    def __init__(self) -> None:
        jsii.create(Schedule, self, [])

    @jsii.member(jsii_name="cron")
    @classmethod
    def cron(cls, *, day: typing.Optional[str]=None, hour: typing.Optional[str]=None, minute: typing.Optional[str]=None, month: typing.Optional[str]=None, week_day: typing.Optional[str]=None) -> "Schedule":
        """Create a schedule from a set of cron fields.

        :param options: -
        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        """
        options = CronOptions(day=day, hour=hour, minute=minute, month=month, week_day=week_day)

        return jsii.sinvoke(cls, "cron", [options])

    @jsii.member(jsii_name="expression")
    @classmethod
    def expression(cls, expression: str) -> "Schedule":
        """Construct a schedule from a literal schedule expression.

        :param expression: The expression to use. Must be in a format that AutoScaling will recognize

        see
        :see: http://crontab.org/
        """
        return jsii.sinvoke(cls, "expression", [expression])

    @property
    @jsii.member(jsii_name="expressionString")
    @abc.abstractmethod
    def expression_string(self) -> str:
        """Retrieve the expression for this schedule."""
        ...


class _ScheduleProxy(Schedule):
    @property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> str:
        """Retrieve the expression for this schedule."""
        return jsii.get(self, "expressionString")


class ScheduledAction(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.ScheduledAction"):
    """Define a scheduled scaling action."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", schedule: "Schedule", desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param auto_scaling_group: The AutoScalingGroup to apply the scheduled actions to.
        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props = ScheduledActionProps(auto_scaling_group=auto_scaling_group, schedule=schedule, desired_capacity=desired_capacity, end_time=end_time, max_capacity=max_capacity, min_capacity=min_capacity, start_time=start_time)

        jsii.create(ScheduledAction, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.ScheduledActionProps", jsii_struct_bases=[BasicScheduledActionProps], name_mapping={'schedule': 'schedule', 'desired_capacity': 'desiredCapacity', 'end_time': 'endTime', 'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'start_time': 'startTime', 'auto_scaling_group': 'autoScalingGroup'})
class ScheduledActionProps(BasicScheduledActionProps):
    def __init__(self, *, schedule: "Schedule", desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None, auto_scaling_group: "IAutoScalingGroup"):
        """Properties for a scheduled action on an AutoScalingGroup.

        :param schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
        :param desired_capacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
        :param end_time: When this scheduled action expires. Default: - The rule never expires.
        :param max_capacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
        :param min_capacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
        :param start_time: When this scheduled action becomes active. Default: - The rule is activate immediately.
        :param auto_scaling_group: The AutoScalingGroup to apply the scheduled actions to.
        """
        self._values = {
            'schedule': schedule,
            'auto_scaling_group': auto_scaling_group,
        }
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if end_time is not None: self._values["end_time"] = end_time
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if min_capacity is not None: self._values["min_capacity"] = min_capacity
        if start_time is not None: self._values["start_time"] = start_time

    @property
    def schedule(self) -> "Schedule":
        """When to perform this action.

        Supports cron expressions.

        For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            08 * * ?
        """
        return self._values.get('schedule')

    @property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """The new desired capacity.

        At the scheduled time, set the desired capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        default
        :default: - No new desired capacity.
        """
        return self._values.get('desired_capacity')

    @property
    def end_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action expires.

        default
        :default: - The rule never expires.
        """
        return self._values.get('end_time')

    @property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """The new maximum capacity.

        At the scheduled time, set the maximum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        default
        :default: - No new maximum capacity.
        """
        return self._values.get('max_capacity')

    @property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """The new minimum capacity.

        At the scheduled time, set the minimum capacity to the given capacity.

        At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

        default
        :default: - No new minimum capacity.
        """
        return self._values.get('min_capacity')

    @property
    def start_time(self) -> typing.Optional[datetime.datetime]:
        """When this scheduled action becomes active.

        default
        :default: - The rule is activate immediately.
        """
        return self._values.get('start_time')

    @property
    def auto_scaling_group(self) -> "IAutoScalingGroup":
        """The AutoScalingGroup to apply the scheduled actions to."""
        return self._values.get('auto_scaling_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class StepScalingAction(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.StepScalingAction"):
    """Define a step scaling action.

    This kind of scaling policy adjusts the target capacity in configurable
    steps. The size of the step is configurable based on the metric's distance
    to its alarm threshold.

    This Action must be used as the target of a CloudWatch alarm to take effect.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param auto_scaling_group: The auto scaling group.
        :param adjustment_type: How the adjustment numbers are interpreted. Default: ChangeInCapacity
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: The default cooldown configured on the AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. Default: Average
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = StepScalingActionProps(auto_scaling_group=auto_scaling_group, adjustment_type=adjustment_type, cooldown=cooldown, estimated_instance_warmup=estimated_instance_warmup, metric_aggregation_type=metric_aggregation_type, min_adjustment_magnitude=min_adjustment_magnitude)

        jsii.create(StepScalingAction, self, [scope, id, props])

    @jsii.member(jsii_name="addAdjustment")
    def add_adjustment(self, *, adjustment: jsii.Number, lower_bound: typing.Optional[jsii.Number]=None, upper_bound: typing.Optional[jsii.Number]=None) -> None:
        """Add an adjusment interval to the ScalingAction.

        :param adjustment: -
        :param adjustment: What number to adjust the capacity with. The number is interpeted as an added capacity, a new fixed capacity or an added percentage depending on the AdjustmentType value of the StepScalingPolicy. Can be positive or negative.
        :param lower_bound: Lower bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is higher than this value. Default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
        :param upper_bound: Upper bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is lower than this value. Default: +Infinity
        """
        adjustment = AdjustmentTier(adjustment=adjustment, lower_bound=lower_bound, upper_bound=upper_bound)

        return jsii.invoke(self, "addAdjustment", [adjustment])

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.StepScalingActionProps", jsii_struct_bases=[], name_mapping={'auto_scaling_group': 'autoScalingGroup', 'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'metric_aggregation_type': 'metricAggregationType', 'min_adjustment_magnitude': 'minAdjustmentMagnitude'})
class StepScalingActionProps():
    def __init__(self, *, auto_scaling_group: "IAutoScalingGroup", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None):
        """Properties for a scaling policy.

        :param auto_scaling_group: The auto scaling group.
        :param adjustment_type: How the adjustment numbers are interpreted. Default: ChangeInCapacity
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: The default cooldown configured on the AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param metric_aggregation_type: The aggregation type for the CloudWatch metrics. Default: Average
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        self._values = {
            'auto_scaling_group': auto_scaling_group,
        }
        if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
        if cooldown is not None: self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if metric_aggregation_type is not None: self._values["metric_aggregation_type"] = metric_aggregation_type
        if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @property
    def auto_scaling_group(self) -> "IAutoScalingGroup":
        """The auto scaling group."""
        return self._values.get('auto_scaling_group')

    @property
    def adjustment_type(self) -> typing.Optional["AdjustmentType"]:
        """How the adjustment numbers are interpreted.

        default
        :default: ChangeInCapacity
        """
        return self._values.get('adjustment_type')

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: The default cooldown configured on the AutoScalingGroup
        """
        return self._values.get('cooldown')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: Same as the cooldown
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def metric_aggregation_type(self) -> typing.Optional["MetricAggregationType"]:
        """The aggregation type for the CloudWatch metrics.

        default
        :default: Average
        """
        return self._values.get('metric_aggregation_type')

    @property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        default
        :default: No minimum scaling effect
        """
        return self._values.get('min_adjustment_magnitude')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StepScalingActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class StepScalingPolicy(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicy"):
    """Define a acaling strategy which scales depending on absolute values of some metric.

    You can specify the scaling behavior for various values of the metric.

    Implemented using one or more CloudWatch alarms and Step Scaling Policies.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param auto_scaling_group: The auto scaling group.
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = StepScalingPolicyProps(auto_scaling_group=auto_scaling_group, metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, estimated_instance_warmup=estimated_instance_warmup, min_adjustment_magnitude=min_adjustment_magnitude)

        jsii.create(StepScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="lowerAction")
    def lower_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "lowerAction")

    @property
    @jsii.member(jsii_name="lowerAlarm")
    def lower_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "lowerAlarm")

    @property
    @jsii.member(jsii_name="upperAction")
    def upper_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "upperAction")

    @property
    @jsii.member(jsii_name="upperAlarm")
    def upper_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "upperAlarm")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicyProps", jsii_struct_bases=[BasicStepScalingPolicyProps], name_mapping={'metric': 'metric', 'scaling_steps': 'scalingSteps', 'adjustment_type': 'adjustmentType', 'cooldown': 'cooldown', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'min_adjustment_magnitude': 'minAdjustmentMagnitude', 'auto_scaling_group': 'autoScalingGroup'})
class StepScalingPolicyProps(BasicStepScalingPolicyProps):
    def __init__(self, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, auto_scaling_group: "IAutoScalingGroup"):
        """
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        :param auto_scaling_group: The auto scaling group.
        """
        self._values = {
            'metric': metric,
            'scaling_steps': scaling_steps,
            'auto_scaling_group': auto_scaling_group,
        }
        if adjustment_type is not None: self._values["adjustment_type"] = adjustment_type
        if cooldown is not None: self._values["cooldown"] = cooldown
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if min_adjustment_magnitude is not None: self._values["min_adjustment_magnitude"] = min_adjustment_magnitude

    @property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """Metric to scale on."""
        return self._values.get('metric')

    @property
    def scaling_steps(self) -> typing.List["ScalingInterval"]:
        """The intervals for scaling.

        Maps a range of metric values to a particular scaling behavior.
        """
        return self._values.get('scaling_steps')

    @property
    def adjustment_type(self) -> typing.Optional["AdjustmentType"]:
        """How the adjustment numbers inside 'intervals' are interpreted.

        default
        :default: ChangeInCapacity
        """
        return self._values.get('adjustment_type')

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Grace period after scaling activity.

        default
        :default: Default cooldown period on your AutoScalingGroup
        """
        return self._values.get('cooldown')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: Same as the cooldown
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def min_adjustment_magnitude(self) -> typing.Optional[jsii.Number]:
        """Minimum absolute number to adjust capacity with as result of percentage scaling.

        Only when using AdjustmentType = PercentChangeInCapacity, this number controls
        the minimum absolute effect size.

        default
        :default: No minimum scaling effect
        """
        return self._values.get('min_adjustment_magnitude')

    @property
    def auto_scaling_group(self) -> "IAutoScalingGroup":
        """The auto scaling group."""
        return self._values.get('auto_scaling_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StepScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class TargetTrackingScalingPolicy(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicy"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param auto_scaling_group: 
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metric.
        :param resource_label: The resource label associated with the predefined metric. Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the format should be: app///targetgroup// Default: - No resource label.
        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props = TargetTrackingScalingPolicyProps(auto_scaling_group=auto_scaling_group, target_value=target_value, custom_metric=custom_metric, predefined_metric=predefined_metric, resource_label=resource_label, cooldown=cooldown, disable_scale_in=disable_scale_in, estimated_instance_warmup=estimated_instance_warmup)

        jsii.create(TargetTrackingScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicyProps", jsii_struct_bases=[BasicTargetTrackingScalingPolicyProps], name_mapping={'cooldown': 'cooldown', 'disable_scale_in': 'disableScaleIn', 'estimated_instance_warmup': 'estimatedInstanceWarmup', 'target_value': 'targetValue', 'custom_metric': 'customMetric', 'predefined_metric': 'predefinedMetric', 'resource_label': 'resourceLabel', 'auto_scaling_group': 'autoScalingGroup'})
class TargetTrackingScalingPolicyProps(BasicTargetTrackingScalingPolicyProps):
    def __init__(self, *, cooldown: typing.Optional[aws_cdk.core.Duration]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup: typing.Optional[aws_cdk.core.Duration]=None, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.IMetric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, auto_scaling_group: "IAutoScalingGroup"):
        """Properties for a concrete TargetTrackingPolicy.

        Adds the scalingTarget.

        :param cooldown: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
        :param estimated_instance_warmup: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        :param target_value: The target value for the metric.
        :param custom_metric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
        :param predefined_metric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metric.
        :param resource_label: The resource label associated with the predefined metric. Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the format should be: app///targetgroup// Default: - No resource label.
        :param auto_scaling_group: 
        """
        self._values = {
            'target_value': target_value,
            'auto_scaling_group': auto_scaling_group,
        }
        if cooldown is not None: self._values["cooldown"] = cooldown
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if estimated_instance_warmup is not None: self._values["estimated_instance_warmup"] = estimated_instance_warmup
        if custom_metric is not None: self._values["custom_metric"] = custom_metric
        if predefined_metric is not None: self._values["predefined_metric"] = predefined_metric
        if resource_label is not None: self._values["resource_label"] = resource_label

    @property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scaling completes before another scaling activity can start.

        default
        :default: - The default cooldown configured on the AutoScalingGroup.
        """
        return self._values.get('cooldown')

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the autoscaling group. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        group.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def estimated_instance_warmup(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Estimated time until a newly launched instance can send metrics to CloudWatch.

        default
        :default: - Same as the cooldown.
        """
        return self._values.get('estimated_instance_warmup')

    @property
    def target_value(self) -> jsii.Number:
        """The target value for the metric."""
        return self._values.get('target_value')

    @property
    def custom_metric(self) -> typing.Optional[aws_cdk.aws_cloudwatch.IMetric]:
        """A custom metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No custom metric.
        """
        return self._values.get('custom_metric')

    @property
    def predefined_metric(self) -> typing.Optional["PredefinedMetric"]:
        """A predefined metric for application autoscaling.

        The metric must track utilization. Scaling out will happen if the metric is higher than
        the target value, scaling in will happen in the metric is lower than the target value.

        Exactly one of customMetric or predefinedMetric must be specified.

        default
        :default: - No predefined metric.
        """
        return self._values.get('predefined_metric')

    @property
    def resource_label(self) -> typing.Optional[str]:
        """The resource label associated with the predefined metric.

        Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the
        format should be:

        app///targetgroup//

        default
        :default: - No resource label.
        """
        return self._values.get('resource_label')

    @property
    def auto_scaling_group(self) -> "IAutoScalingGroup":
        return self._values.get('auto_scaling_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TargetTrackingScalingPolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.UpdateType")
class UpdateType(enum.Enum):
    """The type of update to perform on instances in this AutoScalingGroup."""
    NONE = "NONE"
    """Don't do anything."""
    REPLACING_UPDATE = "REPLACING_UPDATE"
    """Replace the entire AutoScalingGroup.

    Builds a new AutoScalingGroup first, then delete the old one.
    """
    ROLLING_UPDATE = "ROLLING_UPDATE"
    """Replace the instances in the AutoScalingGroup."""

__all__ = ["AdjustmentTier", "AdjustmentType", "AutoScalingGroup", "AutoScalingGroupProps", "BaseTargetTrackingProps", "BasicLifecycleHookProps", "BasicScheduledActionProps", "BasicStepScalingPolicyProps", "BasicTargetTrackingScalingPolicyProps", "BlockDevice", "BlockDeviceVolume", "CfnAutoScalingGroup", "CfnAutoScalingGroupProps", "CfnLaunchConfiguration", "CfnLaunchConfigurationProps", "CfnLifecycleHook", "CfnLifecycleHookProps", "CfnScalingPolicy", "CfnScalingPolicyProps", "CfnScheduledAction", "CfnScheduledActionProps", "CommonAutoScalingGroupProps", "CpuUtilizationScalingProps", "CronOptions", "DefaultResult", "EbsDeviceOptions", "EbsDeviceOptionsBase", "EbsDeviceProps", "EbsDeviceSnapshotOptions", "EbsDeviceVolumeType", "Ec2HealthCheckOptions", "ElbHealthCheckOptions", "HealthCheck", "IAutoScalingGroup", "ILifecycleHook", "ILifecycleHookTarget", "LifecycleHook", "LifecycleHookProps", "LifecycleHookTargetConfig", "LifecycleTransition", "MetricAggregationType", "MetricTargetTrackingProps", "NetworkUtilizationScalingProps", "PredefinedMetric", "RequestCountScalingProps", "RollingUpdateConfiguration", "ScalingInterval", "ScalingProcess", "Schedule", "ScheduledAction", "ScheduledActionProps", "StepScalingAction", "StepScalingActionProps", "StepScalingPolicy", "StepScalingPolicyProps", "TargetTrackingScalingPolicy", "TargetTrackingScalingPolicyProps", "UpdateType", "__jsii_assembly__"]

publication.publish()
