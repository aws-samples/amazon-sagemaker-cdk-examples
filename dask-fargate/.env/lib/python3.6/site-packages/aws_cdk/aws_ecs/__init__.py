"""
## Amazon ECS Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This package contains constructs for working with **Amazon Elastic Container
Service** (Amazon ECS).

Amazon ECS is a highly scalable, fast, container management service
that makes it easy to run, stop,
and manage Docker containers on a cluster of Amazon EC2 instances.

For further information on Amazon ECS,
see the [Amazon ECS documentation](https://docs.aws.amazon.com/ecs)

The following example creates an Amazon ECS cluster,
adds capacity to it,
and instantiates the Amazon ECS Service with an automatic load balancer.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ecs as ecs

# Create an ECS cluster
cluster = ecs.Cluster(self, "Cluster",
    vpc=vpc
)

# Add capacity to it
cluster.add_capacity("DefaultAutoScalingGroupCapacity",
    instance_type=ec2.InstanceType("t2.xlarge"),
    desired_capacity=3
)

task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")

task_definition.add_container("DefaultContainer",
    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
    memory_limit_mi_b=512
)

# Instantiate an Amazon ECS Service
ecs_service = ecs.Ec2Service(self, "Service",
    cluster=cluster,
    task_definition=task_definition
)
```

For a set of constructs defining common ECS architectural patterns, see the `@aws-cdk/aws-ecs-patterns` package.

## AWS Fargate vs Amazon ECS

There are two sets of constructs in this library; one to run tasks on Amazon ECS and
one to run tasks on AWS Fargate.

* Use the `Ec2TaskDefinition` and `Ec2Service` constructs to run tasks on Amazon EC2 instances running in your account.
* Use the `FargateTaskDefinition` and `FargateService` constructs to run tasks on
  instances that are managed for you by AWS.

Here are the main differences:

* **Amazon EC2**: instances are under your control. Complete control of task to host
  allocation. Required to specify at least a memory reseration or limit for
  every container. Can use Host, Bridge and AwsVpc networking modes. Can attach
  Classic Load Balancer. Can share volumes between container and host.
* **AWS Fargate**: tasks run on AWS-managed instances, AWS manages task to host
  allocation for you. Requires specification of memory and cpu sizes at the
  taskdefinition level. Only supports AwsVpc networking modes and
  Application/Network Load Balancers. Only the AWS log driver is supported.
  Many host features are not supported such as adding kernel capabilities
  and mounting host devices/volumes inside the container.

For more information on Amazon EC2 vs AWS Fargate and networking see the AWS Documentation:
[AWS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html) and
[Task Networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html).

## Clusters

A `Cluster` defines the infrastructure to run your
tasks on. You can run many tasks on a single cluster.

The following code creates a cluster that can run AWS Fargate tasks:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster = ecs.Cluster(self, "Cluster",
    vpc=vpc
)
```

To use tasks with Amazon EC2 launch-type, you have to add capacity to
the cluster in order for tasks to be scheduled on your instances.  Typically,
you add an AutoScalingGroup with instances running the latest
Amazon ECS-optimized AMI to the cluster. There is a method to build and add such an
AutoScalingGroup automatically, or you can supply a customized AutoScalingGroup
that you construct yourself. It's possible to add multiple AutoScalingGroups
with various instance types.

The following example creates an Amazon ECS cluster and adds capacity to it:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster = ecs.Cluster(self, "Cluster",
    vpc=vpc
)

# Either add default capacity
cluster.add_capacity("DefaultAutoScalingGroupCapacity",
    instance_type=ec2.InstanceType("t2.xlarge"),
    desired_capacity=3
)

# Or add customized capacity. Be sure to start the Amazon ECS-optimized AMI.
auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
    vpc=vpc,
    instance_type=ec2.InstanceType("t2.xlarge"),
    machine_image=EcsOptimizedImage.amazon_linux(),
    # Or use Amazon ECS-Optimized Amazon Linux 2 AMI
    # machineImage: EcsOptimizedImage.amazonLinux2(),
    desired_capacity=3
)

cluster.add_auto_scaling_group(auto_scaling_group)
```

If you omit the property `vpc`, the construct will create a new VPC with two AZs.

### Spot Instances

To add spot instances into the cluster, you must specify the `spotPrice` in the `ecs.AddCapacityOptions` and optionally enable the `spotInstanceDraining` property.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Add an AutoScalingGroup with spot instances to the existing cluster
cluster.add_capacity("AsgSpot",
    max_capacity=2,
    min_capacity=2,
    desired_capacity=2,
    instance_type=ec2.InstanceType("c5.xlarge"),
    spot_price="0.0735",
    # Enable the Automated Spot Draining support for Amazon ECS
    spot_instance_draining=True
)
```

## Task definitions

A task Definition describes what a single copy of a **task** should look like.
A task definition has one or more containers; typically, it has one
main container (the *default container* is the first one that's added
to the task definition, and it is marked *essential*) and optionally
some supporting containers which are used to support the main container,
doings things like upload logs or metrics to monitoring services.

To run a task or service with Amazon EC2 launch type, use the `Ec2TaskDefinition`. For AWS Fargate tasks/services, use the
`FargateTaskDefinition`. These classes provide a simplified API that only contain
properties relevant for that specific launch type.

For a `FargateTaskDefinition`, specify the task size (`memoryLimitMiB` and `cpu`):

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
    memory_limit_mi_b=512,
    cpu=256
)
```

To add containers to a task definition, call `addContainer()`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
container = fargate_task_definition.add_container("WebContainer",
    # Use an image from DockerHub
    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
)
```

For a `Ec2TaskDefinition`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
ec2_task_definition = ecs.Ec2TaskDefinition(self, "TaskDef",
    network_mode=NetworkMode.BRIDGE
)

container = ec2_task_definition.add_container("WebContainer",
    # Use an image from DockerHub
    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
    memory_limit_mi_b=1024
)
```

You can specify container properties when you add them to the task definition, or with various methods, e.g.:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
container.add_port_mappings(
    container_port=3000
)
```

To use a TaskDefinition that can be used with either Amazon EC2 or
AWS Fargate launch types, use the `TaskDefinition` construct.

When creating a task definition you have to specify what kind of
tasks you intend to run: Amazon EC2, AWS Fargate, or both.
The following example uses both:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
task_definition = ecs.TaskDefinition(self, "TaskDef",
    memory_mi_b="512",
    cpu="256",
    network_mode=NetworkMode.AWS_VPC,
    compatibility=ecs.Compatibility.EC2_AND_FARGATE
)
```

### Images

Images supply the software that runs inside the container. Images can be
obtained from either DockerHub or from ECR repositories, or built directly from a local Dockerfile.

* `ecs.ContainerImage.fromRegistry(imageName)`: use a public image.
* `ecs.ContainerImage.fromRegistry(imageName, { credentials: mySecret })`: use a private image that requires credentials.
* `ecs.ContainerImage.fromEcrRepository(repo, tag)`: use the given ECR repository as the image
  to start. If no tag is provided, "latest" is assumed.
* `ecs.ContainerImage.fromAsset('./image')`: build and upload an
  image directly from a `Dockerfile` in your source directory.

### Environment variables

To pass environment variables to the container, use the `environment` and `secrets` props.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
task_definition.add_container("container",
    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
    memory_limit_mi_b=1024,
    environment={# clear text, not for sensitive data
        "STAGE": "prod"},
    secrets={# Retrieved from AWS Secrets Manager or AWS Systems Manager Parameter Store at container start-up.
        "SECRET": ecs.Secret.from_secrets_manager(secret),
        "PARAMETER": ecs.Secret.from_ssm_parameter(parameter)}
)
```

The task execution role is automatically granted read permissions on the secrets/parameters.

## Service

A `Service` instantiates a `TaskDefinition` on a `Cluster` a given number of
times, optionally associating them with a load balancer.
If a task fails,
Amazon ECS automatically restarts the task.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
task_definition =

service = ecs.FargateService(self, "Service",
    cluster=cluster,
    task_definition=task_definition,
    desired_count=5
)
```

### Include an application/network load balancer

`Services` are load balancing targets and can be added to a target group, which will be attached to an application/network load balancers:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

service = ecs.FargateService(self, "Service")

lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
listener = lb.add_listener("Listener", port=80)
target_group1 = listener.add_targets("ECS1",
    port=80,
    targets=[service]
)
target_group2 = listener.add_targets("ECS2",
    port=80,
    targets=[service.load_balancer_target(
        container_name="MyContainer",
        container_port=8080
    )]
)
```

Note that in the example above, the default `service` only allows you to register the first essential container or the first mapped port on the container as a target and add it to a new target group. To have more control over which container and port to register as targets, you can use `service.loadBalancerTarget()` to return a load balancing target for a specific container and port.

Alternatively, you can also create all load balancer targets to be registered in this service, add them to target groups, and attach target groups to listeners accordingly.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

service = ecs.FargateService(self, "Service")

lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
listener = lb.add_listener("Listener", port=80)
service.register_load_balancer_targets(
    container_target={
        "container_name": "web",
        "container_port": 80
    },
    target_group_id="ECS",
    listener=ecs.ListenerConfig.application_listener(listener,
        protocol=elbv2.ApplicationProtocol.HTTPS
    )
)
```

### Using a Load Balancer from a different Stack

If you want to put your Load Balancer and the Service it is load balancing to in
different stacks, you may not be able to use the convenience methods
`loadBalancer.addListener()` and `listener.addTargets()`.

The reason is that these methods will create resources in the same Stack as the
object they're called on, which may lead to cyclic references between stacks.
Instead, you will have to create an `ApplicationListener` in the service stack,
or an empty `TargetGroup` in the load balancer stack that you attach your
service to.

See the [ecs/cross-stack-load-balancer example](https://github.com/aws-samples/aws-cdk-examples/tree/master/typescript/ecs/cross-stack-load-balancer/)
for the alternatives.

### Include a classic load balancer

`Services` can also be directly attached to a classic load balancer as targets:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancing as elb

service = ecs.Ec2Service(self, "Service")

lb = elb.LoadBalancer(stack, "LB", vpc=vpc)
lb.add_listener(external_port=80)
lb.add_target(service)
```

Similarly, if you want to have more control over load balancer targeting:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancing as elb

service = ecs.Ec2Service(self, "Service")

lb = elb.LoadBalancer(stack, "LB", vpc=vpc)
lb.add_listener(external_port=80)
lb.add_target(service.load_balancer_target,
    container_name="MyContainer",
    container_port=80
)
```

There are two higher-level constructs available which include a load balancer for you that can be found in the aws-ecs-patterns module:

* `LoadBalancedFargateService`
* `LoadBalancedEc2Service`

## Task Auto-Scaling

You can configure the task count of a service to match demand. Task auto-scaling is
configured by calling `autoScaleTaskCount()`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
scaling = service.auto_scale_task_count(max_capacity=10)
scaling.scale_on_cpu_utilization("CpuScaling",
    target_utilization_percent=50
)

scaling.scale_on_request_count("RequestScaling",
    requests_per_target=10000,
    target_group=target
)
```

Task auto-scaling is powered by *Application Auto-Scaling*.
See that section for details.

## Instance Auto-Scaling

If you're running on AWS Fargate, AWS manages the physical machines that your
containers are running on for you. If you're running an Amazon ECS cluster however,
your Amazon EC2 instances might fill up as your number of Tasks goes up.

To avoid placement errors, configure auto-scaling for your
Amazon EC2 instance group so that your instance count scales with demand. To keep
your Amazon EC2 instances halfway loaded, scaling up to a maximum of 30 instances
if required:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
auto_scaling_group = cluster.add_capacity("DefaultAutoScalingGroup",
    instance_type=ec2.InstanceType("t2.xlarge"),
    min_capacity=3,
    max_capacity=30,
    desired_capacity=3,

    # Give instances 5 minutes to drain running tasks when an instance is
    # terminated. This is the default, turn this off by specifying 0 or
    # change the timeout up to 900 seconds.
    task_drain_time=Duration.seconds(300)
)

auto_scaling_group.scale_on_cpu_utilization("KeepCpuHalfwayLoaded",
    target_utilization_percent=50
)
```

See the `@aws-cdk/aws-autoscaling` library for more autoscaling options
you can configure on your instances.

## Integration with CloudWatch Events

To start an Amazon ECS task on an Amazon EC2-backed Cluster, instantiate an
`@aws-cdk/aws-events-targets.EcsTask` instead of an `Ec2Service`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_events_targets as targets

# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_asset(path.resolve(__dirname, "..", "eventhandler-image")),
    memory_limit_mi_b=256,
    logging=ecs.AwsLogDriver(stream_prefix="EventDemo")
)

# An Rule that describes the event trigger (in this case a scheduled run)
rule = events.Rule(self, "Rule",
    schedule=events.Schedule.expression("rate(1 min)")
)

# Pass an environment variable to the container 'TheContainer' in the task
rule.add_target(targets.EcsTask(
    cluster=cluster,
    task_definition=task_definition,
    task_count=1,
    container_overrides=[ContainerOverride(
        container_name="TheContainer",
        environment=[TaskEnvironmentVariable(
            name="I_WAS_TRIGGERED",
            value="From CloudWatch Events"
        )]
    )]
))
```

## Log Drivers

Currently Supported Log Drivers:

* awslogs
* fluentd
* gelf
* journald
* json-file
* splunk
* syslog

### awslogs Log Driver

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.LogDrivers.awslogs(stream_prefix="EventDemo")
)
```

### fluentd Log Driver

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.LogDrivers.fluentd()
)
```

### gelf Log Driver

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.LogDrivers.gelf()
)
```

### journald Log Driver

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.LogDrivers.journald()
)
```

### json-file Log Driver

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.LogDrivers.json_file()
)
```

### splunk Log Driver

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.LogDrivers.splunk()
)
```

### syslog Log Driver

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.LogDrivers.syslog()
)
```

### Generic Log Driver

A generic log driver object exists to provide a lower level abstraction of the log driver configuration.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Create a Task Definition for the container to start
task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("example-image"),
    memory_limit_mi_b=256,
    logging=ecs.GenericLogDriver(
        log_driver="fluentd",
        options={
            "tag": "example-tag"
        }
    )
)
```
"""
import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_autoscaling
import aws_cdk.aws_autoscaling_hooktargets
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudformation
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecr_assets
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_route53
import aws_cdk.aws_route53_targets
import aws_cdk.aws_secretsmanager
import aws_cdk.aws_servicediscovery
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.aws_ssm
import aws_cdk.core
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecs", "1.18.0", __name__, "aws-ecs@1.18.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AddAutoScalingGroupCapacityOptions", jsii_struct_bases=[], name_mapping={'can_containers_access_instance_role': 'canContainersAccessInstanceRole', 'spot_instance_draining': 'spotInstanceDraining', 'task_drain_time': 'taskDrainTime'})
class AddAutoScalingGroupCapacityOptions():
    def __init__(self, *, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[aws_cdk.core.Duration]=None):
        """The properties for adding an AutoScalingGroup.

        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)
        """
        self._values = {
        }
        if can_containers_access_instance_role is not None: self._values["can_containers_access_instance_role"] = can_containers_access_instance_role
        if spot_instance_draining is not None: self._values["spot_instance_draining"] = spot_instance_draining
        if task_drain_time is not None: self._values["task_drain_time"] = task_drain_time

    @property
    def can_containers_access_instance_role(self) -> typing.Optional[bool]:
        """Specifies whether the containers can access the container instance role.

        default
        :default: false
        """
        return self._values.get('can_containers_access_instance_role')

    @property
    def spot_instance_draining(self) -> typing.Optional[bool]:
        """Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_.

        default
        :default: false
        """
        return self._values.get('spot_instance_draining')

    @property
    def task_drain_time(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period to wait before force terminating an instance that is draining.

        This creates a Lambda function that is used by a lifecycle hook for the
        AutoScalingGroup that will delay instance termination until all ECS tasks
        have drained from the instance. Set to 0 to disable task draining.

        Set to 0 to disable task draining.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('task_drain_time')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddAutoScalingGroupCapacityOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AddCapacityOptions", jsii_struct_bases=[AddAutoScalingGroupCapacityOptions, aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps], name_mapping={'can_containers_access_instance_role': 'canContainersAccessInstanceRole', 'spot_instance_draining': 'spotInstanceDraining', 'task_drain_time': 'taskDrainTime', 'allow_all_outbound': 'allowAllOutbound', 'associate_public_ip_address': 'associatePublicIpAddress', 'cooldown': 'cooldown', 'desired_capacity': 'desiredCapacity', 'health_check': 'healthCheck', 'ignore_unmodified_size_properties': 'ignoreUnmodifiedSizeProperties', 'key_name': 'keyName', 'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'notifications_topic': 'notificationsTopic', 'replacing_update_min_successful_instances_percent': 'replacingUpdateMinSuccessfulInstancesPercent', 'resource_signal_count': 'resourceSignalCount', 'resource_signal_timeout': 'resourceSignalTimeout', 'rolling_update_configuration': 'rollingUpdateConfiguration', 'spot_price': 'spotPrice', 'update_type': 'updateType', 'vpc_subnets': 'vpcSubnets', 'instance_type': 'instanceType', 'machine_image': 'machineImage'})
class AddCapacityOptions(AddAutoScalingGroupCapacityOptions, aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps):
    def __init__(self, *, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[aws_cdk.core.Duration]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[aws_cdk.aws_autoscaling.HealthCheck]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[aws_cdk.aws_autoscaling.UpdateType]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, instance_type: aws_cdk.aws_ec2.InstanceType, machine_image: typing.Optional[aws_cdk.aws_ec2.IMachineImage]=None):
        """The properties for adding instance capacity to an AutoScalingGroup.

        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)
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
        :param instance_type: The EC2 instance type to use when launching instances into the AutoScalingGroup.
        :param machine_image: The ECS-optimized AMI variant to use. For more information, see `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_. Default: - Amazon Linux 2
        """
        if isinstance(rolling_update_configuration, dict): rolling_update_configuration = aws_cdk.aws_autoscaling.RollingUpdateConfiguration(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'instance_type': instance_type,
        }
        if can_containers_access_instance_role is not None: self._values["can_containers_access_instance_role"] = can_containers_access_instance_role
        if spot_instance_draining is not None: self._values["spot_instance_draining"] = spot_instance_draining
        if task_drain_time is not None: self._values["task_drain_time"] = task_drain_time
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
        if machine_image is not None: self._values["machine_image"] = machine_image

    @property
    def can_containers_access_instance_role(self) -> typing.Optional[bool]:
        """Specifies whether the containers can access the container instance role.

        default
        :default: false
        """
        return self._values.get('can_containers_access_instance_role')

    @property
    def spot_instance_draining(self) -> typing.Optional[bool]:
        """Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_.

        default
        :default: false
        """
        return self._values.get('spot_instance_draining')

    @property
    def task_drain_time(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period to wait before force terminating an instance that is draining.

        This creates a Lambda function that is used by a lifecycle hook for the
        AutoScalingGroup that will delay instance termination until all ECS tasks
        have drained from the instance. Set to 0 to disable task draining.

        Set to 0 to disable task draining.

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('task_drain_time')

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
    def health_check(self) -> typing.Optional[aws_cdk.aws_autoscaling.HealthCheck]:
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
    def rolling_update_configuration(self) -> typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]:
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
    def update_type(self) -> typing.Optional[aws_cdk.aws_autoscaling.UpdateType]:
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
        """The EC2 instance type to use when launching instances into the AutoScalingGroup."""
        return self._values.get('instance_type')

    @property
    def machine_image(self) -> typing.Optional[aws_cdk.aws_ec2.IMachineImage]:
        """The ECS-optimized AMI variant to use.

        For more information, see
        `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_.

        default
        :default: - Amazon Linux 2
        """
        return self._values.get('machine_image')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddCapacityOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.AmiHardwareType")
class AmiHardwareType(enum.Enum):
    """The ECS-optimized AMI variant to use.

    For more information, see
    `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_.
    """
    STANDARD = "STANDARD"
    """Use the standard Amazon ECS-optimized AMI."""
    GPU = "GPU"
    """Use the Amazon ECS GPU-optimized AMI."""
    ARM = "ARM"
    """Use the Amazon ECS-optimized Amazon Linux 2 (arm64) AMI."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AppMeshProxyConfigurationConfigProps", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'properties': 'properties'})
class AppMeshProxyConfigurationConfigProps():
    def __init__(self, *, container_name: str, properties: "AppMeshProxyConfigurationProps"):
        """The configuration to use when setting an App Mesh proxy configuration.

        :param container_name: The name of the container that will serve as the App Mesh proxy.
        :param properties: The set of network configuration parameters to provide the Container Network Interface (CNI) plugin.
        """
        if isinstance(properties, dict): properties = AppMeshProxyConfigurationProps(**properties)
        self._values = {
            'container_name': container_name,
            'properties': properties,
        }

    @property
    def container_name(self) -> str:
        """The name of the container that will serve as the App Mesh proxy."""
        return self._values.get('container_name')

    @property
    def properties(self) -> "AppMeshProxyConfigurationProps":
        """The set of network configuration parameters to provide the Container Network Interface (CNI) plugin."""
        return self._values.get('properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppMeshProxyConfigurationConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AppMeshProxyConfigurationProps", jsii_struct_bases=[], name_mapping={'app_ports': 'appPorts', 'proxy_egress_port': 'proxyEgressPort', 'proxy_ingress_port': 'proxyIngressPort', 'egress_ignored_i_ps': 'egressIgnoredIPs', 'egress_ignored_ports': 'egressIgnoredPorts', 'ignored_gid': 'ignoredGID', 'ignored_uid': 'ignoredUID'})
class AppMeshProxyConfigurationProps():
    def __init__(self, *, app_ports: typing.List[jsii.Number], proxy_egress_port: jsii.Number, proxy_ingress_port: jsii.Number, egress_ignored_i_ps: typing.Optional[typing.List[str]]=None, egress_ignored_ports: typing.Optional[typing.List[jsii.Number]]=None, ignored_gid: typing.Optional[jsii.Number]=None, ignored_uid: typing.Optional[jsii.Number]=None):
        """Interface for setting the properties of proxy configuration.

        :param app_ports: The list of ports that the application uses. Network traffic to these ports is forwarded to the ProxyIngressPort and ProxyEgressPort.
        :param proxy_egress_port: Specifies the port that outgoing traffic from the AppPorts is directed to.
        :param proxy_ingress_port: Specifies the port that incoming traffic to the AppPorts is directed to.
        :param egress_ignored_i_ps: The egress traffic going to these specified IP addresses is ignored and not redirected to the ProxyEgressPort. It can be an empty list.
        :param egress_ignored_ports: The egress traffic going to these specified ports is ignored and not redirected to the ProxyEgressPort. It can be an empty list.
        :param ignored_gid: The group ID (GID) of the proxy container as defined by the user parameter in a container definition. This is used to ensure the proxy ignores its own traffic. If IgnoredUID is specified, this field can be empty.
        :param ignored_uid: The user ID (UID) of the proxy container as defined by the user parameter in a container definition. This is used to ensure the proxy ignores its own traffic. If IgnoredGID is specified, this field can be empty.
        """
        self._values = {
            'app_ports': app_ports,
            'proxy_egress_port': proxy_egress_port,
            'proxy_ingress_port': proxy_ingress_port,
        }
        if egress_ignored_i_ps is not None: self._values["egress_ignored_i_ps"] = egress_ignored_i_ps
        if egress_ignored_ports is not None: self._values["egress_ignored_ports"] = egress_ignored_ports
        if ignored_gid is not None: self._values["ignored_gid"] = ignored_gid
        if ignored_uid is not None: self._values["ignored_uid"] = ignored_uid

    @property
    def app_ports(self) -> typing.List[jsii.Number]:
        """The list of ports that the application uses. Network traffic to these ports is forwarded to the ProxyIngressPort and ProxyEgressPort."""
        return self._values.get('app_ports')

    @property
    def proxy_egress_port(self) -> jsii.Number:
        """Specifies the port that outgoing traffic from the AppPorts is directed to."""
        return self._values.get('proxy_egress_port')

    @property
    def proxy_ingress_port(self) -> jsii.Number:
        """Specifies the port that incoming traffic to the AppPorts is directed to."""
        return self._values.get('proxy_ingress_port')

    @property
    def egress_ignored_i_ps(self) -> typing.Optional[typing.List[str]]:
        """The egress traffic going to these specified IP addresses is ignored and not redirected to the ProxyEgressPort.

        It can be an empty list.
        """
        return self._values.get('egress_ignored_i_ps')

    @property
    def egress_ignored_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        """The egress traffic going to these specified ports is ignored and not redirected to the ProxyEgressPort.

        It can be an empty list.
        """
        return self._values.get('egress_ignored_ports')

    @property
    def ignored_gid(self) -> typing.Optional[jsii.Number]:
        """The group ID (GID) of the proxy container as defined by the user parameter in a container definition. This is used to ensure the proxy ignores its own traffic. If IgnoredUID is specified, this field can be empty."""
        return self._values.get('ignored_gid')

    @property
    def ignored_uid(self) -> typing.Optional[jsii.Number]:
        """The user ID (UID) of the proxy container as defined by the user parameter in a container definition. This is used to ensure the proxy ignores its own traffic. If IgnoredGID is specified, this field can be empty."""
        return self._values.get('ignored_uid')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppMeshProxyConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AssetImageProps", jsii_struct_bases=[], name_mapping={'build_args': 'buildArgs', 'target': 'target'})
class AssetImageProps():
    def __init__(self, *, build_args: typing.Optional[typing.Mapping[str,str]]=None, target: typing.Optional[str]=None):
        """The properties for building an AssetImage.

        :param build_args: The arguments to pass to the ``docker build`` command. Default: none
        :param target: Docker target to build to. Default: none
        """
        self._values = {
        }
        if build_args is not None: self._values["build_args"] = build_args
        if target is not None: self._values["target"] = target

    @property
    def build_args(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The arguments to pass to the ``docker build`` command.

        default
        :default: none
        """
        return self._values.get('build_args')

    @property
    def target(self) -> typing.Optional[str]:
        """Docker target to build to.

        default
        :default: none
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AwsLogDriverProps", jsii_struct_bases=[], name_mapping={'stream_prefix': 'streamPrefix', 'datetime_format': 'datetimeFormat', 'log_group': 'logGroup', 'log_retention': 'logRetention', 'multiline_pattern': 'multilinePattern'})
class AwsLogDriverProps():
    def __init__(self, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, multiline_pattern: typing.Optional[str]=None):
        """Specifies the awslogs log driver configuration options.

        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.
        """
        self._values = {
            'stream_prefix': stream_prefix,
        }
        if datetime_format is not None: self._values["datetime_format"] = datetime_format
        if log_group is not None: self._values["log_group"] = log_group
        if log_retention is not None: self._values["log_retention"] = log_retention
        if multiline_pattern is not None: self._values["multiline_pattern"] = multiline_pattern

    @property
    def stream_prefix(self) -> str:
        """Prefix for the log streams.

        The awslogs-stream-prefix option allows you to associate a log stream
        with the specified prefix, the container name, and the ID of the Amazon
        ECS task to which the container belongs. If you specify a prefix with
        this option, then the log stream takes the following format::

            prefix-name/container-name/ecs-task-id
        """
        return self._values.get('stream_prefix')

    @property
    def datetime_format(self) -> typing.Optional[str]:
        """This option defines a multiline start pattern in Python strftime format.

        A log message consists of a line that matches the pattern and any
        following lines that don’t match the pattern. Thus the matched line is
        the delimiter between log messages.

        default
        :default: - No multiline matching.
        """
        return self._values.get('datetime_format')

    @property
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        """The log group to log to.

        default
        :default: - A log group is automatically created.
        """
        return self._values.get('log_group')

    @property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        """The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct.

        default
        :default: - Logs never expire.
        """
        return self._values.get('log_retention')

    @property
    def multiline_pattern(self) -> typing.Optional[str]:
        """This option defines a multiline start pattern using a regular expression.

        A log message consists of a line that matches the pattern and any
        following lines that don’t match the pattern. Thus the matched line is
        the delimiter between log messages.

        This option is ignored if datetimeFormat is also configured.

        default
        :default: - No multiline matching.
        """
        return self._values.get('multiline_pattern')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.BaseLogDriverProps", jsii_struct_bases=[], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag'})
class BaseLogDriverProps():
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None):
        """
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag

    @property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env
        """
        return self._values.get('env')

    @property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex
        """
        return self._values.get('env_regex')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels
        """
        return self._values.get('labels')

    @property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID
        """
        return self._values.get('tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.BaseServiceOptions", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName'})
class BaseServiceOptions():
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None):
        """The properties for the base Ec2Service or FargateService service.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        self._values = {
            'cluster': cluster,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name

    @property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service."""
        return self._values.get('cluster')

    @property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE
        """
        return self._values.get('propagate_tags')

    @property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseServiceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.BaseServiceProps", jsii_struct_bases=[BaseServiceOptions], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'launch_type': 'launchType'})
class BaseServiceProps(BaseServiceOptions):
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None, launch_type: "LaunchType"):
        """Complete base service properties that are required to be supplied by the implementation of the BaseService class.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param launch_type: The launch type on which to run your service. Valid values are: LaunchType.ECS or LaunchType.FARGATE
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        self._values = {
            'cluster': cluster,
            'launch_type': launch_type,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name

    @property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service."""
        return self._values.get('cluster')

    @property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE
        """
        return self._values.get('propagate_tags')

    @property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @property
    def launch_type(self) -> "LaunchType":
        """The launch type on which to run your service.

        Valid values are: LaunchType.ECS or LaunchType.FARGATE
        """
        return self._values.get('launch_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.BinPackResource")
class BinPackResource(enum.Enum):
    """Instance resource used for bin packing."""
    CPU = "CPU"
    """Fill up hosts' CPU allocations first."""
    MEMORY = "MEMORY"
    """Fill up hosts' memory allocations first."""

class BuiltInAttributes(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.BuiltInAttributes"):
    """The built-in container instance attributes."""
    def __init__(self) -> None:
        jsii.create(BuiltInAttributes, self, [])

    @classproperty
    @jsii.member(jsii_name="AMI_ID")
    def AMI_ID(cls) -> str:
        """The AMI id the instance is using."""
        return jsii.sget(cls, "AMI_ID")

    @classproperty
    @jsii.member(jsii_name="AVAILABILITY_ZONE")
    def AVAILABILITY_ZONE(cls) -> str:
        """The AvailabilityZone where the instance is running in."""
        return jsii.sget(cls, "AVAILABILITY_ZONE")

    @classproperty
    @jsii.member(jsii_name="INSTANCE_ID")
    def INSTANCE_ID(cls) -> str:
        """The id of the instance."""
        return jsii.sget(cls, "INSTANCE_ID")

    @classproperty
    @jsii.member(jsii_name="INSTANCE_TYPE")
    def INSTANCE_TYPE(cls) -> str:
        """The EC2 instance type."""
        return jsii.sget(cls, "INSTANCE_TYPE")

    @classproperty
    @jsii.member(jsii_name="OS_TYPE")
    def OS_TYPE(cls) -> str:
        """The operating system of the instance.

        Either 'linux' or 'windows'.
        """
        return jsii.sget(cls, "OS_TYPE")


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Capability")
class Capability(enum.Enum):
    """A Linux capability."""
    ALL = "ALL"
    AUDIT_CONTROL = "AUDIT_CONTROL"
    AUDIT_WRITE = "AUDIT_WRITE"
    BLOCK_SUSPEND = "BLOCK_SUSPEND"
    CHOWN = "CHOWN"
    DAC_OVERRIDE = "DAC_OVERRIDE"
    DAC_READ_SEARCH = "DAC_READ_SEARCH"
    FOWNER = "FOWNER"
    FSETID = "FSETID"
    IPC_LOCK = "IPC_LOCK"
    IPC_OWNER = "IPC_OWNER"
    KILL = "KILL"
    LEASE = "LEASE"
    LINUX_IMMUTABLE = "LINUX_IMMUTABLE"
    MAC_ADMIN = "MAC_ADMIN"
    MAC_OVERRIDE = "MAC_OVERRIDE"
    MKNOD = "MKNOD"
    NET_ADMIN = "NET_ADMIN"
    NET_BIND_SERVICE = "NET_BIND_SERVICE"
    NET_BROADCAST = "NET_BROADCAST"
    NET_RAW = "NET_RAW"
    SETFCAP = "SETFCAP"
    SETGID = "SETGID"
    SETPCAP = "SETPCAP"
    SETUID = "SETUID"
    SYS_ADMIN = "SYS_ADMIN"
    SYS_BOOT = "SYS_BOOT"
    SYS_CHROOT = "SYS_CHROOT"
    SYS_MODULE = "SYS_MODULE"
    SYS_NICE = "SYS_NICE"
    SYS_PACCT = "SYS_PACCT"
    SYS_PTRACE = "SYS_PTRACE"
    SYS_RAWIO = "SYS_RAWIO"
    SYS_RESOURCE = "SYS_RESOURCE"
    SYS_TIME = "SYS_TIME"
    SYS_TTY_CONFIG = "SYS_TTY_CONFIG"
    SYSLOG = "SYSLOG"
    WAKE_ALARM = "WAKE_ALARM"

@jsii.implements(aws_cdk.core.IInspectable)
class CfnCluster(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnCluster"):
    """A CloudFormation ``AWS::ECS::Cluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::Cluster
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ECS::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param cluster_name: ``AWS::ECS::Cluster.ClusterName``.
        :param tags: ``AWS::ECS::Cluster.Tags``.
        """
        props = CfnClusterProps(cluster_name=cluster_name, tags=tags)

        jsii.create(CfnCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ECS::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Cluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[str]):
        return jsii.set(self, "clusterName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnClusterProps", jsii_struct_bases=[], name_mapping={'cluster_name': 'clusterName', 'tags': 'tags'})
class CfnClusterProps():
    def __init__(self, *, cluster_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::ECS::Cluster``.

        :param cluster_name: ``AWS::ECS::Cluster.ClusterName``.
        :param tags: ``AWS::ECS::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html
        """
        self._values = {
        }
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if tags is not None: self._values["tags"] = tags

    @property
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Cluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustername
        """
        return self._values.get('cluster_name')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ECS::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnService(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnService"):
    """A CloudFormation ``AWS::ECS::Service``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::Service
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: str, cluster: typing.Optional[str]=None, deployment_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentConfigurationProperty"]]]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, health_check_grace_period_seconds: typing.Optional[jsii.Number]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LoadBalancerProperty"]]]]]=None, network_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NetworkConfigurationProperty"]]]=None, placement_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PlacementConstraintProperty"]]]]]=None, placement_strategies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PlacementStrategyProperty"]]]]]=None, platform_version: typing.Optional[str]=None, propagate_tags: typing.Optional[str]=None, role: typing.Optional[str]=None, scheduling_strategy: typing.Optional[str]=None, service_name: typing.Optional[str]=None, service_registries: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ServiceRegistryProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ECS::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param task_definition: ``AWS::ECS::Service.TaskDefinition``.
        :param cluster: ``AWS::ECS::Service.Cluster``.
        :param deployment_configuration: ``AWS::ECS::Service.DeploymentConfiguration``.
        :param desired_count: ``AWS::ECS::Service.DesiredCount``.
        :param enable_ecs_managed_tags: ``AWS::ECS::Service.EnableECSManagedTags``.
        :param health_check_grace_period_seconds: ``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.
        :param launch_type: ``AWS::ECS::Service.LaunchType``.
        :param load_balancers: ``AWS::ECS::Service.LoadBalancers``.
        :param network_configuration: ``AWS::ECS::Service.NetworkConfiguration``.
        :param placement_constraints: ``AWS::ECS::Service.PlacementConstraints``.
        :param placement_strategies: ``AWS::ECS::Service.PlacementStrategies``.
        :param platform_version: ``AWS::ECS::Service.PlatformVersion``.
        :param propagate_tags: ``AWS::ECS::Service.PropagateTags``.
        :param role: ``AWS::ECS::Service.Role``.
        :param scheduling_strategy: ``AWS::ECS::Service.SchedulingStrategy``.
        :param service_name: ``AWS::ECS::Service.ServiceName``.
        :param service_registries: ``AWS::ECS::Service.ServiceRegistries``.
        :param tags: ``AWS::ECS::Service.Tags``.
        """
        props = CfnServiceProps(task_definition=task_definition, cluster=cluster, deployment_configuration=deployment_configuration, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period_seconds=health_check_grace_period_seconds, launch_type=launch_type, load_balancers=load_balancers, network_configuration=network_configuration, placement_constraints=placement_constraints, placement_strategies=placement_strategies, platform_version=platform_version, propagate_tags=propagate_tags, role=role, scheduling_strategy=scheduling_strategy, service_name=service_name, service_registries=service_registries, tags=tags)

        jsii.create(CfnService, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ECS::Service.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> str:
        """``AWS::ECS::Service.TaskDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-taskdefinition
        """
        return jsii.get(self, "taskDefinition")

    @task_definition.setter
    def task_definition(self, value: str):
        return jsii.set(self, "taskDefinition", value)

    @property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-cluster
        """
        return jsii.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: typing.Optional[str]):
        return jsii.set(self, "cluster", value)

    @property
    @jsii.member(jsii_name="deploymentConfiguration")
    def deployment_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentConfigurationProperty"]]]:
        """``AWS::ECS::Service.DeploymentConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentconfiguration
        """
        return jsii.get(self, "deploymentConfiguration")

    @deployment_configuration.setter
    def deployment_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentConfigurationProperty"]]]):
        return jsii.set(self, "deploymentConfiguration", value)

    @property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.DesiredCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-desiredcount
        """
        return jsii.get(self, "desiredCount")

    @desired_count.setter
    def desired_count(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "desiredCount", value)

    @property
    @jsii.member(jsii_name="enableEcsManagedTags")
    def enable_ecs_managed_tags(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ECS::Service.EnableECSManagedTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-enableecsmanagedtags
        """
        return jsii.get(self, "enableEcsManagedTags")

    @enable_ecs_managed_tags.setter
    def enable_ecs_managed_tags(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "enableEcsManagedTags", value)

    @property
    @jsii.member(jsii_name="healthCheckGracePeriodSeconds")
    def health_check_grace_period_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-healthcheckgraceperiodseconds
        """
        return jsii.get(self, "healthCheckGracePeriodSeconds")

    @health_check_grace_period_seconds.setter
    def health_check_grace_period_seconds(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "healthCheckGracePeriodSeconds", value)

    @property
    @jsii.member(jsii_name="launchType")
    def launch_type(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.LaunchType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-launchtype
        """
        return jsii.get(self, "launchType")

    @launch_type.setter
    def launch_type(self, value: typing.Optional[str]):
        return jsii.set(self, "launchType", value)

    @property
    @jsii.member(jsii_name="loadBalancers")
    def load_balancers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LoadBalancerProperty"]]]]]:
        """``AWS::ECS::Service.LoadBalancers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-loadbalancers
        """
        return jsii.get(self, "loadBalancers")

    @load_balancers.setter
    def load_balancers(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LoadBalancerProperty"]]]]]):
        return jsii.set(self, "loadBalancers", value)

    @property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NetworkConfigurationProperty"]]]:
        """``AWS::ECS::Service.NetworkConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-networkconfiguration
        """
        return jsii.get(self, "networkConfiguration")

    @network_configuration.setter
    def network_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NetworkConfigurationProperty"]]]):
        return jsii.set(self, "networkConfiguration", value)

    @property
    @jsii.member(jsii_name="placementConstraints")
    def placement_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PlacementConstraintProperty"]]]]]:
        """``AWS::ECS::Service.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementconstraints
        """
        return jsii.get(self, "placementConstraints")

    @placement_constraints.setter
    def placement_constraints(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PlacementConstraintProperty"]]]]]):
        return jsii.set(self, "placementConstraints", value)

    @property
    @jsii.member(jsii_name="placementStrategies")
    def placement_strategies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PlacementStrategyProperty"]]]]]:
        """``AWS::ECS::Service.PlacementStrategies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementstrategies
        """
        return jsii.get(self, "placementStrategies")

    @placement_strategies.setter
    def placement_strategies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PlacementStrategyProperty"]]]]]):
        return jsii.set(self, "placementStrategies", value)

    @property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PlatformVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-platformversion
        """
        return jsii.get(self, "platformVersion")

    @platform_version.setter
    def platform_version(self, value: typing.Optional[str]):
        return jsii.set(self, "platformVersion", value)

    @property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PropagateTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-propagatetags
        """
        return jsii.get(self, "propagateTags")

    @propagate_tags.setter
    def propagate_tags(self, value: typing.Optional[str]):
        return jsii.set(self, "propagateTags", value)

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-role
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: typing.Optional[str]):
        return jsii.set(self, "role", value)

    @property
    @jsii.member(jsii_name="schedulingStrategy")
    def scheduling_strategy(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.SchedulingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-schedulingstrategy
        """
        return jsii.get(self, "schedulingStrategy")

    @scheduling_strategy.setter
    def scheduling_strategy(self, value: typing.Optional[str]):
        return jsii.set(self, "schedulingStrategy", value)

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.ServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-servicename
        """
        return jsii.get(self, "serviceName")

    @service_name.setter
    def service_name(self, value: typing.Optional[str]):
        return jsii.set(self, "serviceName", value)

    @property
    @jsii.member(jsii_name="serviceRegistries")
    def service_registries(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ServiceRegistryProperty"]]]]]:
        """``AWS::ECS::Service.ServiceRegistries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-serviceregistries
        """
        return jsii.get(self, "serviceRegistries")

    @service_registries.setter
    def service_registries(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ServiceRegistryProperty"]]]]]):
        return jsii.set(self, "serviceRegistries", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.AwsVpcConfigurationProperty", jsii_struct_bases=[], name_mapping={'subnets': 'subnets', 'assign_public_ip': 'assignPublicIp', 'security_groups': 'securityGroups'})
    class AwsVpcConfigurationProperty():
        def __init__(self, *, subnets: typing.List[str], assign_public_ip: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None):
            """
            :param subnets: ``CfnService.AwsVpcConfigurationProperty.Subnets``.
            :param assign_public_ip: ``CfnService.AwsVpcConfigurationProperty.AssignPublicIp``.
            :param security_groups: ``CfnService.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html
            """
            self._values = {
                'subnets': subnets,
            }
            if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None: self._values["security_groups"] = security_groups

        @property
        def subnets(self) -> typing.List[str]:
            """``CfnService.AwsVpcConfigurationProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-subnets
            """
            return self._values.get('subnets')

        @property
        def assign_public_ip(self) -> typing.Optional[str]:
            """``CfnService.AwsVpcConfigurationProperty.AssignPublicIp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-assignpublicip
            """
            return self._values.get('assign_public_ip')

        @property
        def security_groups(self) -> typing.Optional[typing.List[str]]:
            """``CfnService.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-securitygroups
            """
            return self._values.get('security_groups')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AwsVpcConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.DeploymentConfigurationProperty", jsii_struct_bases=[], name_mapping={'maximum_percent': 'maximumPercent', 'minimum_healthy_percent': 'minimumHealthyPercent'})
    class DeploymentConfigurationProperty():
        def __init__(self, *, maximum_percent: typing.Optional[jsii.Number]=None, minimum_healthy_percent: typing.Optional[jsii.Number]=None):
            """
            :param maximum_percent: ``CfnService.DeploymentConfigurationProperty.MaximumPercent``.
            :param minimum_healthy_percent: ``CfnService.DeploymentConfigurationProperty.MinimumHealthyPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html
            """
            self._values = {
            }
            if maximum_percent is not None: self._values["maximum_percent"] = maximum_percent
            if minimum_healthy_percent is not None: self._values["minimum_healthy_percent"] = minimum_healthy_percent

        @property
        def maximum_percent(self) -> typing.Optional[jsii.Number]:
            """``CfnService.DeploymentConfigurationProperty.MaximumPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html#cfn-ecs-service-deploymentconfiguration-maximumpercent
            """
            return self._values.get('maximum_percent')

        @property
        def minimum_healthy_percent(self) -> typing.Optional[jsii.Number]:
            """``CfnService.DeploymentConfigurationProperty.MinimumHealthyPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html#cfn-ecs-service-deploymentconfiguration-minimumhealthypercent
            """
            return self._values.get('minimum_healthy_percent')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.LoadBalancerProperty", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'container_name': 'containerName', 'load_balancer_name': 'loadBalancerName', 'target_group_arn': 'targetGroupArn'})
    class LoadBalancerProperty():
        def __init__(self, *, container_port: jsii.Number, container_name: typing.Optional[str]=None, load_balancer_name: typing.Optional[str]=None, target_group_arn: typing.Optional[str]=None):
            """
            :param container_port: ``CfnService.LoadBalancerProperty.ContainerPort``.
            :param container_name: ``CfnService.LoadBalancerProperty.ContainerName``.
            :param load_balancer_name: ``CfnService.LoadBalancerProperty.LoadBalancerName``.
            :param target_group_arn: ``CfnService.LoadBalancerProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html
            """
            self._values = {
                'container_port': container_port,
            }
            if container_name is not None: self._values["container_name"] = container_name
            if load_balancer_name is not None: self._values["load_balancer_name"] = load_balancer_name
            if target_group_arn is not None: self._values["target_group_arn"] = target_group_arn

        @property
        def container_port(self) -> jsii.Number:
            """``CfnService.LoadBalancerProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-containerport
            """
            return self._values.get('container_port')

        @property
        def container_name(self) -> typing.Optional[str]:
            """``CfnService.LoadBalancerProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-containername
            """
            return self._values.get('container_name')

        @property
        def load_balancer_name(self) -> typing.Optional[str]:
            """``CfnService.LoadBalancerProperty.LoadBalancerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-loadbalancername
            """
            return self._values.get('load_balancer_name')

        @property
        def target_group_arn(self) -> typing.Optional[str]:
            """``CfnService.LoadBalancerProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-targetgrouparn
            """
            return self._values.get('target_group_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoadBalancerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.NetworkConfigurationProperty", jsii_struct_bases=[], name_mapping={'awsvpc_configuration': 'awsvpcConfiguration'})
    class NetworkConfigurationProperty():
        def __init__(self, *, awsvpc_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.AwsVpcConfigurationProperty"]]]=None):
            """
            :param awsvpc_configuration: ``CfnService.NetworkConfigurationProperty.AwsvpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-networkconfiguration.html
            """
            self._values = {
            }
            if awsvpc_configuration is not None: self._values["awsvpc_configuration"] = awsvpc_configuration

        @property
        def awsvpc_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.AwsVpcConfigurationProperty"]]]:
            """``CfnService.NetworkConfigurationProperty.AwsvpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-networkconfiguration.html#cfn-ecs-service-networkconfiguration-awsvpcconfiguration
            """
            return self._values.get('awsvpc_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NetworkConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.PlacementConstraintProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'expression': 'expression'})
    class PlacementConstraintProperty():
        def __init__(self, *, type: str, expression: typing.Optional[str]=None):
            """
            :param type: ``CfnService.PlacementConstraintProperty.Type``.
            :param expression: ``CfnService.PlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html
            """
            self._values = {
                'type': type,
            }
            if expression is not None: self._values["expression"] = expression

        @property
        def type(self) -> str:
            """``CfnService.PlacementConstraintProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html#cfn-ecs-service-placementconstraint-type
            """
            return self._values.get('type')

        @property
        def expression(self) -> typing.Optional[str]:
            """``CfnService.PlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html#cfn-ecs-service-placementconstraint-expression
            """
            return self._values.get('expression')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PlacementConstraintProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.PlacementStrategyProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'field': 'field'})
    class PlacementStrategyProperty():
        def __init__(self, *, type: str, field: typing.Optional[str]=None):
            """
            :param type: ``CfnService.PlacementStrategyProperty.Type``.
            :param field: ``CfnService.PlacementStrategyProperty.Field``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html
            """
            self._values = {
                'type': type,
            }
            if field is not None: self._values["field"] = field

        @property
        def type(self) -> str:
            """``CfnService.PlacementStrategyProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html#cfn-ecs-service-placementstrategy-type
            """
            return self._values.get('type')

        @property
        def field(self) -> typing.Optional[str]:
            """``CfnService.PlacementStrategyProperty.Field``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html#cfn-ecs-service-placementstrategy-field
            """
            return self._values.get('field')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PlacementStrategyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.ServiceRegistryProperty", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'container_port': 'containerPort', 'port': 'port', 'registry_arn': 'registryArn'})
    class ServiceRegistryProperty():
        def __init__(self, *, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, port: typing.Optional[jsii.Number]=None, registry_arn: typing.Optional[str]=None):
            """
            :param container_name: ``CfnService.ServiceRegistryProperty.ContainerName``.
            :param container_port: ``CfnService.ServiceRegistryProperty.ContainerPort``.
            :param port: ``CfnService.ServiceRegistryProperty.Port``.
            :param registry_arn: ``CfnService.ServiceRegistryProperty.RegistryArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html
            """
            self._values = {
            }
            if container_name is not None: self._values["container_name"] = container_name
            if container_port is not None: self._values["container_port"] = container_port
            if port is not None: self._values["port"] = port
            if registry_arn is not None: self._values["registry_arn"] = registry_arn

        @property
        def container_name(self) -> typing.Optional[str]:
            """``CfnService.ServiceRegistryProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-containername
            """
            return self._values.get('container_name')

        @property
        def container_port(self) -> typing.Optional[jsii.Number]:
            """``CfnService.ServiceRegistryProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-containerport
            """
            return self._values.get('container_port')

        @property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnService.ServiceRegistryProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-port
            """
            return self._values.get('port')

        @property
        def registry_arn(self) -> typing.Optional[str]:
            """``CfnService.ServiceRegistryProperty.RegistryArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-registryarn
            """
            return self._values.get('registry_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ServiceRegistryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnServiceProps", jsii_struct_bases=[], name_mapping={'task_definition': 'taskDefinition', 'cluster': 'cluster', 'deployment_configuration': 'deploymentConfiguration', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableEcsManagedTags', 'health_check_grace_period_seconds': 'healthCheckGracePeriodSeconds', 'launch_type': 'launchType', 'load_balancers': 'loadBalancers', 'network_configuration': 'networkConfiguration', 'placement_constraints': 'placementConstraints', 'placement_strategies': 'placementStrategies', 'platform_version': 'platformVersion', 'propagate_tags': 'propagateTags', 'role': 'role', 'scheduling_strategy': 'schedulingStrategy', 'service_name': 'serviceName', 'service_registries': 'serviceRegistries', 'tags': 'tags'})
class CfnServiceProps():
    def __init__(self, *, task_definition: str, cluster: typing.Optional[str]=None, deployment_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.DeploymentConfigurationProperty"]]]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, health_check_grace_period_seconds: typing.Optional[jsii.Number]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.LoadBalancerProperty"]]]]]=None, network_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.NetworkConfigurationProperty"]]]=None, placement_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.PlacementConstraintProperty"]]]]]=None, placement_strategies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.PlacementStrategyProperty"]]]]]=None, platform_version: typing.Optional[str]=None, propagate_tags: typing.Optional[str]=None, role: typing.Optional[str]=None, scheduling_strategy: typing.Optional[str]=None, service_name: typing.Optional[str]=None, service_registries: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.ServiceRegistryProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::ECS::Service``.

        :param task_definition: ``AWS::ECS::Service.TaskDefinition``.
        :param cluster: ``AWS::ECS::Service.Cluster``.
        :param deployment_configuration: ``AWS::ECS::Service.DeploymentConfiguration``.
        :param desired_count: ``AWS::ECS::Service.DesiredCount``.
        :param enable_ecs_managed_tags: ``AWS::ECS::Service.EnableECSManagedTags``.
        :param health_check_grace_period_seconds: ``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.
        :param launch_type: ``AWS::ECS::Service.LaunchType``.
        :param load_balancers: ``AWS::ECS::Service.LoadBalancers``.
        :param network_configuration: ``AWS::ECS::Service.NetworkConfiguration``.
        :param placement_constraints: ``AWS::ECS::Service.PlacementConstraints``.
        :param placement_strategies: ``AWS::ECS::Service.PlacementStrategies``.
        :param platform_version: ``AWS::ECS::Service.PlatformVersion``.
        :param propagate_tags: ``AWS::ECS::Service.PropagateTags``.
        :param role: ``AWS::ECS::Service.Role``.
        :param scheduling_strategy: ``AWS::ECS::Service.SchedulingStrategy``.
        :param service_name: ``AWS::ECS::Service.ServiceName``.
        :param service_registries: ``AWS::ECS::Service.ServiceRegistries``.
        :param tags: ``AWS::ECS::Service.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html
        """
        self._values = {
            'task_definition': task_definition,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if deployment_configuration is not None: self._values["deployment_configuration"] = deployment_configuration
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period_seconds is not None: self._values["health_check_grace_period_seconds"] = health_check_grace_period_seconds
        if launch_type is not None: self._values["launch_type"] = launch_type
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if network_configuration is not None: self._values["network_configuration"] = network_configuration
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None: self._values["placement_strategies"] = placement_strategies
        if platform_version is not None: self._values["platform_version"] = platform_version
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if role is not None: self._values["role"] = role
        if scheduling_strategy is not None: self._values["scheduling_strategy"] = scheduling_strategy
        if service_name is not None: self._values["service_name"] = service_name
        if service_registries is not None: self._values["service_registries"] = service_registries
        if tags is not None: self._values["tags"] = tags

    @property
    def task_definition(self) -> str:
        """``AWS::ECS::Service.TaskDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-taskdefinition
        """
        return self._values.get('task_definition')

    @property
    def cluster(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-cluster
        """
        return self._values.get('cluster')

    @property
    def deployment_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.DeploymentConfigurationProperty"]]]:
        """``AWS::ECS::Service.DeploymentConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentconfiguration
        """
        return self._values.get('deployment_configuration')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.DesiredCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-desiredcount
        """
        return self._values.get('desired_count')

    @property
    def enable_ecs_managed_tags(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ECS::Service.EnableECSManagedTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-enableecsmanagedtags
        """
        return self._values.get('enable_ecs_managed_tags')

    @property
    def health_check_grace_period_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-healthcheckgraceperiodseconds
        """
        return self._values.get('health_check_grace_period_seconds')

    @property
    def launch_type(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.LaunchType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-launchtype
        """
        return self._values.get('launch_type')

    @property
    def load_balancers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.LoadBalancerProperty"]]]]]:
        """``AWS::ECS::Service.LoadBalancers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-loadbalancers
        """
        return self._values.get('load_balancers')

    @property
    def network_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.NetworkConfigurationProperty"]]]:
        """``AWS::ECS::Service.NetworkConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-networkconfiguration
        """
        return self._values.get('network_configuration')

    @property
    def placement_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.PlacementConstraintProperty"]]]]]:
        """``AWS::ECS::Service.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementconstraints
        """
        return self._values.get('placement_constraints')

    @property
    def placement_strategies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.PlacementStrategyProperty"]]]]]:
        """``AWS::ECS::Service.PlacementStrategies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementstrategies
        """
        return self._values.get('placement_strategies')

    @property
    def platform_version(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PlatformVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-platformversion
        """
        return self._values.get('platform_version')

    @property
    def propagate_tags(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PropagateTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-propagatetags
        """
        return self._values.get('propagate_tags')

    @property
    def role(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-role
        """
        return self._values.get('role')

    @property
    def scheduling_strategy(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.SchedulingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-schedulingstrategy
        """
        return self._values.get('scheduling_strategy')

    @property
    def service_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.ServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-servicename
        """
        return self._values.get('service_name')

    @property
    def service_registries(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.ServiceRegistryProperty"]]]]]:
        """``AWS::ECS::Service.ServiceRegistries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-serviceregistries
        """
        return self._values.get('service_registries')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ECS::Service.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTaskDefinition(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition"):
    """A CloudFormation ``AWS::ECS::TaskDefinition``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, container_definitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]=None, cpu: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, family: typing.Optional[str]=None, inference_accelerators: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "InferenceAcceleratorProperty"]]]]]=None, ipc_mode: typing.Optional[str]=None, memory: typing.Optional[str]=None, network_mode: typing.Optional[str]=None, pid_mode: typing.Optional[str]=None, placement_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TaskDefinitionPlacementConstraintProperty"]]]]]=None, proxy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProxyConfigurationProperty"]]]=None, requires_compatibilities: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, task_role_arn: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeProperty"]]]]]=None) -> None:
        """Create a new ``AWS::ECS::TaskDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param container_definitions: ``AWS::ECS::TaskDefinition.ContainerDefinitions``.
        :param cpu: ``AWS::ECS::TaskDefinition.Cpu``.
        :param execution_role_arn: ``AWS::ECS::TaskDefinition.ExecutionRoleArn``.
        :param family: ``AWS::ECS::TaskDefinition.Family``.
        :param inference_accelerators: ``AWS::ECS::TaskDefinition.InferenceAccelerators``.
        :param ipc_mode: ``AWS::ECS::TaskDefinition.IpcMode``.
        :param memory: ``AWS::ECS::TaskDefinition.Memory``.
        :param network_mode: ``AWS::ECS::TaskDefinition.NetworkMode``.
        :param pid_mode: ``AWS::ECS::TaskDefinition.PidMode``.
        :param placement_constraints: ``AWS::ECS::TaskDefinition.PlacementConstraints``.
        :param proxy_configuration: ``AWS::ECS::TaskDefinition.ProxyConfiguration``.
        :param requires_compatibilities: ``AWS::ECS::TaskDefinition.RequiresCompatibilities``.
        :param tags: ``AWS::ECS::TaskDefinition.Tags``.
        :param task_role_arn: ``AWS::ECS::TaskDefinition.TaskRoleArn``.
        :param volumes: ``AWS::ECS::TaskDefinition.Volumes``.
        """
        props = CfnTaskDefinitionProps(container_definitions=container_definitions, cpu=cpu, execution_role_arn=execution_role_arn, family=family, inference_accelerators=inference_accelerators, ipc_mode=ipc_mode, memory=memory, network_mode=network_mode, pid_mode=pid_mode, placement_constraints=placement_constraints, proxy_configuration=proxy_configuration, requires_compatibilities=requires_compatibilities, tags=tags, task_role_arn=task_role_arn, volumes=volumes)

        jsii.create(CfnTaskDefinition, self, [scope, id, props])

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
        """``AWS::ECS::TaskDefinition.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="containerDefinitions")
    def container_definitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ECS::TaskDefinition.ContainerDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-containerdefinitions
        """
        return jsii.get(self, "containerDefinitions")

    @container_definitions.setter
    def container_definitions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "containerDefinitions", value)

    @property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Cpu``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-cpu
        """
        return jsii.get(self, "cpu")

    @cpu.setter
    def cpu(self, value: typing.Optional[str]):
        return jsii.set(self, "cpu", value)

    @property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "executionRoleArn", value)

    @property
    @jsii.member(jsii_name="family")
    def family(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-family
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: typing.Optional[str]):
        return jsii.set(self, "family", value)

    @property
    @jsii.member(jsii_name="inferenceAccelerators")
    def inference_accelerators(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "InferenceAcceleratorProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.InferenceAccelerators``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-inferenceaccelerators
        """
        return jsii.get(self, "inferenceAccelerators")

    @inference_accelerators.setter
    def inference_accelerators(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "InferenceAcceleratorProperty"]]]]]):
        return jsii.set(self, "inferenceAccelerators", value)

    @property
    @jsii.member(jsii_name="ipcMode")
    def ipc_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.IpcMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-ipcmode
        """
        return jsii.get(self, "ipcMode")

    @ipc_mode.setter
    def ipc_mode(self, value: typing.Optional[str]):
        return jsii.set(self, "ipcMode", value)

    @property
    @jsii.member(jsii_name="memory")
    def memory(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Memory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-memory
        """
        return jsii.get(self, "memory")

    @memory.setter
    def memory(self, value: typing.Optional[str]):
        return jsii.set(self, "memory", value)

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.NetworkMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-networkmode
        """
        return jsii.get(self, "networkMode")

    @network_mode.setter
    def network_mode(self, value: typing.Optional[str]):
        return jsii.set(self, "networkMode", value)

    @property
    @jsii.member(jsii_name="pidMode")
    def pid_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.PidMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-pidmode
        """
        return jsii.get(self, "pidMode")

    @pid_mode.setter
    def pid_mode(self, value: typing.Optional[str]):
        return jsii.set(self, "pidMode", value)

    @property
    @jsii.member(jsii_name="placementConstraints")
    def placement_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TaskDefinitionPlacementConstraintProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-placementconstraints
        """
        return jsii.get(self, "placementConstraints")

    @placement_constraints.setter
    def placement_constraints(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TaskDefinitionPlacementConstraintProperty"]]]]]):
        return jsii.set(self, "placementConstraints", value)

    @property
    @jsii.member(jsii_name="proxyConfiguration")
    def proxy_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProxyConfigurationProperty"]]]:
        """``AWS::ECS::TaskDefinition.ProxyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-proxyconfiguration
        """
        return jsii.get(self, "proxyConfiguration")

    @proxy_configuration.setter
    def proxy_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProxyConfigurationProperty"]]]):
        return jsii.set(self, "proxyConfiguration", value)

    @property
    @jsii.member(jsii_name="requiresCompatibilities")
    def requires_compatibilities(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ECS::TaskDefinition.RequiresCompatibilities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-requirescompatibilities
        """
        return jsii.get(self, "requiresCompatibilities")

    @requires_compatibilities.setter
    def requires_compatibilities(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "requiresCompatibilities", value)

    @property
    @jsii.member(jsii_name="taskRoleArn")
    def task_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.TaskRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-taskrolearn
        """
        return jsii.get(self, "taskRoleArn")

    @task_role_arn.setter
    def task_role_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "taskRoleArn", value)

    @property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.Volumes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-volumes
        """
        return jsii.get(self, "volumes")

    @volumes.setter
    def volumes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeProperty"]]]]]):
        return jsii.set(self, "volumes", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ContainerDefinitionProperty", jsii_struct_bases=[], name_mapping={'command': 'command', 'cpu': 'cpu', 'depends_on': 'dependsOn', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'health_check': 'healthCheck', 'hostname': 'hostname', 'image': 'image', 'interactive': 'interactive', 'links': 'links', 'linux_parameters': 'linuxParameters', 'log_configuration': 'logConfiguration', 'memory': 'memory', 'memory_reservation': 'memoryReservation', 'mount_points': 'mountPoints', 'name': 'name', 'port_mappings': 'portMappings', 'privileged': 'privileged', 'pseudo_terminal': 'pseudoTerminal', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'repository_credentials': 'repositoryCredentials', 'resource_requirements': 'resourceRequirements', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'system_controls': 'systemControls', 'ulimits': 'ulimits', 'user': 'user', 'volumes_from': 'volumesFrom', 'working_directory': 'workingDirectory'})
    class ContainerDefinitionProperty():
        def __init__(self, *, command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.ContainerDependencyProperty"]]]]]=None, disable_networking: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.KeyValuePairProperty"]]]]]=None, essential: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, extra_hosts: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.HostEntryProperty"]]]]]=None, health_check: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.HealthCheckProperty"]]]=None, hostname: typing.Optional[str]=None, image: typing.Optional[str]=None, interactive: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, links: typing.Optional[typing.List[str]]=None, linux_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.LinuxParametersProperty"]]]=None, log_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.LogConfigurationProperty"]]]=None, memory: typing.Optional[jsii.Number]=None, memory_reservation: typing.Optional[jsii.Number]=None, mount_points: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.MountPointProperty"]]]]]=None, name: typing.Optional[str]=None, port_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.PortMappingProperty"]]]]]=None, privileged: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, pseudo_terminal: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, readonly_root_filesystem: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, repository_credentials: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]]]=None, resource_requirements: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.ResourceRequirementProperty"]]]]]=None, secrets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.SecretProperty"]]]]]=None, start_timeout: typing.Optional[jsii.Number]=None, stop_timeout: typing.Optional[jsii.Number]=None, system_controls: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.SystemControlProperty"]]]]]=None, ulimits: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.UlimitProperty"]]]]]=None, user: typing.Optional[str]=None, volumes_from: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.VolumeFromProperty"]]]]]=None, working_directory: typing.Optional[str]=None):
            """
            :param command: ``CfnTaskDefinition.ContainerDefinitionProperty.Command``.
            :param cpu: ``CfnTaskDefinition.ContainerDefinitionProperty.Cpu``.
            :param depends_on: ``CfnTaskDefinition.ContainerDefinitionProperty.DependsOn``.
            :param disable_networking: ``CfnTaskDefinition.ContainerDefinitionProperty.DisableNetworking``.
            :param dns_search_domains: ``CfnTaskDefinition.ContainerDefinitionProperty.DnsSearchDomains``.
            :param dns_servers: ``CfnTaskDefinition.ContainerDefinitionProperty.DnsServers``.
            :param docker_labels: ``CfnTaskDefinition.ContainerDefinitionProperty.DockerLabels``.
            :param docker_security_options: ``CfnTaskDefinition.ContainerDefinitionProperty.DockerSecurityOptions``.
            :param entry_point: ``CfnTaskDefinition.ContainerDefinitionProperty.EntryPoint``.
            :param environment: ``CfnTaskDefinition.ContainerDefinitionProperty.Environment``.
            :param essential: ``CfnTaskDefinition.ContainerDefinitionProperty.Essential``.
            :param extra_hosts: ``CfnTaskDefinition.ContainerDefinitionProperty.ExtraHosts``.
            :param health_check: ``CfnTaskDefinition.ContainerDefinitionProperty.HealthCheck``.
            :param hostname: ``CfnTaskDefinition.ContainerDefinitionProperty.Hostname``.
            :param image: ``CfnTaskDefinition.ContainerDefinitionProperty.Image``.
            :param interactive: ``CfnTaskDefinition.ContainerDefinitionProperty.Interactive``.
            :param links: ``CfnTaskDefinition.ContainerDefinitionProperty.Links``.
            :param linux_parameters: ``CfnTaskDefinition.ContainerDefinitionProperty.LinuxParameters``.
            :param log_configuration: ``CfnTaskDefinition.ContainerDefinitionProperty.LogConfiguration``.
            :param memory: ``CfnTaskDefinition.ContainerDefinitionProperty.Memory``.
            :param memory_reservation: ``CfnTaskDefinition.ContainerDefinitionProperty.MemoryReservation``.
            :param mount_points: ``CfnTaskDefinition.ContainerDefinitionProperty.MountPoints``.
            :param name: ``CfnTaskDefinition.ContainerDefinitionProperty.Name``.
            :param port_mappings: ``CfnTaskDefinition.ContainerDefinitionProperty.PortMappings``.
            :param privileged: ``CfnTaskDefinition.ContainerDefinitionProperty.Privileged``.
            :param pseudo_terminal: ``CfnTaskDefinition.ContainerDefinitionProperty.PseudoTerminal``.
            :param readonly_root_filesystem: ``CfnTaskDefinition.ContainerDefinitionProperty.ReadonlyRootFilesystem``.
            :param repository_credentials: ``CfnTaskDefinition.ContainerDefinitionProperty.RepositoryCredentials``.
            :param resource_requirements: ``CfnTaskDefinition.ContainerDefinitionProperty.ResourceRequirements``.
            :param secrets: ``CfnTaskDefinition.ContainerDefinitionProperty.Secrets``.
            :param start_timeout: ``CfnTaskDefinition.ContainerDefinitionProperty.StartTimeout``.
            :param stop_timeout: ``CfnTaskDefinition.ContainerDefinitionProperty.StopTimeout``.
            :param system_controls: ``CfnTaskDefinition.ContainerDefinitionProperty.SystemControls``.
            :param ulimits: ``CfnTaskDefinition.ContainerDefinitionProperty.Ulimits``.
            :param user: ``CfnTaskDefinition.ContainerDefinitionProperty.User``.
            :param volumes_from: ``CfnTaskDefinition.ContainerDefinitionProperty.VolumesFrom``.
            :param working_directory: ``CfnTaskDefinition.ContainerDefinitionProperty.WorkingDirectory``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html
            """
            self._values = {
            }
            if command is not None: self._values["command"] = command
            if cpu is not None: self._values["cpu"] = cpu
            if depends_on is not None: self._values["depends_on"] = depends_on
            if disable_networking is not None: self._values["disable_networking"] = disable_networking
            if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
            if dns_servers is not None: self._values["dns_servers"] = dns_servers
            if docker_labels is not None: self._values["docker_labels"] = docker_labels
            if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
            if entry_point is not None: self._values["entry_point"] = entry_point
            if environment is not None: self._values["environment"] = environment
            if essential is not None: self._values["essential"] = essential
            if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
            if health_check is not None: self._values["health_check"] = health_check
            if hostname is not None: self._values["hostname"] = hostname
            if image is not None: self._values["image"] = image
            if interactive is not None: self._values["interactive"] = interactive
            if links is not None: self._values["links"] = links
            if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
            if log_configuration is not None: self._values["log_configuration"] = log_configuration
            if memory is not None: self._values["memory"] = memory
            if memory_reservation is not None: self._values["memory_reservation"] = memory_reservation
            if mount_points is not None: self._values["mount_points"] = mount_points
            if name is not None: self._values["name"] = name
            if port_mappings is not None: self._values["port_mappings"] = port_mappings
            if privileged is not None: self._values["privileged"] = privileged
            if pseudo_terminal is not None: self._values["pseudo_terminal"] = pseudo_terminal
            if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
            if repository_credentials is not None: self._values["repository_credentials"] = repository_credentials
            if resource_requirements is not None: self._values["resource_requirements"] = resource_requirements
            if secrets is not None: self._values["secrets"] = secrets
            if start_timeout is not None: self._values["start_timeout"] = start_timeout
            if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
            if system_controls is not None: self._values["system_controls"] = system_controls
            if ulimits is not None: self._values["ulimits"] = ulimits
            if user is not None: self._values["user"] = user
            if volumes_from is not None: self._values["volumes_from"] = volumes_from
            if working_directory is not None: self._values["working_directory"] = working_directory

        @property
        def command(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Command``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-command
            """
            return self._values.get('command')

        @property
        def cpu(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Cpu``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-cpu
            """
            return self._values.get('cpu')

        @property
        def depends_on(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.ContainerDependencyProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DependsOn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dependson
            """
            return self._values.get('depends_on')

        @property
        def disable_networking(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DisableNetworking``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-disablenetworking
            """
            return self._values.get('disable_networking')

        @property
        def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DnsSearchDomains``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dnssearchdomains
            """
            return self._values.get('dns_search_domains')

        @property
        def dns_servers(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DnsServers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dnsservers
            """
            return self._values.get('dns_servers')

        @property
        def docker_labels(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DockerLabels``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dockerlabels
            """
            return self._values.get('docker_labels')

        @property
        def docker_security_options(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DockerSecurityOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dockersecurityoptions
            """
            return self._values.get('docker_security_options')

        @property
        def entry_point(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.EntryPoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-entrypoint
            """
            return self._values.get('entry_point')

        @property
        def environment(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.KeyValuePairProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Environment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-environment
            """
            return self._values.get('environment')

        @property
        def essential(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Essential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-essential
            """
            return self._values.get('essential')

        @property
        def extra_hosts(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.HostEntryProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.ExtraHosts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-extrahosts
            """
            return self._values.get('extra_hosts')

        @property
        def health_check(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.HealthCheckProperty"]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.HealthCheck``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-healthcheck
            """
            return self._values.get('health_check')

        @property
        def hostname(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Hostname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-hostname
            """
            return self._values.get('hostname')

        @property
        def image(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-image
            """
            return self._values.get('image')

        @property
        def interactive(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Interactive``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-interactive
            """
            return self._values.get('interactive')

        @property
        def links(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Links``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-links
            """
            return self._values.get('links')

        @property
        def linux_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.LinuxParametersProperty"]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.LinuxParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-linuxparameters
            """
            return self._values.get('linux_parameters')

        @property
        def log_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.LogConfigurationProperty"]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.LogConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration
            """
            return self._values.get('log_configuration')

        @property
        def memory(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Memory``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-memory
            """
            return self._values.get('memory')

        @property
        def memory_reservation(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.MemoryReservation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-memoryreservation
            """
            return self._values.get('memory_reservation')

        @property
        def mount_points(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.MountPointProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.MountPoints``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints
            """
            return self._values.get('mount_points')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-name
            """
            return self._values.get('name')

        @property
        def port_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.PortMappingProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.PortMappings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-portmappings
            """
            return self._values.get('port_mappings')

        @property
        def privileged(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Privileged``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-privileged
            """
            return self._values.get('privileged')

        @property
        def pseudo_terminal(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.PseudoTerminal``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-pseudoterminal
            """
            return self._values.get('pseudo_terminal')

        @property
        def readonly_root_filesystem(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.ReadonlyRootFilesystem``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-readonlyrootfilesystem
            """
            return self._values.get('readonly_root_filesystem')

        @property
        def repository_credentials(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.RepositoryCredentials``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-repositorycredentials
            """
            return self._values.get('repository_credentials')

        @property
        def resource_requirements(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.ResourceRequirementProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.ResourceRequirements``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-resourcerequirements
            """
            return self._values.get('resource_requirements')

        @property
        def secrets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.SecretProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Secrets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-secrets
            """
            return self._values.get('secrets')

        @property
        def start_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.StartTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-starttimeout
            """
            return self._values.get('start_timeout')

        @property
        def stop_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.StopTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-stoptimeout
            """
            return self._values.get('stop_timeout')

        @property
        def system_controls(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.SystemControlProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.SystemControls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-systemcontrols
            """
            return self._values.get('system_controls')

        @property
        def ulimits(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.UlimitProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Ulimits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-ulimits
            """
            return self._values.get('ulimits')

        @property
        def user(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.User``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-user
            """
            return self._values.get('user')

        @property
        def volumes_from(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.VolumeFromProperty"]]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.VolumesFrom``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom
            """
            return self._values.get('volumes_from')

        @property
        def working_directory(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.WorkingDirectory``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-workingdirectory
            """
            return self._values.get('working_directory')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ContainerDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ContainerDependencyProperty", jsii_struct_bases=[], name_mapping={'condition': 'condition', 'container_name': 'containerName'})
    class ContainerDependencyProperty():
        def __init__(self, *, condition: str, container_name: str):
            """
            :param condition: ``CfnTaskDefinition.ContainerDependencyProperty.Condition``.
            :param container_name: ``CfnTaskDefinition.ContainerDependencyProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html
            """
            self._values = {
                'condition': condition,
                'container_name': container_name,
            }

        @property
        def condition(self) -> str:
            """``CfnTaskDefinition.ContainerDependencyProperty.Condition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html#cfn-ecs-taskdefinition-containerdependency-condition
            """
            return self._values.get('condition')

        @property
        def container_name(self) -> str:
            """``CfnTaskDefinition.ContainerDependencyProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html#cfn-ecs-taskdefinition-containerdependency-containername
            """
            return self._values.get('container_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ContainerDependencyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.DeviceProperty", jsii_struct_bases=[], name_mapping={'host_path': 'hostPath', 'container_path': 'containerPath', 'permissions': 'permissions'})
    class DeviceProperty():
        def __init__(self, *, host_path: str, container_path: typing.Optional[str]=None, permissions: typing.Optional[typing.List[str]]=None):
            """
            :param host_path: ``CfnTaskDefinition.DeviceProperty.HostPath``.
            :param container_path: ``CfnTaskDefinition.DeviceProperty.ContainerPath``.
            :param permissions: ``CfnTaskDefinition.DeviceProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html
            """
            self._values = {
                'host_path': host_path,
            }
            if container_path is not None: self._values["container_path"] = container_path
            if permissions is not None: self._values["permissions"] = permissions

        @property
        def host_path(self) -> str:
            """``CfnTaskDefinition.DeviceProperty.HostPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-hostpath
            """
            return self._values.get('host_path')

        @property
        def container_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.DeviceProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-containerpath
            """
            return self._values.get('container_path')

        @property
        def permissions(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.DeviceProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-permissions
            """
            return self._values.get('permissions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeviceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.DockerVolumeConfigurationProperty", jsii_struct_bases=[], name_mapping={'autoprovision': 'autoprovision', 'driver': 'driver', 'driver_opts': 'driverOpts', 'labels': 'labels', 'scope': 'scope'})
    class DockerVolumeConfigurationProperty():
        def __init__(self, *, autoprovision: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, driver: typing.Optional[str]=None, driver_opts: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, labels: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, scope: typing.Optional[str]=None):
            """
            :param autoprovision: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Autoprovision``.
            :param driver: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Driver``.
            :param driver_opts: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.DriverOpts``.
            :param labels: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Labels``.
            :param scope: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html
            """
            self._values = {
            }
            if autoprovision is not None: self._values["autoprovision"] = autoprovision
            if driver is not None: self._values["driver"] = driver
            if driver_opts is not None: self._values["driver_opts"] = driver_opts
            if labels is not None: self._values["labels"] = labels
            if scope is not None: self._values["scope"] = scope

        @property
        def autoprovision(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Autoprovision``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-autoprovision
            """
            return self._values.get('autoprovision')

        @property
        def driver(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Driver``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-driver
            """
            return self._values.get('driver')

        @property
        def driver_opts(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.DriverOpts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-driveropts
            """
            return self._values.get('driver_opts')

        @property
        def labels(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Labels``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-labels
            """
            return self._values.get('labels')

        @property
        def scope(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-scope
            """
            return self._values.get('scope')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DockerVolumeConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HealthCheckProperty", jsii_struct_bases=[], name_mapping={'command': 'command', 'interval': 'interval', 'retries': 'retries', 'start_period': 'startPeriod', 'timeout': 'timeout'})
    class HealthCheckProperty():
        def __init__(self, *, command: typing.List[str], interval: typing.Optional[jsii.Number]=None, retries: typing.Optional[jsii.Number]=None, start_period: typing.Optional[jsii.Number]=None, timeout: typing.Optional[jsii.Number]=None):
            """
            :param command: ``CfnTaskDefinition.HealthCheckProperty.Command``.
            :param interval: ``CfnTaskDefinition.HealthCheckProperty.Interval``.
            :param retries: ``CfnTaskDefinition.HealthCheckProperty.Retries``.
            :param start_period: ``CfnTaskDefinition.HealthCheckProperty.StartPeriod``.
            :param timeout: ``CfnTaskDefinition.HealthCheckProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html
            """
            self._values = {
                'command': command,
            }
            if interval is not None: self._values["interval"] = interval
            if retries is not None: self._values["retries"] = retries
            if start_period is not None: self._values["start_period"] = start_period
            if timeout is not None: self._values["timeout"] = timeout

        @property
        def command(self) -> typing.List[str]:
            """``CfnTaskDefinition.HealthCheckProperty.Command``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-command
            """
            return self._values.get('command')

        @property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.Interval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-interval
            """
            return self._values.get('interval')

        @property
        def retries(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.Retries``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-retries
            """
            return self._values.get('retries')

        @property
        def start_period(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.StartPeriod``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-startperiod
            """
            return self._values.get('start_period')

        @property
        def timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-timeout
            """
            return self._values.get('timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HostEntryProperty", jsii_struct_bases=[], name_mapping={'hostname': 'hostname', 'ip_address': 'ipAddress'})
    class HostEntryProperty():
        def __init__(self, *, hostname: str, ip_address: str):
            """
            :param hostname: ``CfnTaskDefinition.HostEntryProperty.Hostname``.
            :param ip_address: ``CfnTaskDefinition.HostEntryProperty.IpAddress``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html
            """
            self._values = {
                'hostname': hostname,
                'ip_address': ip_address,
            }

        @property
        def hostname(self) -> str:
            """``CfnTaskDefinition.HostEntryProperty.Hostname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html#cfn-ecs-taskdefinition-containerdefinition-hostentry-hostname
            """
            return self._values.get('hostname')

        @property
        def ip_address(self) -> str:
            """``CfnTaskDefinition.HostEntryProperty.IpAddress``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html#cfn-ecs-taskdefinition-containerdefinition-hostentry-ipaddress
            """
            return self._values.get('ip_address')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HostEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HostVolumePropertiesProperty", jsii_struct_bases=[], name_mapping={'source_path': 'sourcePath'})
    class HostVolumePropertiesProperty():
        def __init__(self, *, source_path: typing.Optional[str]=None):
            """
            :param source_path: ``CfnTaskDefinition.HostVolumePropertiesProperty.SourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes-host.html
            """
            self._values = {
            }
            if source_path is not None: self._values["source_path"] = source_path

        @property
        def source_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.HostVolumePropertiesProperty.SourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes-host.html#cfn-ecs-taskdefinition-volumes-host-sourcepath
            """
            return self._values.get('source_path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HostVolumePropertiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.InferenceAcceleratorProperty", jsii_struct_bases=[], name_mapping={'device_name': 'deviceName', 'device_type': 'deviceType'})
    class InferenceAcceleratorProperty():
        def __init__(self, *, device_name: typing.Optional[str]=None, device_type: typing.Optional[str]=None):
            """
            :param device_name: ``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceName``.
            :param device_type: ``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-inferenceaccelerator.html
            """
            self._values = {
            }
            if device_name is not None: self._values["device_name"] = device_name
            if device_type is not None: self._values["device_type"] = device_type

        @property
        def device_name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-inferenceaccelerator.html#cfn-ecs-taskdefinition-inferenceaccelerator-devicename
            """
            return self._values.get('device_name')

        @property
        def device_type(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-inferenceaccelerator.html#cfn-ecs-taskdefinition-inferenceaccelerator-devicetype
            """
            return self._values.get('device_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InferenceAcceleratorProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.KernelCapabilitiesProperty", jsii_struct_bases=[], name_mapping={'add': 'add', 'drop': 'drop'})
    class KernelCapabilitiesProperty():
        def __init__(self, *, add: typing.Optional[typing.List[str]]=None, drop: typing.Optional[typing.List[str]]=None):
            """
            :param add: ``CfnTaskDefinition.KernelCapabilitiesProperty.Add``.
            :param drop: ``CfnTaskDefinition.KernelCapabilitiesProperty.Drop``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html
            """
            self._values = {
            }
            if add is not None: self._values["add"] = add
            if drop is not None: self._values["drop"] = drop

        @property
        def add(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.KernelCapabilitiesProperty.Add``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html#cfn-ecs-taskdefinition-kernelcapabilities-add
            """
            return self._values.get('add')

        @property
        def drop(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.KernelCapabilitiesProperty.Drop``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html#cfn-ecs-taskdefinition-kernelcapabilities-drop
            """
            return self._values.get('drop')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'KernelCapabilitiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.KeyValuePairProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class KeyValuePairProperty():
        def __init__(self, *, name: typing.Optional[str]=None, value: typing.Optional[str]=None):
            """
            :param name: ``CfnTaskDefinition.KeyValuePairProperty.Name``.
            :param value: ``CfnTaskDefinition.KeyValuePairProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if value is not None: self._values["value"] = value

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.KeyValuePairProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html#cfn-ecs-taskdefinition-containerdefinition-environment-name
            """
            return self._values.get('name')

        @property
        def value(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.KeyValuePairProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html#cfn-ecs-taskdefinition-containerdefinition-environment-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'KeyValuePairProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.LinuxParametersProperty", jsii_struct_bases=[], name_mapping={'capabilities': 'capabilities', 'devices': 'devices', 'init_process_enabled': 'initProcessEnabled', 'shared_memory_size': 'sharedMemorySize', 'tmpfs': 'tmpfs'})
    class LinuxParametersProperty():
        def __init__(self, *, capabilities: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.KernelCapabilitiesProperty"]]]=None, devices: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.DeviceProperty"]]]]]=None, init_process_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, shared_memory_size: typing.Optional[jsii.Number]=None, tmpfs: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.TmpfsProperty"]]]]]=None):
            """
            :param capabilities: ``CfnTaskDefinition.LinuxParametersProperty.Capabilities``.
            :param devices: ``CfnTaskDefinition.LinuxParametersProperty.Devices``.
            :param init_process_enabled: ``CfnTaskDefinition.LinuxParametersProperty.InitProcessEnabled``.
            :param shared_memory_size: ``CfnTaskDefinition.LinuxParametersProperty.SharedMemorySize``.
            :param tmpfs: ``CfnTaskDefinition.LinuxParametersProperty.Tmpfs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html
            """
            self._values = {
            }
            if capabilities is not None: self._values["capabilities"] = capabilities
            if devices is not None: self._values["devices"] = devices
            if init_process_enabled is not None: self._values["init_process_enabled"] = init_process_enabled
            if shared_memory_size is not None: self._values["shared_memory_size"] = shared_memory_size
            if tmpfs is not None: self._values["tmpfs"] = tmpfs

        @property
        def capabilities(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.KernelCapabilitiesProperty"]]]:
            """``CfnTaskDefinition.LinuxParametersProperty.Capabilities``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-capabilities
            """
            return self._values.get('capabilities')

        @property
        def devices(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.DeviceProperty"]]]]]:
            """``CfnTaskDefinition.LinuxParametersProperty.Devices``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-devices
            """
            return self._values.get('devices')

        @property
        def init_process_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.LinuxParametersProperty.InitProcessEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-initprocessenabled
            """
            return self._values.get('init_process_enabled')

        @property
        def shared_memory_size(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.LinuxParametersProperty.SharedMemorySize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-sharedmemorysize
            """
            return self._values.get('shared_memory_size')

        @property
        def tmpfs(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.TmpfsProperty"]]]]]:
            """``CfnTaskDefinition.LinuxParametersProperty.Tmpfs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-tmpfs
            """
            return self._values.get('tmpfs')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LinuxParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.LogConfigurationProperty", jsii_struct_bases=[], name_mapping={'log_driver': 'logDriver', 'options': 'options', 'secret_options': 'secretOptions'})
    class LogConfigurationProperty():
        def __init__(self, *, log_driver: str, options: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, secret_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.SecretProperty"]]]]]=None):
            """
            :param log_driver: ``CfnTaskDefinition.LogConfigurationProperty.LogDriver``.
            :param options: ``CfnTaskDefinition.LogConfigurationProperty.Options``.
            :param secret_options: ``CfnTaskDefinition.LogConfigurationProperty.SecretOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html
            """
            self._values = {
                'log_driver': log_driver,
            }
            if options is not None: self._values["options"] = options
            if secret_options is not None: self._values["secret_options"] = secret_options

        @property
        def log_driver(self) -> str:
            """``CfnTaskDefinition.LogConfigurationProperty.LogDriver``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration-logdriver
            """
            return self._values.get('log_driver')

        @property
        def options(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
            """``CfnTaskDefinition.LogConfigurationProperty.Options``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration-options
            """
            return self._values.get('options')

        @property
        def secret_options(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.SecretProperty"]]]]]:
            """``CfnTaskDefinition.LogConfigurationProperty.SecretOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-logconfiguration-secretoptions
            """
            return self._values.get('secret_options')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LogConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.MountPointProperty", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'read_only': 'readOnly', 'source_volume': 'sourceVolume'})
    class MountPointProperty():
        def __init__(self, *, container_path: typing.Optional[str]=None, read_only: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, source_volume: typing.Optional[str]=None):
            """
            :param container_path: ``CfnTaskDefinition.MountPointProperty.ContainerPath``.
            :param read_only: ``CfnTaskDefinition.MountPointProperty.ReadOnly``.
            :param source_volume: ``CfnTaskDefinition.MountPointProperty.SourceVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html
            """
            self._values = {
            }
            if container_path is not None: self._values["container_path"] = container_path
            if read_only is not None: self._values["read_only"] = read_only
            if source_volume is not None: self._values["source_volume"] = source_volume

        @property
        def container_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.MountPointProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-containerpath
            """
            return self._values.get('container_path')

        @property
        def read_only(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.MountPointProperty.ReadOnly``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-readonly
            """
            return self._values.get('read_only')

        @property
        def source_volume(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.MountPointProperty.SourceVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-sourcevolume
            """
            return self._values.get('source_volume')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MountPointProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.PortMappingProperty", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'host_port': 'hostPort', 'protocol': 'protocol'})
    class PortMappingProperty():
        def __init__(self, *, container_port: typing.Optional[jsii.Number]=None, host_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[str]=None):
            """
            :param container_port: ``CfnTaskDefinition.PortMappingProperty.ContainerPort``.
            :param host_port: ``CfnTaskDefinition.PortMappingProperty.HostPort``.
            :param protocol: ``CfnTaskDefinition.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html
            """
            self._values = {
            }
            if container_port is not None: self._values["container_port"] = container_port
            if host_port is not None: self._values["host_port"] = host_port
            if protocol is not None: self._values["protocol"] = protocol

        @property
        def container_port(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.PortMappingProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-containerport
            """
            return self._values.get('container_port')

        @property
        def host_port(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.PortMappingProperty.HostPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-readonly
            """
            return self._values.get('host_port')

        @property
        def protocol(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-sourcevolume
            """
            return self._values.get('protocol')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PortMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ProxyConfigurationProperty", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'proxy_configuration_properties': 'proxyConfigurationProperties', 'type': 'type'})
    class ProxyConfigurationProperty():
        def __init__(self, *, container_name: str, proxy_configuration_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.KeyValuePairProperty"]]]]]=None, type: typing.Optional[str]=None):
            """
            :param container_name: ``CfnTaskDefinition.ProxyConfigurationProperty.ContainerName``.
            :param proxy_configuration_properties: ``CfnTaskDefinition.ProxyConfigurationProperty.ProxyConfigurationProperties``.
            :param type: ``CfnTaskDefinition.ProxyConfigurationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html
            """
            self._values = {
                'container_name': container_name,
            }
            if proxy_configuration_properties is not None: self._values["proxy_configuration_properties"] = proxy_configuration_properties
            if type is not None: self._values["type"] = type

        @property
        def container_name(self) -> str:
            """``CfnTaskDefinition.ProxyConfigurationProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-containername
            """
            return self._values.get('container_name')

        @property
        def proxy_configuration_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.KeyValuePairProperty"]]]]]:
            """``CfnTaskDefinition.ProxyConfigurationProperty.ProxyConfigurationProperties``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-proxyconfigurationproperties
            """
            return self._values.get('proxy_configuration_properties')

        @property
        def type(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ProxyConfigurationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProxyConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.RepositoryCredentialsProperty", jsii_struct_bases=[], name_mapping={'credentials_parameter': 'credentialsParameter'})
    class RepositoryCredentialsProperty():
        def __init__(self, *, credentials_parameter: typing.Optional[str]=None):
            """
            :param credentials_parameter: ``CfnTaskDefinition.RepositoryCredentialsProperty.CredentialsParameter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-repositorycredentials.html
            """
            self._values = {
            }
            if credentials_parameter is not None: self._values["credentials_parameter"] = credentials_parameter

        @property
        def credentials_parameter(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.RepositoryCredentialsProperty.CredentialsParameter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-repositorycredentials.html#cfn-ecs-taskdefinition-repositorycredentials-credentialsparameter
            """
            return self._values.get('credentials_parameter')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RepositoryCredentialsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ResourceRequirementProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'value': 'value'})
    class ResourceRequirementProperty():
        def __init__(self, *, type: str, value: str):
            """
            :param type: ``CfnTaskDefinition.ResourceRequirementProperty.Type``.
            :param value: ``CfnTaskDefinition.ResourceRequirementProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html
            """
            self._values = {
                'type': type,
                'value': value,
            }

        @property
        def type(self) -> str:
            """``CfnTaskDefinition.ResourceRequirementProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html#cfn-ecs-taskdefinition-resourcerequirement-type
            """
            return self._values.get('type')

        @property
        def value(self) -> str:
            """``CfnTaskDefinition.ResourceRequirementProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html#cfn-ecs-taskdefinition-resourcerequirement-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourceRequirementProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.SecretProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value_from': 'valueFrom'})
    class SecretProperty():
        def __init__(self, *, name: str, value_from: str):
            """
            :param name: ``CfnTaskDefinition.SecretProperty.Name``.
            :param value_from: ``CfnTaskDefinition.SecretProperty.ValueFrom``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html
            """
            self._values = {
                'name': name,
                'value_from': value_from,
            }

        @property
        def name(self) -> str:
            """``CfnTaskDefinition.SecretProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html#cfn-ecs-taskdefinition-secret-name
            """
            return self._values.get('name')

        @property
        def value_from(self) -> str:
            """``CfnTaskDefinition.SecretProperty.ValueFrom``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html#cfn-ecs-taskdefinition-secret-valuefrom
            """
            return self._values.get('value_from')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SecretProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.SystemControlProperty", jsii_struct_bases=[], name_mapping={'namespace': 'namespace', 'value': 'value'})
    class SystemControlProperty():
        def __init__(self, *, namespace: str, value: str):
            """
            :param namespace: ``CfnTaskDefinition.SystemControlProperty.Namespace``.
            :param value: ``CfnTaskDefinition.SystemControlProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-systemcontrol.html
            """
            self._values = {
                'namespace': namespace,
                'value': value,
            }

        @property
        def namespace(self) -> str:
            """``CfnTaskDefinition.SystemControlProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-systemcontrol.html#cfn-ecs-taskdefinition-systemcontrol-namespace
            """
            return self._values.get('namespace')

        @property
        def value(self) -> str:
            """``CfnTaskDefinition.SystemControlProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-systemcontrol.html#cfn-ecs-taskdefinition-systemcontrol-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SystemControlProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'expression': 'expression'})
    class TaskDefinitionPlacementConstraintProperty():
        def __init__(self, *, type: str, expression: typing.Optional[str]=None):
            """
            :param type: ``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Type``.
            :param expression: ``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html
            """
            self._values = {
                'type': type,
            }
            if expression is not None: self._values["expression"] = expression

        @property
        def type(self) -> str:
            """``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html#cfn-ecs-taskdefinition-taskdefinitionplacementconstraint-type
            """
            return self._values.get('type')

        @property
        def expression(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html#cfn-ecs-taskdefinition-taskdefinitionplacementconstraint-expression
            """
            return self._values.get('expression')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TaskDefinitionPlacementConstraintProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.TmpfsProperty", jsii_struct_bases=[], name_mapping={'size': 'size', 'container_path': 'containerPath', 'mount_options': 'mountOptions'})
    class TmpfsProperty():
        def __init__(self, *, size: jsii.Number, container_path: typing.Optional[str]=None, mount_options: typing.Optional[typing.List[str]]=None):
            """
            :param size: ``CfnTaskDefinition.TmpfsProperty.Size``.
            :param container_path: ``CfnTaskDefinition.TmpfsProperty.ContainerPath``.
            :param mount_options: ``CfnTaskDefinition.TmpfsProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html
            """
            self._values = {
                'size': size,
            }
            if container_path is not None: self._values["container_path"] = container_path
            if mount_options is not None: self._values["mount_options"] = mount_options

        @property
        def size(self) -> jsii.Number:
            """``CfnTaskDefinition.TmpfsProperty.Size``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-size
            """
            return self._values.get('size')

        @property
        def container_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.TmpfsProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-containerpath
            """
            return self._values.get('container_path')

        @property
        def mount_options(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.TmpfsProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-mountoptions
            """
            return self._values.get('mount_options')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TmpfsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.UlimitProperty", jsii_struct_bases=[], name_mapping={'hard_limit': 'hardLimit', 'name': 'name', 'soft_limit': 'softLimit'})
    class UlimitProperty():
        def __init__(self, *, hard_limit: jsii.Number, name: str, soft_limit: jsii.Number):
            """
            :param hard_limit: ``CfnTaskDefinition.UlimitProperty.HardLimit``.
            :param name: ``CfnTaskDefinition.UlimitProperty.Name``.
            :param soft_limit: ``CfnTaskDefinition.UlimitProperty.SoftLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html
            """
            self._values = {
                'hard_limit': hard_limit,
                'name': name,
                'soft_limit': soft_limit,
            }

        @property
        def hard_limit(self) -> jsii.Number:
            """``CfnTaskDefinition.UlimitProperty.HardLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-hardlimit
            """
            return self._values.get('hard_limit')

        @property
        def name(self) -> str:
            """``CfnTaskDefinition.UlimitProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-name
            """
            return self._values.get('name')

        @property
        def soft_limit(self) -> jsii.Number:
            """``CfnTaskDefinition.UlimitProperty.SoftLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-softlimit
            """
            return self._values.get('soft_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'UlimitProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.VolumeFromProperty", jsii_struct_bases=[], name_mapping={'read_only': 'readOnly', 'source_container': 'sourceContainer'})
    class VolumeFromProperty():
        def __init__(self, *, read_only: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, source_container: typing.Optional[str]=None):
            """
            :param read_only: ``CfnTaskDefinition.VolumeFromProperty.ReadOnly``.
            :param source_container: ``CfnTaskDefinition.VolumeFromProperty.SourceContainer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html
            """
            self._values = {
            }
            if read_only is not None: self._values["read_only"] = read_only
            if source_container is not None: self._values["source_container"] = source_container

        @property
        def read_only(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTaskDefinition.VolumeFromProperty.ReadOnly``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom-readonly
            """
            return self._values.get('read_only')

        @property
        def source_container(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.VolumeFromProperty.SourceContainer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom-sourcecontainer
            """
            return self._values.get('source_container')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VolumeFromProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.VolumeProperty", jsii_struct_bases=[], name_mapping={'docker_volume_configuration': 'dockerVolumeConfiguration', 'host': 'host', 'name': 'name'})
    class VolumeProperty():
        def __init__(self, *, docker_volume_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.DockerVolumeConfigurationProperty"]]]=None, host: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.HostVolumePropertiesProperty"]]]=None, name: typing.Optional[str]=None):
            """
            :param docker_volume_configuration: ``CfnTaskDefinition.VolumeProperty.DockerVolumeConfiguration``.
            :param host: ``CfnTaskDefinition.VolumeProperty.Host``.
            :param name: ``CfnTaskDefinition.VolumeProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html
            """
            self._values = {
            }
            if docker_volume_configuration is not None: self._values["docker_volume_configuration"] = docker_volume_configuration
            if host is not None: self._values["host"] = host
            if name is not None: self._values["name"] = name

        @property
        def docker_volume_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.DockerVolumeConfigurationProperty"]]]:
            """``CfnTaskDefinition.VolumeProperty.DockerVolumeConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volume-dockervolumeconfiguration
            """
            return self._values.get('docker_volume_configuration')

        @property
        def host(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.HostVolumePropertiesProperty"]]]:
            """``CfnTaskDefinition.VolumeProperty.Host``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volumes-host
            """
            return self._values.get('host')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.VolumeProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volumes-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VolumeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinitionProps", jsii_struct_bases=[], name_mapping={'container_definitions': 'containerDefinitions', 'cpu': 'cpu', 'execution_role_arn': 'executionRoleArn', 'family': 'family', 'inference_accelerators': 'inferenceAccelerators', 'ipc_mode': 'ipcMode', 'memory': 'memory', 'network_mode': 'networkMode', 'pid_mode': 'pidMode', 'placement_constraints': 'placementConstraints', 'proxy_configuration': 'proxyConfiguration', 'requires_compatibilities': 'requiresCompatibilities', 'tags': 'tags', 'task_role_arn': 'taskRoleArn', 'volumes': 'volumes'})
class CfnTaskDefinitionProps():
    def __init__(self, *, container_definitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnTaskDefinition.ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]=None, cpu: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, family: typing.Optional[str]=None, inference_accelerators: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.InferenceAcceleratorProperty"]]]]]=None, ipc_mode: typing.Optional[str]=None, memory: typing.Optional[str]=None, network_mode: typing.Optional[str]=None, pid_mode: typing.Optional[str]=None, placement_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty"]]]]]=None, proxy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.ProxyConfigurationProperty"]]]=None, requires_compatibilities: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, task_role_arn: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.VolumeProperty"]]]]]=None):
        """Properties for defining a ``AWS::ECS::TaskDefinition``.

        :param container_definitions: ``AWS::ECS::TaskDefinition.ContainerDefinitions``.
        :param cpu: ``AWS::ECS::TaskDefinition.Cpu``.
        :param execution_role_arn: ``AWS::ECS::TaskDefinition.ExecutionRoleArn``.
        :param family: ``AWS::ECS::TaskDefinition.Family``.
        :param inference_accelerators: ``AWS::ECS::TaskDefinition.InferenceAccelerators``.
        :param ipc_mode: ``AWS::ECS::TaskDefinition.IpcMode``.
        :param memory: ``AWS::ECS::TaskDefinition.Memory``.
        :param network_mode: ``AWS::ECS::TaskDefinition.NetworkMode``.
        :param pid_mode: ``AWS::ECS::TaskDefinition.PidMode``.
        :param placement_constraints: ``AWS::ECS::TaskDefinition.PlacementConstraints``.
        :param proxy_configuration: ``AWS::ECS::TaskDefinition.ProxyConfiguration``.
        :param requires_compatibilities: ``AWS::ECS::TaskDefinition.RequiresCompatibilities``.
        :param tags: ``AWS::ECS::TaskDefinition.Tags``.
        :param task_role_arn: ``AWS::ECS::TaskDefinition.TaskRoleArn``.
        :param volumes: ``AWS::ECS::TaskDefinition.Volumes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html
        """
        self._values = {
        }
        if container_definitions is not None: self._values["container_definitions"] = container_definitions
        if cpu is not None: self._values["cpu"] = cpu
        if execution_role_arn is not None: self._values["execution_role_arn"] = execution_role_arn
        if family is not None: self._values["family"] = family
        if inference_accelerators is not None: self._values["inference_accelerators"] = inference_accelerators
        if ipc_mode is not None: self._values["ipc_mode"] = ipc_mode
        if memory is not None: self._values["memory"] = memory
        if network_mode is not None: self._values["network_mode"] = network_mode
        if pid_mode is not None: self._values["pid_mode"] = pid_mode
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if requires_compatibilities is not None: self._values["requires_compatibilities"] = requires_compatibilities
        if tags is not None: self._values["tags"] = tags
        if task_role_arn is not None: self._values["task_role_arn"] = task_role_arn
        if volumes is not None: self._values["volumes"] = volumes

    @property
    def container_definitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnTaskDefinition.ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ECS::TaskDefinition.ContainerDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-containerdefinitions
        """
        return self._values.get('container_definitions')

    @property
    def cpu(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Cpu``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-cpu
        """
        return self._values.get('cpu')

    @property
    def execution_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-executionrolearn
        """
        return self._values.get('execution_role_arn')

    @property
    def family(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-family
        """
        return self._values.get('family')

    @property
    def inference_accelerators(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.InferenceAcceleratorProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.InferenceAccelerators``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-inferenceaccelerators
        """
        return self._values.get('inference_accelerators')

    @property
    def ipc_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.IpcMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-ipcmode
        """
        return self._values.get('ipc_mode')

    @property
    def memory(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Memory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-memory
        """
        return self._values.get('memory')

    @property
    def network_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.NetworkMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-networkmode
        """
        return self._values.get('network_mode')

    @property
    def pid_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.PidMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-pidmode
        """
        return self._values.get('pid_mode')

    @property
    def placement_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-placementconstraints
        """
        return self._values.get('placement_constraints')

    @property
    def proxy_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTaskDefinition.ProxyConfigurationProperty"]]]:
        """``AWS::ECS::TaskDefinition.ProxyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-proxyconfiguration
        """
        return self._values.get('proxy_configuration')

    @property
    def requires_compatibilities(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ECS::TaskDefinition.RequiresCompatibilities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-requirescompatibilities
        """
        return self._values.get('requires_compatibilities')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ECS::TaskDefinition.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-tags
        """
        return self._values.get('tags')

    @property
    def task_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.TaskRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-taskrolearn
        """
        return self._values.get('task_role_arn')

    @property
    def volumes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.VolumeProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.Volumes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-volumes
        """
        return self._values.get('volumes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CloudMapNamespaceOptions", jsii_struct_bases=[], name_mapping={'name': 'name', 'type': 'type', 'vpc': 'vpc'})
class CloudMapNamespaceOptions():
    def __init__(self, *, name: str, type: typing.Optional[aws_cdk.aws_servicediscovery.NamespaceType]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The options for creating an AWS Cloud Map namespace.

        :param name: The name of the namespace, such as example.com.
        :param type: The type of CloudMap Namespace to create. Default: PrivateDns
        :param vpc: The VPC to associate the namespace with. This property is required for private DNS namespaces. Default: VPC of the cluster for Private DNS Namespace, otherwise none
        """
        self._values = {
            'name': name,
        }
        if type is not None: self._values["type"] = type
        if vpc is not None: self._values["vpc"] = vpc

    @property
    def name(self) -> str:
        """The name of the namespace, such as example.com."""
        return self._values.get('name')

    @property
    def type(self) -> typing.Optional[aws_cdk.aws_servicediscovery.NamespaceType]:
        """The type of CloudMap Namespace to create.

        default
        :default: PrivateDns
        """
        return self._values.get('type')

    @property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC to associate the namespace with.

        This property is required for private DNS namespaces.

        default
        :default: VPC of the cluster for Private DNS Namespace, otherwise none
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudMapNamespaceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CloudMapOptions", jsii_struct_bases=[], name_mapping={'cloud_map_namespace': 'cloudMapNamespace', 'dns_record_type': 'dnsRecordType', 'dns_ttl': 'dnsTtl', 'failure_threshold': 'failureThreshold', 'name': 'name'})
class CloudMapOptions():
    def __init__(self, *, cloud_map_namespace: typing.Optional[aws_cdk.aws_servicediscovery.INamespace]=None, dns_record_type: typing.Optional[aws_cdk.aws_servicediscovery.DnsRecordType]=None, dns_ttl: typing.Optional[aws_cdk.core.Duration]=None, failure_threshold: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None):
        """The options to enabling AWS Cloud Map for an Amazon ECS service.

        :param cloud_map_namespace: The service discovery namespace for the Cloud Map service to attach to the ECS service. Default: - the defaultCloudMapNamespace associated to the cluster
        :param dns_record_type: The DNS record type that you want AWS Cloud Map to create. The supported record types are A or SRV. Default: DnsRecordType.A
        :param dns_ttl: The amount of time that you want DNS resolvers to cache the settings for this record. Default: 60
        :param failure_threshold: The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance. NOTE: This is used for HealthCheckCustomConfig
        :param name: The name of the Cloud Map service to attach to the ECS service. Default: CloudFormation-generated name
        """
        self._values = {
        }
        if cloud_map_namespace is not None: self._values["cloud_map_namespace"] = cloud_map_namespace
        if dns_record_type is not None: self._values["dns_record_type"] = dns_record_type
        if dns_ttl is not None: self._values["dns_ttl"] = dns_ttl
        if failure_threshold is not None: self._values["failure_threshold"] = failure_threshold
        if name is not None: self._values["name"] = name

    @property
    def cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """The service discovery namespace for the Cloud Map service to attach to the ECS service.

        default
        :default: - the defaultCloudMapNamespace associated to the cluster
        """
        return self._values.get('cloud_map_namespace')

    @property
    def dns_record_type(self) -> typing.Optional[aws_cdk.aws_servicediscovery.DnsRecordType]:
        """The DNS record type that you want AWS Cloud Map to create.

        The supported record types are A or SRV.

        default
        :default: DnsRecordType.A
        """
        return self._values.get('dns_record_type')

    @property
    def dns_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time that you want DNS resolvers to cache the settings for this record.

        default
        :default: 60
        """
        return self._values.get('dns_ttl')

    @property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        """The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance.

        NOTE: This is used for HealthCheckCustomConfig
        """
        return self._values.get('failure_threshold')

    @property
    def name(self) -> typing.Optional[str]:
        """The name of the Cloud Map service to attach to the ECS service.

        default
        :default: CloudFormation-generated name
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudMapOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ClusterAttributes", jsii_struct_bases=[], name_mapping={'cluster_name': 'clusterName', 'security_groups': 'securityGroups', 'vpc': 'vpc', 'autoscaling_group': 'autoscalingGroup', 'cluster_arn': 'clusterArn', 'default_cloud_map_namespace': 'defaultCloudMapNamespace', 'has_ec2_capacity': 'hasEc2Capacity'})
class ClusterAttributes():
    def __init__(self, *, cluster_name: str, security_groups: typing.List[aws_cdk.aws_ec2.ISecurityGroup], vpc: aws_cdk.aws_ec2.IVpc, autoscaling_group: typing.Optional[aws_cdk.aws_autoscaling.IAutoScalingGroup]=None, cluster_arn: typing.Optional[str]=None, default_cloud_map_namespace: typing.Optional[aws_cdk.aws_servicediscovery.INamespace]=None, has_ec2_capacity: typing.Optional[bool]=None):
        """The properties to import from the ECS cluster.

        :param cluster_name: The name of the cluster.
        :param security_groups: The security groups associated with the container instances registered to the cluster.
        :param vpc: The VPC associated with the cluster.
        :param autoscaling_group: Autoscaling group added to the cluster if capacity is added. Default: - No default autoscaling group
        :param cluster_arn: The Amazon Resource Name (ARN) that identifies the cluster. Default: Derived from clusterName
        :param default_cloud_map_namespace: The AWS Cloud Map namespace to associate with the cluster. Default: - No default namespace
        :param has_ec2_capacity: Specifies whether the cluster has EC2 instance capacity. Default: true
        """
        self._values = {
            'cluster_name': cluster_name,
            'security_groups': security_groups,
            'vpc': vpc,
        }
        if autoscaling_group is not None: self._values["autoscaling_group"] = autoscaling_group
        if cluster_arn is not None: self._values["cluster_arn"] = cluster_arn
        if default_cloud_map_namespace is not None: self._values["default_cloud_map_namespace"] = default_cloud_map_namespace
        if has_ec2_capacity is not None: self._values["has_ec2_capacity"] = has_ec2_capacity

    @property
    def cluster_name(self) -> str:
        """The name of the cluster."""
        return self._values.get('cluster_name')

    @property
    def security_groups(self) -> typing.List[aws_cdk.aws_ec2.ISecurityGroup]:
        """The security groups associated with the container instances registered to the cluster."""
        return self._values.get('security_groups')

    @property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC associated with the cluster."""
        return self._values.get('vpc')

    @property
    def autoscaling_group(self) -> typing.Optional[aws_cdk.aws_autoscaling.IAutoScalingGroup]:
        """Autoscaling group added to the cluster if capacity is added.

        default
        :default: - No default autoscaling group
        """
        return self._values.get('autoscaling_group')

    @property
    def cluster_arn(self) -> typing.Optional[str]:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        default
        :default: Derived from clusterName
        """
        return self._values.get('cluster_arn')

    @property
    def default_cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """The AWS Cloud Map namespace to associate with the cluster.

        default
        :default: - No default namespace
        """
        return self._values.get('default_cloud_map_namespace')

    @property
    def has_ec2_capacity(self) -> typing.Optional[bool]:
        """Specifies whether the cluster has EC2 instance capacity.

        default
        :default: true
        """
        return self._values.get('has_ec2_capacity')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ClusterProps", jsii_struct_bases=[], name_mapping={'capacity': 'capacity', 'cluster_name': 'clusterName', 'default_cloud_map_namespace': 'defaultCloudMapNamespace', 'vpc': 'vpc'})
class ClusterProps():
    def __init__(self, *, capacity: typing.Optional["AddCapacityOptions"]=None, cluster_name: typing.Optional[str]=None, default_cloud_map_namespace: typing.Optional["CloudMapNamespaceOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The properties used to define an ECS cluster.

        :param capacity: The ec2 capacity to add to the cluster. Default: - no EC2 capacity will be added, you can use ``addCapacity`` to add capacity later.
        :param cluster_name: The name for the cluster. Default: CloudFormation-generated name
        :param default_cloud_map_namespace: The service discovery namespace created in this cluster. Default: - no service discovery namespace created, you can use ``addDefaultCloudMapNamespace`` to add a default service discovery namespace later.
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs
        """
        if isinstance(capacity, dict): capacity = AddCapacityOptions(**capacity)
        if isinstance(default_cloud_map_namespace, dict): default_cloud_map_namespace = CloudMapNamespaceOptions(**default_cloud_map_namespace)
        self._values = {
        }
        if capacity is not None: self._values["capacity"] = capacity
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if default_cloud_map_namespace is not None: self._values["default_cloud_map_namespace"] = default_cloud_map_namespace
        if vpc is not None: self._values["vpc"] = vpc

    @property
    def capacity(self) -> typing.Optional["AddCapacityOptions"]:
        """The ec2 capacity to add to the cluster.

        default
        :default: - no EC2 capacity will be added, you can use ``addCapacity`` to add capacity later.
        """
        return self._values.get('capacity')

    @property
    def cluster_name(self) -> typing.Optional[str]:
        """The name for the cluster.

        default
        :default: CloudFormation-generated name
        """
        return self._values.get('cluster_name')

    @property
    def default_cloud_map_namespace(self) -> typing.Optional["CloudMapNamespaceOptions"]:
        """The service discovery namespace created in this cluster.

        default
        :default:

        - no service discovery namespace created, you can use ``addDefaultCloudMapNamespace`` to add a
          default service discovery namespace later.
        """
        return self._values.get('default_cloud_map_namespace')

    @property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where your ECS instances will be running or your ENIs will be deployed.

        default
        :default: - creates a new VPC with two AZs
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CommonTaskDefinitionProps", jsii_struct_bases=[], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes'})
class CommonTaskDefinitionProps():
    def __init__(self, *, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None):
        """The common properties for all task definitions.

        For more information, see
        `Task Definition Parameters <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html>`_.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        """
        self._values = {
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes

    @property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.
        """
        return self._values.get('execution_role')

    @property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.
        """
        return self._values.get('proxy_configuration')

    @property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    @property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.
        """
        return self._values.get('volumes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonTaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Compatibility")
class Compatibility(enum.Enum):
    """The task launch type compatibility requirement."""
    EC2 = "EC2"
    """The task should specify the EC2 launch type."""
    FARGATE = "FARGATE"
    """The task should specify the Fargate launch type."""
    EC2_AND_FARGATE = "EC2_AND_FARGATE"
    """The task can specify either the EC2 or Fargate launch types."""

class ContainerDefinition(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.ContainerDefinition"):
    """A container definition is used in a task definition to describe the containers that are launched as part of a task."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: "TaskDefinition", image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str,"Secret"]]=None, start_timeout: typing.Optional[aws_cdk.core.Duration]=None, stop_timeout: typing.Optional[aws_cdk.core.Duration]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the ContainerDefinition class.

        :param scope: -
        :param id: -
        :param props: -
        :param task_definition: The name of the task definition that includes this container definition. [disable-awslint:ref-via-interface]
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux paramters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /
        """
        props = ContainerDefinitionProps(task_definition=task_definition, image=image, command=command, cpu=cpu, disable_networking=disable_networking, dns_search_domains=dns_search_domains, dns_servers=dns_servers, docker_labels=docker_labels, docker_security_options=docker_security_options, entry_point=entry_point, environment=environment, essential=essential, extra_hosts=extra_hosts, gpu_count=gpu_count, health_check=health_check, hostname=hostname, linux_parameters=linux_parameters, logging=logging, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, privileged=privileged, readonly_root_filesystem=readonly_root_filesystem, secrets=secrets, start_timeout=start_timeout, stop_timeout=stop_timeout, user=user, working_directory=working_directory)

        jsii.create(ContainerDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="addContainerDependencies")
    def add_container_dependencies(self, *container_dependencies: "ContainerDependency") -> None:
        """This method adds one or more container dependencies to the container.

        :param container_dependencies: -
        """
        return jsii.invoke(self, "addContainerDependencies", [*container_dependencies])

    @jsii.member(jsii_name="addLink")
    def add_link(self, container: "ContainerDefinition", alias: typing.Optional[str]=None) -> None:
        """This method adds a link which allows containers to communicate with each other without the need for port mappings.

        This parameter is only supported if the task definition is using the bridge network mode.
        Warning: The --link flag is a legacy feature of Docker. It may eventually be removed.

        :param container: -
        :param alias: -
        """
        return jsii.invoke(self, "addLink", [container, alias])

    @jsii.member(jsii_name="addMountPoints")
    def add_mount_points(self, *mount_points: "MountPoint") -> None:
        """This method adds one or more mount points for data volumes to the container.

        :param mount_points: -
        """
        return jsii.invoke(self, "addMountPoints", [*mount_points])

    @jsii.member(jsii_name="addPortMappings")
    def add_port_mappings(self, *port_mappings: "PortMapping") -> None:
        """This method adds one or more port mappings to the container.

        :param port_mappings: -
        """
        return jsii.invoke(self, "addPortMappings", [*port_mappings])

    @jsii.member(jsii_name="addScratch")
    def add_scratch(self, *, container_path: str, name: str, read_only: bool, source_path: str) -> None:
        """This method mounts temporary disk space to the container.

        This adds the correct container mountPoint and task definition volume.

        :param scratch: -
        :param container_path: The path on the container to mount the scratch volume at.
        :param name: The name of the scratch volume to mount. Must be a volume name referenced in the name parameter of task definition volume.
        :param read_only: Specifies whether to give the container read-only access to the scratch volume. If this value is true, the container has read-only access to the scratch volume. If this value is false, then the container can write to the scratch volume.
        :param source_path: 
        """
        scratch = ScratchSpace(container_path=container_path, name=name, read_only=read_only, source_path=source_path)

        return jsii.invoke(self, "addScratch", [scratch])

    @jsii.member(jsii_name="addToExecutionPolicy")
    def add_to_execution_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """This method adds the specified statement to the IAM task execution policy in the task definition.

        :param statement: -
        """
        return jsii.invoke(self, "addToExecutionPolicy", [statement])

    @jsii.member(jsii_name="addUlimits")
    def add_ulimits(self, *ulimits: "Ulimit") -> None:
        """This method adds one or more ulimits to the container.

        :param ulimits: -
        """
        return jsii.invoke(self, "addUlimits", [*ulimits])

    @jsii.member(jsii_name="addVolumesFrom")
    def add_volumes_from(self, *volumes_from: "VolumeFrom") -> None:
        """This method adds one or more volumes to the container.

        :param volumes_from: -
        """
        return jsii.invoke(self, "addVolumesFrom", [*volumes_from])

    @jsii.member(jsii_name="renderContainerDefinition")
    def render_container_definition(self, task_definition: typing.Optional["TaskDefinition"]=None) -> "CfnTaskDefinition.ContainerDefinitionProperty":
        """Render this container definition to a CloudFormation object.

        :param task_definition: [disable-awslint:ref-via-interface] (made optional to avoid breaking change).
        """
        return jsii.invoke(self, "renderContainerDefinition", [task_definition])

    @property
    @jsii.member(jsii_name="containerDependencies")
    def container_dependencies(self) -> typing.List["ContainerDependency"]:
        """An array dependencies defined for container startup and shutdown."""
        return jsii.get(self, "containerDependencies")

    @property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> str:
        """The name of this container."""
        return jsii.get(self, "containerName")

    @property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        """The port the container will listen on."""
        return jsii.get(self, "containerPort")

    @property
    @jsii.member(jsii_name="essential")
    def essential(self) -> bool:
        """Specifies whether the container will be marked essential.

        If the essential parameter of a container is marked as true, and that container
        fails or stops for any reason, all other containers that are part of the task are
        stopped. If the essential parameter of a container is marked as false, then its
        failure does not affect the rest of the containers in a task.

        If this parameter isomitted, a container is assumed to be essential.
        """
        return jsii.get(self, "essential")

    @property
    @jsii.member(jsii_name="ingressPort")
    def ingress_port(self) -> jsii.Number:
        """The inbound rules associated with the security group the task or service will use.

        This property is only used for tasks that use the awsvpc network mode.
        """
        return jsii.get(self, "ingressPort")

    @property
    @jsii.member(jsii_name="memoryLimitSpecified")
    def memory_limit_specified(self) -> bool:
        """Whether there was at least one memory limit specified in this definition."""
        return jsii.get(self, "memoryLimitSpecified")

    @property
    @jsii.member(jsii_name="mountPoints")
    def mount_points(self) -> typing.List["MountPoint"]:
        """The mount points for data volumes in your container."""
        return jsii.get(self, "mountPoints")

    @property
    @jsii.member(jsii_name="portMappings")
    def port_mappings(self) -> typing.List["PortMapping"]:
        """The list of port mappings for the container.

        Port mappings allow containers to access ports
        on the host container instance to send or receive traffic.
        """
        return jsii.get(self, "portMappings")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        """The name of the task definition that includes this container definition."""
        return jsii.get(self, "taskDefinition")

    @property
    @jsii.member(jsii_name="ulimits")
    def ulimits(self) -> typing.List["Ulimit"]:
        """An array of ulimits to set in the container."""
        return jsii.get(self, "ulimits")

    @property
    @jsii.member(jsii_name="volumesFrom")
    def volumes_from(self) -> typing.List["VolumeFrom"]:
        """The data volumes to mount from another container in the same task definition."""
        return jsii.get(self, "volumesFrom")

    @property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """The Linux-specific modifications that are applied to the container, such as Linux kernel capabilities."""
        return jsii.get(self, "linuxParameters")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerDefinitionOptions", jsii_struct_bases=[], name_mapping={'image': 'image', 'command': 'command', 'cpu': 'cpu', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'gpu_count': 'gpuCount', 'health_check': 'healthCheck', 'hostname': 'hostname', 'linux_parameters': 'linuxParameters', 'logging': 'logging', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'privileged': 'privileged', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'user': 'user', 'working_directory': 'workingDirectory'})
class ContainerDefinitionOptions():
    def __init__(self, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str,"Secret"]]=None, start_timeout: typing.Optional[aws_cdk.core.Duration]=None, stop_timeout: typing.Optional[aws_cdk.core.Duration]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None):
        """
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux paramters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if disable_networking is not None: self._values["disable_networking"] = disable_networking
        if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
        if dns_servers is not None: self._values["dns_servers"] = dns_servers
        if docker_labels is not None: self._values["docker_labels"] = docker_labels
        if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
        if entry_point is not None: self._values["entry_point"] = entry_point
        if environment is not None: self._values["environment"] = environment
        if essential is not None: self._values["essential"] = essential
        if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if health_check is not None: self._values["health_check"] = health_check
        if hostname is not None: self._values["hostname"] = hostname
        if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
        if logging is not None: self._values["logging"] = logging
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if privileged is not None: self._values["privileged"] = privileged
        if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None: self._values["secrets"] = secrets
        if start_timeout is not None: self._values["start_timeout"] = start_timeout
        if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
        if user is not None: self._values["user"] = user
        if working_directory is not None: self._values["working_directory"] = working_directory

    @property
    def image(self) -> "ContainerImage":
        """The image used to start a container.

        This string is passed directly to the Docker daemon.
        Images in the Docker Hub registry are available by default.
        Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.
        TODO: Update these to specify using classes of IContainerImage
        """
        return self._values.get('image')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: - No minimum CPU units reserved.
        """
        return self._values.get('cpu')

    @property
    def disable_networking(self) -> typing.Optional[bool]:
        """Specifies whether networking is disabled within the container.

        When this parameter is true, networking is disabled within the container.

        default
        :default: false
        """
        return self._values.get('disable_networking')

    @property
    def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS search domains that are presented to the container.

        default
        :default: - No search domains.
        """
        return self._values.get('dns_search_domains')

    @property
    def dns_servers(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS servers that are presented to the container.

        default
        :default: - Default DNS servers.
        """
        return self._values.get('dns_servers')

    @property
    def docker_labels(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A key/value map of labels to add to the container.

        default
        :default: - No labels.
        """
        return self._values.get('docker_labels')

    @property
    def docker_security_options(self) -> typing.Optional[typing.List[str]]:
        """A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems.

        default
        :default: - No security labels.
        """
        return self._values.get('docker_security_options')

    @property
    def entry_point(self) -> typing.Optional[typing.List[str]]:
        """The ENTRYPOINT value to pass to the container.

        default
        :default: - Entry point configured in container.

        see
        :see: https://docs.docker.com/engine/reference/builder/#entrypoint
        """
        return self._values.get('entry_point')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @property
    def essential(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked essential.

        If the essential parameter of a container is marked as true, and that container fails
        or stops for any reason, all other containers that are part of the task are stopped.
        If the essential parameter of a container is marked as false, then its failure does not
        affect the rest of the containers in a task. All tasks must have at least one essential container.

        If this parameter is omitted, a container is assumed to be essential.

        default
        :default: true
        """
        return self._values.get('essential')

    @property
    def extra_hosts(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A list of hostnames and IP address mappings to append to the /etc/hosts file on the container.

        default
        :default: - No extra hosts.
        """
        return self._values.get('extra_hosts')

    @property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of GPUs assigned to the container.

        default
        :default: - No GPUs assigned.
        """
        return self._values.get('gpu_count')

    @property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """The health check command and associated configuration parameters for the container.

        default
        :default: - Health check configuration from container.
        """
        return self._values.get('health_check')

    @property
    def hostname(self) -> typing.Optional[str]:
        """The hostname to use for your container.

        default
        :default: - Automatic hostname.
        """
        return self._values.get('hostname')

    @property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_.

        default
        :default: - No Linux paramters.
        """
        return self._values.get('linux_parameters')

    @property
    def logging(self) -> typing.Optional["LogDriver"]:
        """The log configuration specification for the container.

        default
        :default: - Containers use the same logging driver that the Docker daemon uses.
        """
        return self._values.get('logging')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    @property
    def privileged(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        default
        :default: false
        """
        return self._values.get('privileged')

    @property
    def readonly_root_filesystem(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given read-only access to its root file system.

        default
        :default: false
        """
        return self._values.get('readonly_root_filesystem')

    @property
    def secrets(self) -> typing.Optional[typing.Mapping[str,"Secret"]]:
        """The secret environment variables to pass to the container.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @property
    def start_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Time duration (in seconds) to wait before giving up on resolving dependencies for a container.

        default
        :default: - none
        """
        return self._values.get('start_timeout')

    @property
    def stop_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own.

        default
        :default: - none
        """
        return self._values.get('stop_timeout')

    @property
    def user(self) -> typing.Optional[str]:
        """The user name to use inside the container.

        default
        :default: root
        """
        return self._values.get('user')

    @property
    def working_directory(self) -> typing.Optional[str]:
        """The working directory in which to run commands inside the container.

        default
        :default: /
        """
        return self._values.get('working_directory')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerDefinitionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerDefinitionProps", jsii_struct_bases=[ContainerDefinitionOptions], name_mapping={'image': 'image', 'command': 'command', 'cpu': 'cpu', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'gpu_count': 'gpuCount', 'health_check': 'healthCheck', 'hostname': 'hostname', 'linux_parameters': 'linuxParameters', 'logging': 'logging', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'privileged': 'privileged', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'user': 'user', 'working_directory': 'workingDirectory', 'task_definition': 'taskDefinition'})
class ContainerDefinitionProps(ContainerDefinitionOptions):
    def __init__(self, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str,"Secret"]]=None, start_timeout: typing.Optional[aws_cdk.core.Duration]=None, stop_timeout: typing.Optional[aws_cdk.core.Duration]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None, task_definition: "TaskDefinition"):
        """The properties in a container definition.

        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux paramters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /
        :param task_definition: The name of the task definition that includes this container definition. [disable-awslint:ref-via-interface]
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
            'image': image,
            'task_definition': task_definition,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if disable_networking is not None: self._values["disable_networking"] = disable_networking
        if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
        if dns_servers is not None: self._values["dns_servers"] = dns_servers
        if docker_labels is not None: self._values["docker_labels"] = docker_labels
        if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
        if entry_point is not None: self._values["entry_point"] = entry_point
        if environment is not None: self._values["environment"] = environment
        if essential is not None: self._values["essential"] = essential
        if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if health_check is not None: self._values["health_check"] = health_check
        if hostname is not None: self._values["hostname"] = hostname
        if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
        if logging is not None: self._values["logging"] = logging
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if privileged is not None: self._values["privileged"] = privileged
        if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None: self._values["secrets"] = secrets
        if start_timeout is not None: self._values["start_timeout"] = start_timeout
        if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
        if user is not None: self._values["user"] = user
        if working_directory is not None: self._values["working_directory"] = working_directory

    @property
    def image(self) -> "ContainerImage":
        """The image used to start a container.

        This string is passed directly to the Docker daemon.
        Images in the Docker Hub registry are available by default.
        Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.
        TODO: Update these to specify using classes of IContainerImage
        """
        return self._values.get('image')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: - No minimum CPU units reserved.
        """
        return self._values.get('cpu')

    @property
    def disable_networking(self) -> typing.Optional[bool]:
        """Specifies whether networking is disabled within the container.

        When this parameter is true, networking is disabled within the container.

        default
        :default: false
        """
        return self._values.get('disable_networking')

    @property
    def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS search domains that are presented to the container.

        default
        :default: - No search domains.
        """
        return self._values.get('dns_search_domains')

    @property
    def dns_servers(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS servers that are presented to the container.

        default
        :default: - Default DNS servers.
        """
        return self._values.get('dns_servers')

    @property
    def docker_labels(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A key/value map of labels to add to the container.

        default
        :default: - No labels.
        """
        return self._values.get('docker_labels')

    @property
    def docker_security_options(self) -> typing.Optional[typing.List[str]]:
        """A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems.

        default
        :default: - No security labels.
        """
        return self._values.get('docker_security_options')

    @property
    def entry_point(self) -> typing.Optional[typing.List[str]]:
        """The ENTRYPOINT value to pass to the container.

        default
        :default: - Entry point configured in container.

        see
        :see: https://docs.docker.com/engine/reference/builder/#entrypoint
        """
        return self._values.get('entry_point')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @property
    def essential(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked essential.

        If the essential parameter of a container is marked as true, and that container fails
        or stops for any reason, all other containers that are part of the task are stopped.
        If the essential parameter of a container is marked as false, then its failure does not
        affect the rest of the containers in a task. All tasks must have at least one essential container.

        If this parameter is omitted, a container is assumed to be essential.

        default
        :default: true
        """
        return self._values.get('essential')

    @property
    def extra_hosts(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A list of hostnames and IP address mappings to append to the /etc/hosts file on the container.

        default
        :default: - No extra hosts.
        """
        return self._values.get('extra_hosts')

    @property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of GPUs assigned to the container.

        default
        :default: - No GPUs assigned.
        """
        return self._values.get('gpu_count')

    @property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """The health check command and associated configuration parameters for the container.

        default
        :default: - Health check configuration from container.
        """
        return self._values.get('health_check')

    @property
    def hostname(self) -> typing.Optional[str]:
        """The hostname to use for your container.

        default
        :default: - Automatic hostname.
        """
        return self._values.get('hostname')

    @property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_.

        default
        :default: - No Linux paramters.
        """
        return self._values.get('linux_parameters')

    @property
    def logging(self) -> typing.Optional["LogDriver"]:
        """The log configuration specification for the container.

        default
        :default: - Containers use the same logging driver that the Docker daemon uses.
        """
        return self._values.get('logging')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    @property
    def privileged(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        default
        :default: false
        """
        return self._values.get('privileged')

    @property
    def readonly_root_filesystem(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given read-only access to its root file system.

        default
        :default: false
        """
        return self._values.get('readonly_root_filesystem')

    @property
    def secrets(self) -> typing.Optional[typing.Mapping[str,"Secret"]]:
        """The secret environment variables to pass to the container.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @property
    def start_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Time duration (in seconds) to wait before giving up on resolving dependencies for a container.

        default
        :default: - none
        """
        return self._values.get('start_timeout')

    @property
    def stop_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own.

        default
        :default: - none
        """
        return self._values.get('stop_timeout')

    @property
    def user(self) -> typing.Optional[str]:
        """The user name to use inside the container.

        default
        :default: root
        """
        return self._values.get('user')

    @property
    def working_directory(self) -> typing.Optional[str]:
        """The working directory in which to run commands inside the container.

        default
        :default: /
        """
        return self._values.get('working_directory')

    @property
    def task_definition(self) -> "TaskDefinition":
        """The name of the task definition that includes this container definition.

        [disable-awslint:ref-via-interface]
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerDependency", jsii_struct_bases=[], name_mapping={'container': 'container', 'condition': 'condition'})
class ContainerDependency():
    def __init__(self, *, container: "ContainerDefinition", condition: typing.Optional["ContainerDependencyCondition"]=None):
        """The details of a dependency on another container in the task definition.

        :param container: The container to depend on.
        :param condition: The state the container needs to be in to satisfy the dependency and proceed with startup. Valid values are ContainerDependencyCondition.START, ContainerDependencyCondition.COMPLETE, ContainerDependencyCondition.SUCCESS and ContainerDependencyCondition.HEALTHY. Default: ContainerDependencyCondition.HEALTHY

        see
        :see: https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDependency.html
        """
        self._values = {
            'container': container,
        }
        if condition is not None: self._values["condition"] = condition

    @property
    def container(self) -> "ContainerDefinition":
        """The container to depend on."""
        return self._values.get('container')

    @property
    def condition(self) -> typing.Optional["ContainerDependencyCondition"]:
        """The state the container needs to be in to satisfy the dependency and proceed with startup. Valid values are ContainerDependencyCondition.START, ContainerDependencyCondition.COMPLETE, ContainerDependencyCondition.SUCCESS and ContainerDependencyCondition.HEALTHY.

        default
        :default: ContainerDependencyCondition.HEALTHY
        """
        return self._values.get('condition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerDependency(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.ContainerDependencyCondition")
class ContainerDependencyCondition(enum.Enum):
    START = "START"
    """This condition emulates the behavior of links and volumes today. It validates that a dependent container is started before permitting other containers to start."""
    COMPLETE = "COMPLETE"
    """This condition validates that a dependent container runs to completion (exits) before permitting other containers to start. This can be useful for nonessential containers that run a script and then exit."""
    SUCCESS = "SUCCESS"
    """This condition is the same as COMPLETE, but it also requires that the container exits with a zero status."""
    HEALTHY = "HEALTHY"
    """This condition validates that the dependent container passes its Docker health check before permitting other containers to start. This requires that the dependent container has health checks configured. This condition is confirmed only at task startup."""

class ContainerImage(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.ContainerImage"):
    """Constructs for types of container images."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ContainerImageProxy

    def __init__(self) -> None:
        jsii.create(ContainerImage, self, [])

    @jsii.member(jsii_name="fromAsset")
    @classmethod
    def from_asset(cls, directory: str, *, build_args: typing.Optional[typing.Mapping[str,str]]=None, target: typing.Optional[str]=None) -> "AssetImage":
        """Reference an image that's constructed directly from sources on disk.

        :param directory: The directory containing the Dockerfile.
        :param props: -
        :param build_args: The arguments to pass to the ``docker build`` command. Default: none
        :param target: Docker target to build to. Default: none
        """
        props = AssetImageProps(build_args=build_args, target=target)

        return jsii.sinvoke(cls, "fromAsset", [directory, props])

    @jsii.member(jsii_name="fromEcrRepository")
    @classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "EcrImage":
        """Reference an image in an ECR repository.

        :param repository: -
        :param tag: -
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="fromRegistry")
    @classmethod
    def from_registry(cls, name: str, *, credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> "RepositoryImage":
        """Reference an image on DockerHub or another online registry.

        :param name: -
        :param props: -
        :param credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.
        """
        props = RepositoryImageProps(credentials=credentials)

        return jsii.sinvoke(cls, "fromRegistry", [name, props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -
        """
        ...


class _ContainerImageProxy(ContainerImage):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


class AssetImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.AssetImage"):
    """An image that will be built from a local directory with a Dockerfile."""
    def __init__(self, directory: str, *, build_args: typing.Optional[typing.Mapping[str,str]]=None, target: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the AssetImage class.

        :param directory: The directory containing the Dockerfile.
        :param props: -
        :param build_args: The arguments to pass to the ``docker build`` command. Default: none
        :param target: Docker target to build to. Default: none
        """
        props = AssetImageProps(build_args=build_args, target=target)

        jsii.create(AssetImage, self, [directory, props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerImageConfig", jsii_struct_bases=[], name_mapping={'image_name': 'imageName', 'repository_credentials': 'repositoryCredentials'})
class ContainerImageConfig():
    def __init__(self, *, image_name: str, repository_credentials: typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]=None):
        """The configuration for creating a container image.

        :param image_name: Specifies the name of the container image.
        :param repository_credentials: Specifies the credentials used to access the image repository.
        """
        if isinstance(repository_credentials, dict): repository_credentials = CfnTaskDefinition.RepositoryCredentialsProperty(**repository_credentials)
        self._values = {
            'image_name': image_name,
        }
        if repository_credentials is not None: self._values["repository_credentials"] = repository_credentials

    @property
    def image_name(self) -> str:
        """Specifies the name of the container image."""
        return self._values.get('image_name')

    @property
    def repository_credentials(self) -> typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]:
        """Specifies the credentials used to access the image repository."""
        return self._values.get('repository_credentials')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerImageConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CpuUtilizationScalingProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'target_utilization_percent': 'targetUtilizationPercent'})
class CpuUtilizationScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None, target_utilization_percent: jsii.Number):
        """The properties for enabling scaling based on CPU utilization.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        :param target_utilization_percent: The target value for CPU utilization across all tasks in the service.
        """
        self._values = {
            'target_utilization_percent': target_utilization_percent,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('policy_name')

    @property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default: - No scale in cooldown.
        """
        return self._values.get('scale_in_cooldown')

    @property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default: - No scale out cooldown.
        """
        return self._values.get('scale_out_cooldown')

    @property
    def target_utilization_percent(self) -> jsii.Number:
        """The target value for CPU utilization across all tasks in the service."""
        return self._values.get('target_utilization_percent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CpuUtilizationScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Device", jsii_struct_bases=[], name_mapping={'host_path': 'hostPath', 'container_path': 'containerPath', 'permissions': 'permissions'})
class Device():
    def __init__(self, *, host_path: str, container_path: typing.Optional[str]=None, permissions: typing.Optional[typing.List["DevicePermission"]]=None):
        """A container instance host device.

        :param host_path: The path for the device on the host container instance.
        :param container_path: The path inside the container at which to expose the host device. Default: Same path as the host
        :param permissions: The explicit permissions to provide to the container for the device. By default, the container has permissions for read, write, and mknod for the device. Default: Readonly
        """
        self._values = {
            'host_path': host_path,
        }
        if container_path is not None: self._values["container_path"] = container_path
        if permissions is not None: self._values["permissions"] = permissions

    @property
    def host_path(self) -> str:
        """The path for the device on the host container instance."""
        return self._values.get('host_path')

    @property
    def container_path(self) -> typing.Optional[str]:
        """The path inside the container at which to expose the host device.

        default
        :default: Same path as the host
        """
        return self._values.get('container_path')

    @property
    def permissions(self) -> typing.Optional[typing.List["DevicePermission"]]:
        """The explicit permissions to provide to the container for the device. By default, the container has permissions for read, write, and mknod for the device.

        default
        :default: Readonly
        """
        return self._values.get('permissions')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Device(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.DevicePermission")
class DevicePermission(enum.Enum):
    """Permissions for device access."""
    READ = "READ"
    """Read."""
    WRITE = "WRITE"
    """Write."""
    MKNOD = "MKNOD"
    """Make a node."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.DockerVolumeConfiguration", jsii_struct_bases=[], name_mapping={'driver': 'driver', 'scope': 'scope', 'autoprovision': 'autoprovision', 'driver_opts': 'driverOpts', 'labels': 'labels'})
class DockerVolumeConfiguration():
    def __init__(self, *, driver: str, scope: "Scope", autoprovision: typing.Optional[bool]=None, driver_opts: typing.Optional[typing.Mapping[str,str]]=None, labels: typing.Optional[typing.List[str]]=None):
        """The configuration for a Docker volume.

        Docker volumes are only supported when you are using the EC2 launch type.

        :param driver: The Docker volume driver to use.
        :param scope: The scope for the Docker volume that determines its lifecycle.
        :param autoprovision: Specifies whether the Docker volume should be created if it does not already exist. If true is specified, the Docker volume will be created for you. Default: false
        :param driver_opts: A map of Docker driver-specific options passed through. Default: No options
        :param labels: Custom metadata to add to your Docker volume. Default: No labels
        """
        self._values = {
            'driver': driver,
            'scope': scope,
        }
        if autoprovision is not None: self._values["autoprovision"] = autoprovision
        if driver_opts is not None: self._values["driver_opts"] = driver_opts
        if labels is not None: self._values["labels"] = labels

    @property
    def driver(self) -> str:
        """The Docker volume driver to use."""
        return self._values.get('driver')

    @property
    def scope(self) -> "Scope":
        """The scope for the Docker volume that determines its lifecycle."""
        return self._values.get('scope')

    @property
    def autoprovision(self) -> typing.Optional[bool]:
        """Specifies whether the Docker volume should be created if it does not already exist. If true is specified, the Docker volume will be created for you.

        default
        :default: false
        """
        return self._values.get('autoprovision')

    @property
    def driver_opts(self) -> typing.Optional[typing.Mapping[str,str]]:
        """A map of Docker driver-specific options passed through.

        default
        :default: No options
        """
        return self._values.get('driver_opts')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """Custom metadata to add to your Docker volume.

        default
        :default: No labels
        """
        return self._values.get('labels')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerVolumeConfiguration(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ec2ServiceProps", jsii_struct_bases=[BaseServiceOptions], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'task_definition': 'taskDefinition', 'assign_public_ip': 'assignPublicIp', 'daemon': 'daemon', 'placement_constraints': 'placementConstraints', 'placement_strategies': 'placementStrategies', 'propagate_task_tags_from': 'propagateTaskTagsFrom', 'security_group': 'securityGroup', 'vpc_subnets': 'vpcSubnets'})
class Ec2ServiceProps(BaseServiceOptions):
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, daemon: typing.Optional[bool]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, placement_strategies: typing.Optional[typing.List["PlacementStrategy"]]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None):
        """The properties for defining a service using the EC2 launch type.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. This property is only used for tasks that use the awsvpc network mode. Default: - Use subnet default.
        :param daemon: Specifies whether the service will use the daemon scheduling strategy. If true, the service scheduler deploys exactly one task on each container instance in your cluster. When you are using this strategy, do not specify a desired number of tasks orany task placement strategies. Default: false
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. This property is only used for tasks that use the awsvpc network mode. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. This property is only used for tasks that use the awsvpc network mode. Default: - Private subnets.
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if daemon is not None: self._values["daemon"] = daemon
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None: self._values["placement_strategies"] = placement_strategies
        if propagate_task_tags_from is not None: self._values["propagate_task_tags_from"] = propagate_task_tags_from
        if security_group is not None: self._values["security_group"] = security_group
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service."""
        return self._values.get('cluster')

    @property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE
        """
        return self._values.get('propagate_tags')

    @property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @property
    def task_definition(self) -> "TaskDefinition":
        """The task definition to use for tasks in the service.

        [disable-awslint:ref-via-interface]
        """
        return self._values.get('task_definition')

    @property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address.

        This property is only used for tasks that use the awsvpc network mode.

        default
        :default: - Use subnet default.
        """
        return self._values.get('assign_public_ip')

    @property
    def daemon(self) -> typing.Optional[bool]:
        """Specifies whether the service will use the daemon scheduling strategy. If true, the service scheduler deploys exactly one task on each container instance in your cluster.

        When you are using this strategy, do not specify a desired number of tasks orany task placement strategies.

        default
        :default: false
        """
        return self._values.get('daemon')

    @property
    def placement_constraints(self) -> typing.Optional[typing.List["PlacementConstraint"]]:
        """The placement constraints to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        default
        :default: - No constraints.
        """
        return self._values.get('placement_constraints')

    @property
    def placement_strategies(self) -> typing.Optional[typing.List["PlacementStrategy"]]:
        """The placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        default
        :default: - No strategies.
        """
        return self._values.get('placement_strategies')

    @property
    def propagate_task_tags_from(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: PropagatedTagSource.NONE

        deprecated
        :deprecated: Use ``propagateTags`` instead.

        stability
        :stability: deprecated
        """
        return self._values.get('propagate_task_tags_from')

    @property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """The security groups to associate with the service.

        If you do not specify a security group, the default security group for the VPC is used.

        This property is only used for tasks that use the awsvpc network mode.

        default
        :default: - A new security group is created.
        """
        return self._values.get('security_group')

    @property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The subnets to associate with the service.

        This property is only used for tasks that use the awsvpc network mode.

        default
        :default: - Private subnets.
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ec2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ec2TaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes', 'network_mode': 'networkMode', 'placement_constraints': 'placementConstraints'})
class Ec2TaskDefinitionProps(CommonTaskDefinitionProps):
    def __init__(self, *, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None):
        """The properties for a task definition run on an EC2 cluster.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        :param network_mode: The Docker networking mode to use for the containers in the task. The valid values are none, bridge, awsvpc, and host. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param placement_constraints: An array of placement constraint objects to use for the task. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Default: - No placement constraints.
        """
        self._values = {
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes
        if network_mode is not None: self._values["network_mode"] = network_mode
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints

    @property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.
        """
        return self._values.get('execution_role')

    @property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.
        """
        return self._values.get('proxy_configuration')

    @property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    @property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.
        """
        return self._values.get('volumes')

    @property
    def network_mode(self) -> typing.Optional["NetworkMode"]:
        """The Docker networking mode to use for the containers in the task.

        The valid values are none, bridge, awsvpc, and host.

        default
        :default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        """
        return self._values.get('network_mode')

    @property
    def placement_constraints(self) -> typing.Optional[typing.List["PlacementConstraint"]]:
        """An array of placement constraint objects to use for the task.

        You can
        specify a maximum of 10 constraints per task (this limit includes
        constraints in the task definition and those specified at run time).

        default
        :default: - No placement constraints.
        """
        return self._values.get('placement_constraints')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ec2TaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcrImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.EcrImage"):
    """An image from an Amazon ECR repository."""
    def __init__(self, repository: aws_cdk.aws_ecr.IRepository, tag: str) -> None:
        """Constructs a new instance of the EcrImage class.

        :param repository: -
        :param tag: -
        """
        jsii.create(EcrImage, self, [repository, tag])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param _scope: -
        :param container_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, container_definition])

    @property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> str:
        """The image name. Images in Amazon ECR repositories can be specified by either using the full registry/repository:tag or registry/repository@digest.

        For example, 012345678910.dkr.ecr..amazonaws.com/:latest or
        012345678910.dkr.ecr..amazonaws.com/@sha256:94afd1f2e64d908bc90dbca0035a5b567EXAMPLE.
        """
        return jsii.get(self, "imageName")


@jsii.implements(aws_cdk.aws_ec2.IMachineImage)
class EcsOptimizedAmi(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.EcsOptimizedAmi"):
    """Construct a Linux or Windows machine image from the latest ECS Optimized AMI published in SSM.

    deprecated
    :deprecated: see {@link EcsOptimizedImage#amazonLinux}, {@link EcsOptimizedImage#amazonLinux} and {@link EcsOptimizedImage#windows}

    stability
    :stability: deprecated
    """
    def __init__(self, *, generation: typing.Optional[aws_cdk.aws_ec2.AmazonLinuxGeneration]=None, hardware_type: typing.Optional["AmiHardwareType"]=None, windows_version: typing.Optional["WindowsOptimizedVersion"]=None) -> None:
        """Constructs a new instance of the EcsOptimizedAmi class.

        :param props: -
        :param generation: The Amazon Linux generation to use. Default: AmazonLinuxGeneration.AmazonLinux2
        :param hardware_type: The ECS-optimized AMI variant to use. Default: AmiHardwareType.Standard
        :param windows_version: The Windows Server version to use. Default: none, uses Linux generation

        stability
        :stability: deprecated
        """
        props = EcsOptimizedAmiProps(generation=generation, hardware_type=hardware_type, windows_version=windows_version)

        jsii.create(EcsOptimizedAmi, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.core.Construct) -> aws_cdk.aws_ec2.MachineImageConfig:
        """Return the correct image.

        :param scope: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.EcsOptimizedAmiProps", jsii_struct_bases=[], name_mapping={'generation': 'generation', 'hardware_type': 'hardwareType', 'windows_version': 'windowsVersion'})
class EcsOptimizedAmiProps():
    def __init__(self, *, generation: typing.Optional[aws_cdk.aws_ec2.AmazonLinuxGeneration]=None, hardware_type: typing.Optional["AmiHardwareType"]=None, windows_version: typing.Optional["WindowsOptimizedVersion"]=None):
        """The properties that define which ECS-optimized AMI is used.

        :param generation: The Amazon Linux generation to use. Default: AmazonLinuxGeneration.AmazonLinux2
        :param hardware_type: The ECS-optimized AMI variant to use. Default: AmiHardwareType.Standard
        :param windows_version: The Windows Server version to use. Default: none, uses Linux generation

        deprecated
        :deprecated: see {@link EcsOptimizedImage}

        stability
        :stability: deprecated
        """
        self._values = {
        }
        if generation is not None: self._values["generation"] = generation
        if hardware_type is not None: self._values["hardware_type"] = hardware_type
        if windows_version is not None: self._values["windows_version"] = windows_version

    @property
    def generation(self) -> typing.Optional[aws_cdk.aws_ec2.AmazonLinuxGeneration]:
        """The Amazon Linux generation to use.

        default
        :default: AmazonLinuxGeneration.AmazonLinux2

        stability
        :stability: deprecated
        """
        return self._values.get('generation')

    @property
    def hardware_type(self) -> typing.Optional["AmiHardwareType"]:
        """The ECS-optimized AMI variant to use.

        default
        :default: AmiHardwareType.Standard

        stability
        :stability: deprecated
        """
        return self._values.get('hardware_type')

    @property
    def windows_version(self) -> typing.Optional["WindowsOptimizedVersion"]:
        """The Windows Server version to use.

        default
        :default: none, uses Linux generation

        stability
        :stability: deprecated
        """
        return self._values.get('windows_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsOptimizedAmiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_ec2.IMachineImage)
class EcsOptimizedImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.EcsOptimizedImage"):
    """Construct a Linux or Windows machine image from the latest ECS Optimized AMI published in SSM."""
    @jsii.member(jsii_name="amazonLinux")
    @classmethod
    def amazon_linux(cls) -> "EcsOptimizedImage":
        """Construct an Amazon Linux AMI image from the latest ECS Optimized AMI published in SSM."""
        return jsii.sinvoke(cls, "amazonLinux", [])

    @jsii.member(jsii_name="amazonLinux2")
    @classmethod
    def amazon_linux2(cls, hardware_type: typing.Optional["AmiHardwareType"]=None) -> "EcsOptimizedImage":
        """Construct an Amazon Linux 2 image from the latest ECS Optimized AMI published in SSM.

        :param hardware_type: ECS-optimized AMI variant to use.
        """
        return jsii.sinvoke(cls, "amazonLinux2", [hardware_type])

    @jsii.member(jsii_name="windows")
    @classmethod
    def windows(cls, windows_version: "WindowsOptimizedVersion") -> "EcsOptimizedImage":
        """Construct a Windows image from the latest ECS Optimized AMI published in SSM.

        :param windows_version: Windows Version to use.
        """
        return jsii.sinvoke(cls, "windows", [windows_version])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.core.Construct) -> aws_cdk.aws_ec2.MachineImageConfig:
        """Return the correct image.

        :param scope: -
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.EcsTarget", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'listener': 'listener', 'new_target_group_id': 'newTargetGroupId', 'container_port': 'containerPort', 'protocol': 'protocol'})
class EcsTarget():
    def __init__(self, *, container_name: str, listener: "ListenerConfig", new_target_group_id: str, container_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None):
        """
        :param container_name: The name of the container.
        :param listener: Listener and properties for adding target group to the listener.
        :param new_target_group_id: ID for a target group to be created.
        :param container_port: The port number of the container. Only applicable when using application/network load balancers. Default: - Container port of the first added port mapping.
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: Protocol.TCP
        """
        self._values = {
            'container_name': container_name,
            'listener': listener,
            'new_target_group_id': new_target_group_id,
        }
        if container_port is not None: self._values["container_port"] = container_port
        if protocol is not None: self._values["protocol"] = protocol

    @property
    def container_name(self) -> str:
        """The name of the container."""
        return self._values.get('container_name')

    @property
    def listener(self) -> "ListenerConfig":
        """Listener and properties for adding target group to the listener."""
        return self._values.get('listener')

    @property
    def new_target_group_id(self) -> str:
        """ID for a target group to be created."""
        return self._values.get('new_target_group_id')

    @property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number of the container.

        Only applicable when using application/network load balancers.

        default
        :default: - Container port of the first added port mapping.
        """
        return self._values.get('container_port')

    @property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol used for the port mapping.

        Only applicable when using application load balancers.

        default
        :default: Protocol.TCP
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsTarget(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.FargatePlatformVersion")
class FargatePlatformVersion(enum.Enum):
    """The platform version on which to run your service.

    see
    :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html
    """
    LATEST = "LATEST"
    """The latest, recommended platform version."""
    VERSION1_3 = "VERSION1_3"
    """Version 1.3.0.

    Supports secrets, task recycling.
    """
    VERSION1_2 = "VERSION1_2"
    """Version 1.2.0.

    Supports private registries.
    """
    VERSION1_1 = "VERSION1_1"
    """Version 1.1.0.

    Supports task metadata, health checks, service discovery.
    """
    VERSION1_0 = "VERSION1_0"
    """Initial release.

    Based on Amazon Linux 2017.09.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.FargateServiceProps", jsii_struct_bases=[BaseServiceOptions], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'task_definition': 'taskDefinition', 'assign_public_ip': 'assignPublicIp', 'platform_version': 'platformVersion', 'propagate_task_tags_from': 'propagateTaskTagsFrom', 'security_group': 'securityGroup', 'vpc_subnets': 'vpcSubnets'})
class FargateServiceProps(BaseServiceOptions):
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional["FargatePlatformVersion"]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None):
        """The properties for defining a service using the Fargate launch type.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: - Use subnet default.
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. Default: - Private subnets.
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if platform_version is not None: self._values["platform_version"] = platform_version
        if propagate_task_tags_from is not None: self._values["propagate_task_tags_from"] = propagate_task_tags_from
        if security_group is not None: self._values["security_group"] = security_group
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service."""
        return self._values.get('cluster')

    @property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE
        """
        return self._values.get('propagate_tags')

    @property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @property
    def task_definition(self) -> "TaskDefinition":
        """The task definition to use for tasks in the service.

        [disable-awslint:ref-via-interface]
        """
        return self._values.get('task_definition')

    @property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Specifies whether the task's elastic network interface receives a public IP address.

        If true, each task will receive a public IP address.

        default
        :default: - Use subnet default.
        """
        return self._values.get('assign_public_ip')

    @property
    def platform_version(self) -> typing.Optional["FargatePlatformVersion"]:
        """The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        default
        :default: Latest
        """
        return self._values.get('platform_version')

    @property
    def propagate_task_tags_from(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: PropagatedTagSource.NONE

        deprecated
        :deprecated: Use ``propagateTags`` instead.

        stability
        :stability: deprecated
        """
        return self._values.get('propagate_task_tags_from')

    @property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """The security groups to associate with the service.

        If you do not specify a security group, the default security group for the VPC is used.

        default
        :default: - A new security group is created.
        """
        return self._values.get('security_group')

    @property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The subnets to associate with the service.

        default
        :default: - Private subnets.
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.FargateTaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB'})
class FargateTaskDefinitionProps(CommonTaskDefinitionProps):
    def __init__(self, *, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None):
        """The properties for a task definition.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 512
        """
        self._values = {
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib

    @property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.
        """
        return self._values.get('execution_role')

    @property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.
        """
        return self._values.get('proxy_configuration')

    @property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    @property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.
        """
        return self._values.get('volumes')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)
        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)
        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)
        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)
        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        default
        :default: 256
        """
        return self._values.get('cpu')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)
        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)
        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)
        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)
        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        default
        :default: 512
        """
        return self._values.get('memory_limit_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateTaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.FluentdLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'address': 'address', 'async_connect': 'asyncConnect', 'buffer_limit': 'bufferLimit', 'max_retries': 'maxRetries', 'retry_wait': 'retryWait', 'sub_second_precision': 'subSecondPrecision'})
class FluentdLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, address: typing.Optional[str]=None, async_connect: typing.Optional[bool]=None, buffer_limit: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, retry_wait: typing.Optional[aws_cdk.core.Duration]=None, sub_second_precision: typing.Optional[bool]=None):
        """Specifies the fluentd log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/fluentd/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param address: By default, the logging driver connects to localhost:24224. Supply the address option to connect to a different address. tcp(default) and unix sockets are supported. Default: - address not set.
        :param async_connect: Docker connects to Fluentd in the background. Messages are buffered until the connection is established. Default: - false
        :param buffer_limit: The amount of data to buffer before flushing to disk. Default: - The amount of RAM available to the container.
        :param max_retries: The maximum number of retries. Default: - 4294967295 (2**32 - 1).
        :param retry_wait: How long to wait between retries. Default: - 1 second
        :param sub_second_precision: Generates event logs in nanosecond resolution. Default: - false
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if address is not None: self._values["address"] = address
        if async_connect is not None: self._values["async_connect"] = async_connect
        if buffer_limit is not None: self._values["buffer_limit"] = buffer_limit
        if max_retries is not None: self._values["max_retries"] = max_retries
        if retry_wait is not None: self._values["retry_wait"] = retry_wait
        if sub_second_precision is not None: self._values["sub_second_precision"] = sub_second_precision

    @property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env
        """
        return self._values.get('env')

    @property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex
        """
        return self._values.get('env_regex')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels
        """
        return self._values.get('labels')

    @property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID
        """
        return self._values.get('tag')

    @property
    def address(self) -> typing.Optional[str]:
        """By default, the logging driver connects to localhost:24224.

        Supply the
        address option to connect to a different address. tcp(default) and unix
        sockets are supported.

        default
        :default: - address not set.
        """
        return self._values.get('address')

    @property
    def async_connect(self) -> typing.Optional[bool]:
        """Docker connects to Fluentd in the background.

        Messages are buffered until
        the connection is established.

        default
        :default: - false
        """
        return self._values.get('async_connect')

    @property
    def buffer_limit(self) -> typing.Optional[jsii.Number]:
        """The amount of data to buffer before flushing to disk.

        default
        :default: - The amount of RAM available to the container.
        """
        return self._values.get('buffer_limit')

    @property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """The maximum number of retries.

        default
        :default: - 4294967295 (2**32 - 1).
        """
        return self._values.get('max_retries')

    @property
    def retry_wait(self) -> typing.Optional[aws_cdk.core.Duration]:
        """How long to wait between retries.

        default
        :default: - 1 second
        """
        return self._values.get('retry_wait')

    @property
    def sub_second_precision(self) -> typing.Optional[bool]:
        """Generates event logs in nanosecond resolution.

        default
        :default: - false
        """
        return self._values.get('sub_second_precision')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FluentdLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.GelfCompressionType")
class GelfCompressionType(enum.Enum):
    """The type of compression the GELF driver uses to compress each log message."""
    GZIP = "GZIP"
    ZLIB = "ZLIB"
    NONE = "NONE"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.GelfLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'address': 'address', 'compression_level': 'compressionLevel', 'compression_type': 'compressionType', 'tcp_max_reconnect': 'tcpMaxReconnect', 'tcp_reconnect_delay': 'tcpReconnectDelay'})
class GelfLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, address: str, compression_level: typing.Optional[jsii.Number]=None, compression_type: typing.Optional["GelfCompressionType"]=None, tcp_max_reconnect: typing.Optional[jsii.Number]=None, tcp_reconnect_delay: typing.Optional[aws_cdk.core.Duration]=None):
        """Specifies the journald log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/gelf/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param address: The address of the GELF server. tcp and udp are the only supported URI specifier and you must specify the port.
        :param compression_level: UDP Only The level of compression when gzip or zlib is the gelf-compression-type. An integer in the range of -1 to 9 (BestCompression). Higher levels provide more compression at lower speed. Either -1 or 0 disables compression. Default: - 1
        :param compression_type: UDP Only The type of compression the GELF driver uses to compress each log message. Allowed values are gzip, zlib and none. Default: - gzip
        :param tcp_max_reconnect: TCP Only The maximum number of reconnection attempts when the connection drop. A positive integer. Default: - 3
        :param tcp_reconnect_delay: TCP Only The number of seconds to wait between reconnection attempts. A positive integer. Default: - 1
        """
        self._values = {
            'address': address,
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if compression_level is not None: self._values["compression_level"] = compression_level
        if compression_type is not None: self._values["compression_type"] = compression_type
        if tcp_max_reconnect is not None: self._values["tcp_max_reconnect"] = tcp_max_reconnect
        if tcp_reconnect_delay is not None: self._values["tcp_reconnect_delay"] = tcp_reconnect_delay

    @property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env
        """
        return self._values.get('env')

    @property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex
        """
        return self._values.get('env_regex')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels
        """
        return self._values.get('labels')

    @property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID
        """
        return self._values.get('tag')

    @property
    def address(self) -> str:
        """The address of the GELF server.

        tcp and udp are the only supported URI
        specifier and you must specify the port.
        """
        return self._values.get('address')

    @property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        """UDP Only The level of compression when gzip or zlib is the gelf-compression-type. An integer in the range of -1 to 9 (BestCompression). Higher levels provide more compression at lower speed. Either -1 or 0 disables compression.

        default
        :default: - 1
        """
        return self._values.get('compression_level')

    @property
    def compression_type(self) -> typing.Optional["GelfCompressionType"]:
        """UDP Only The type of compression the GELF driver uses to compress each log message.

        Allowed values are gzip, zlib and none.

        default
        :default: - gzip
        """
        return self._values.get('compression_type')

    @property
    def tcp_max_reconnect(self) -> typing.Optional[jsii.Number]:
        """TCP Only The maximum number of reconnection attempts when the connection drop. A positive integer.

        default
        :default: - 3
        """
        return self._values.get('tcp_max_reconnect')

    @property
    def tcp_reconnect_delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """TCP Only The number of seconds to wait between reconnection attempts. A positive integer.

        default
        :default: - 1
        """
        return self._values.get('tcp_reconnect_delay')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GelfLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.HealthCheck", jsii_struct_bases=[], name_mapping={'command': 'command', 'interval': 'interval', 'retries': 'retries', 'start_period': 'startPeriod', 'timeout': 'timeout'})
class HealthCheck():
    def __init__(self, *, command: typing.List[str], interval: typing.Optional[aws_cdk.core.Duration]=None, retries: typing.Optional[jsii.Number]=None, start_period: typing.Optional[aws_cdk.core.Duration]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None):
        """The health check command and associated configuration parameters for the container.

        :param command: A string array representing the command that the container runs to determine if it is healthy. The string array must start with CMD to execute the command arguments directly, or CMD-SHELL to run the command with the container's default shell. For example: [ "CMD-SHELL", "curl -f http://localhost/ || exit 1" ]
        :param interval: The time period in seconds between each health check execution. You may specify between 5 and 300 seconds. Default: Duration.seconds(30)
        :param retries: The number of times to retry a failed health check before the container is considered unhealthy. You may specify between 1 and 10 retries. Default: 3
        :param start_period: The optional grace period within which to provide containers time to bootstrap before failed health checks count towards the maximum number of retries. You may specify between 0 and 300 seconds. Default: No start period
        :param timeout: The time period in seconds to wait for a health check to succeed before it is considered a failure. You may specify between 2 and 60 seconds. Default: Duration.seconds(5)
        """
        self._values = {
            'command': command,
        }
        if interval is not None: self._values["interval"] = interval
        if retries is not None: self._values["retries"] = retries
        if start_period is not None: self._values["start_period"] = start_period
        if timeout is not None: self._values["timeout"] = timeout

    @property
    def command(self) -> typing.List[str]:
        """A string array representing the command that the container runs to determine if it is healthy. The string array must start with CMD to execute the command arguments directly, or CMD-SHELL to run the command with the container's default shell.

        For example: [ "CMD-SHELL", "curl -f http://localhost/ || exit 1" ]
        """
        return self._values.get('command')

    @property
    def interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period in seconds between each health check execution.

        You may specify between 5 and 300 seconds.

        default
        :default: Duration.seconds(30)
        """
        return self._values.get('interval')

    @property
    def retries(self) -> typing.Optional[jsii.Number]:
        """The number of times to retry a failed health check before the container is considered unhealthy.

        You may specify between 1 and 10 retries.

        default
        :default: 3
        """
        return self._values.get('retries')

    @property
    def start_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The optional grace period within which to provide containers time to bootstrap before failed health checks count towards the maximum number of retries.

        You may specify between 0 and 300 seconds.

        default
        :default: No start period
        """
        return self._values.get('start_period')

    @property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The time period in seconds to wait for a health check to succeed before it is considered a failure.

        You may specify between 2 and 60 seconds.

        default
        :default: Duration.seconds(5)
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HealthCheck(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Host", jsii_struct_bases=[], name_mapping={'source_path': 'sourcePath'})
class Host():
    def __init__(self, *, source_path: typing.Optional[str]=None):
        """The details on a container instance bind mount host volume.

        :param source_path: Specifies the path on the host container instance that is presented to the container. If the sourcePath value does not exist on the host container instance, the Docker daemon creates it. If the location does exist, the contents of the source path folder are exported. This property is not supported for tasks that use the Fargate launch type.
        """
        self._values = {
        }
        if source_path is not None: self._values["source_path"] = source_path

    @property
    def source_path(self) -> typing.Optional[str]:
        """Specifies the path on the host container instance that is presented to the container. If the sourcePath value does not exist on the host container instance, the Docker daemon creates it. If the location does exist, the contents of the source path folder are exported.

        This property is not supported for tasks that use the Fargate launch type.
        """
        return self._values.get('source_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Host(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ICluster")
class ICluster(aws_cdk.core.IResource, jsii.compat.Protocol):
    """A regional grouping of one or more container instances on which you can run tasks and services."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage the allowed network connections for the cluster with Security Groups."""
        ...

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Specifies whether the cluster has EC2 instance capacity."""
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC associated with the cluster."""
        ...

    @property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> typing.Optional[aws_cdk.aws_autoscaling.IAutoScalingGroup]:
        """The autoscaling group added to the cluster if capacity is associated to the cluster."""
        ...

    @property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """The AWS Cloud Map namespace to associate with the cluster."""
        ...


class _IClusterProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """A regional grouping of one or more container instances on which you can run tasks and services."""
    __jsii_type__ = "@aws-cdk/aws-ecs.ICluster"
    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage the allowed network connections for the cluster with Security Groups."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Specifies whether the cluster has EC2 instance capacity."""
        return jsii.get(self, "hasEc2Capacity")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC associated with the cluster."""
        return jsii.get(self, "vpc")

    @property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> typing.Optional[aws_cdk.aws_autoscaling.IAutoScalingGroup]:
        """The autoscaling group added to the cluster if capacity is associated to the cluster."""
        return jsii.get(self, "autoscalingGroup")

    @property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """The AWS Cloud Map namespace to associate with the cluster."""
        return jsii.get(self, "defaultCloudMapNamespace")


@jsii.implements(ICluster)
class Cluster(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Cluster"):
    """A regional grouping of one or more container instances on which you can run tasks and services."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, capacity: typing.Optional["AddCapacityOptions"]=None, cluster_name: typing.Optional[str]=None, default_cloud_map_namespace: typing.Optional["CloudMapNamespaceOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the Cluster class.

        :param scope: -
        :param id: -
        :param props: -
        :param capacity: The ec2 capacity to add to the cluster. Default: - no EC2 capacity will be added, you can use ``addCapacity`` to add capacity later.
        :param cluster_name: The name for the cluster. Default: CloudFormation-generated name
        :param default_cloud_map_namespace: The service discovery namespace created in this cluster. Default: - no service discovery namespace created, you can use ``addDefaultCloudMapNamespace`` to add a default service discovery namespace later.
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs
        """
        props = ClusterProps(capacity=capacity, cluster_name=cluster_name, default_cloud_map_namespace=default_cloud_map_namespace, vpc=vpc)

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @classmethod
    def from_cluster_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, cluster_name: str, security_groups: typing.List[aws_cdk.aws_ec2.ISecurityGroup], vpc: aws_cdk.aws_ec2.IVpc, autoscaling_group: typing.Optional[aws_cdk.aws_autoscaling.IAutoScalingGroup]=None, cluster_arn: typing.Optional[str]=None, default_cloud_map_namespace: typing.Optional[aws_cdk.aws_servicediscovery.INamespace]=None, has_ec2_capacity: typing.Optional[bool]=None) -> "ICluster":
        """Import an existing cluster to the stack from its attributes.

        :param scope: -
        :param id: -
        :param attrs: -
        :param cluster_name: The name of the cluster.
        :param security_groups: The security groups associated with the container instances registered to the cluster.
        :param vpc: The VPC associated with the cluster.
        :param autoscaling_group: Autoscaling group added to the cluster if capacity is added. Default: - No default autoscaling group
        :param cluster_arn: The Amazon Resource Name (ARN) that identifies the cluster. Default: Derived from clusterName
        :param default_cloud_map_namespace: The AWS Cloud Map namespace to associate with the cluster. Default: - No default namespace
        :param has_ec2_capacity: Specifies whether the cluster has EC2 instance capacity. Default: true
        """
        attrs = ClusterAttributes(cluster_name=cluster_name, security_groups=security_groups, vpc=vpc, autoscaling_group=autoscaling_group, cluster_arn=cluster_arn, default_cloud_map_namespace=default_cloud_map_namespace, has_ec2_capacity=has_ec2_capacity)

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, auto_scaling_group: aws_cdk.aws_autoscaling.AutoScalingGroup, *, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """This method adds compute capacity to a cluster using the specified AutoScalingGroup.

        :param auto_scaling_group: the ASG to add to this cluster. [disable-awslint:ref-via-interface] is needed in order to install the ECS agent by updating the ASGs user data.
        :param options: -
        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)
        """
        options = AddAutoScalingGroupCapacityOptions(can_containers_access_instance_role=can_containers_access_instance_role, spot_instance_draining=spot_instance_draining, task_drain_time=task_drain_time)

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(self, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, machine_image: typing.Optional[aws_cdk.aws_ec2.IMachineImage]=None, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[aws_cdk.core.Duration]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[aws_cdk.aws_autoscaling.HealthCheck]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[aws_cdk.aws_autoscaling.UpdateType]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        """This method adds compute capacity to a cluster by creating an AutoScalingGroup with the specified options.

        Returns the AutoScalingGroup so you can add autoscaling settings to it.

        :param id: -
        :param options: -
        :param instance_type: The EC2 instance type to use when launching instances into the AutoScalingGroup.
        :param machine_image: The ECS-optimized AMI variant to use. For more information, see `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_. Default: - Amazon Linux 2
        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)
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
        options = AddCapacityOptions(instance_type=instance_type, machine_image=machine_image, can_containers_access_instance_role=can_containers_access_instance_role, spot_instance_draining=spot_instance_draining, task_drain_time=task_drain_time, allow_all_outbound=allow_all_outbound, associate_public_ip_address=associate_public_ip_address, cooldown=cooldown, desired_capacity=desired_capacity, health_check=health_check, ignore_unmodified_size_properties=ignore_unmodified_size_properties, key_name=key_name, max_capacity=max_capacity, min_capacity=min_capacity, notifications_topic=notifications_topic, replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent, resource_signal_count=resource_signal_count, resource_signal_timeout=resource_signal_timeout, rolling_update_configuration=rolling_update_configuration, spot_price=spot_price, update_type=update_type, vpc_subnets=vpc_subnets)

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addDefaultCloudMapNamespace")
    def add_default_cloud_map_namespace(self, *, name: str, type: typing.Optional[aws_cdk.aws_servicediscovery.NamespaceType]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_servicediscovery.INamespace:
        """Add an AWS Cloud Map DNS namespace for this cluster. NOTE: HttpNamespaces are not supported, as ECS always requires a DNSConfig when registering an instance to a Cloud Map service.

        :param options: -
        :param name: The name of the namespace, such as example.com.
        :param type: The type of CloudMap Namespace to create. Default: PrivateDns
        :param vpc: The VPC to associate the namespace with. This property is required for private DNS namespaces. Default: VPC of the cluster for Private DNS Namespace, otherwise none
        """
        options = CloudMapNamespaceOptions(name=name, type=type, vpc=vpc)

        return jsii.invoke(self, "addDefaultCloudMapNamespace", [options])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the specifed CloudWatch metric for this cluster.

        :param metric_name: -
        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuReservation")
    def metric_cpu_reservation(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters CPU reservation.

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricCpuReservation", [props])

    @jsii.member(jsii_name="metricMemoryReservation")
    def metric_memory_reservation(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters memory reservation.

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricMemoryReservation", [props])

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster."""
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster."""
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage the allowed network connections for the cluster with Security Groups."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Whether the cluster has EC2 capacity associated with it."""
        return jsii.get(self, "hasEc2Capacity")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC associated with the cluster."""
        return jsii.get(self, "vpc")

    @property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> typing.Optional[aws_cdk.aws_autoscaling.IAutoScalingGroup]:
        """Getter for autoscaling group added to cluster."""
        return jsii.get(self, "autoscalingGroup")

    @property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """Getter for namespace added to cluster."""
        return jsii.get(self, "defaultCloudMapNamespace")


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IEcsLoadBalancerTarget")
class IEcsLoadBalancerTarget(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget, aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget, jsii.compat.Protocol):
    """Interface for ECS load balancer target."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IEcsLoadBalancerTargetProxy

    pass

class _IEcsLoadBalancerTargetProxy(jsii.proxy_for(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget), jsii.proxy_for(aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget), jsii.proxy_for(aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget)):
    """Interface for ECS load balancer target."""
    __jsii_type__ = "@aws-cdk/aws-ecs.IEcsLoadBalancerTarget"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IService")
class IService(aws_cdk.core.IResource, jsii.compat.Protocol):
    """The interface for a service."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IServiceProxy

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        attribute:
        :attribute:: true
        """
        ...


class _IServiceProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """The interface for a service."""
    __jsii_type__ = "@aws-cdk/aws-ecs.IService"
    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceArn")


@jsii.implements(IService, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget, aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget)
class BaseService(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.BaseService"):
    """The base class for Ec2Service and FargateService services."""
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseServiceProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, props: "BaseServiceProps", additional_props: typing.Any, task_definition: "TaskDefinition") -> None:
        """Constructs a new instance of the BaseService class.

        :param scope: -
        :param id: -
        :param props: -
        :param additional_props: -
        :param task_definition: -
        """
        jsii.create(BaseService, self, [scope, id, props, additional_props, task_definition])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """This method is called to attach this service to an Application Load Balancer.

        Don't call this function directly. Instead, call ``listener.addTargets()``
        to add this service to a load balancer.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> None:
        """Registers the service as a target of a Classic Load Balancer (CLB).

        Don't call this. Call ``loadBalancer.addTarget()`` instead.

        :param load_balancer: -
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """This method is called to attach this service to a Network Load Balancer.

        Don't call this function directly. Instead, call ``listener.addTargets()``
        to add this service to a load balancer.

        :param target_group: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="autoScaleTaskCount")
    def auto_scale_task_count(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> "ScalableTaskCount":
        """An attribute representing the minimum and maximum task count for an AutoScalingGroup.

        :param props: -
        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1
        """
        props = aws_cdk.aws_applicationautoscaling.EnableScalingProps(max_capacity=max_capacity, min_capacity=min_capacity)

        return jsii.invoke(self, "autoScaleTaskCount", [props])

    @jsii.member(jsii_name="configureAwsVpcNetworking")
    def _configure_aws_vpc_networking(self, vpc: aws_cdk.aws_ec2.IVpc, assign_public_ip: typing.Optional[bool]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None) -> None:
        """This method is called to create a networkConfiguration.

        :param vpc: -
        :param assign_public_ip: -
        :param vpc_subnets: -
        :param security_group: -
        """
        return jsii.invoke(self, "configureAwsVpcNetworking", [vpc, assign_public_ip, vpc_subnets, security_group])

    @jsii.member(jsii_name="enableCloudMap")
    def enable_cloud_map(self, *, cloud_map_namespace: typing.Optional[aws_cdk.aws_servicediscovery.INamespace]=None, dns_record_type: typing.Optional[aws_cdk.aws_servicediscovery.DnsRecordType]=None, dns_ttl: typing.Optional[aws_cdk.core.Duration]=None, failure_threshold: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None) -> aws_cdk.aws_servicediscovery.Service:
        """Enable CloudMap service discovery for the service.

        :param options: -
        :param cloud_map_namespace: The service discovery namespace for the Cloud Map service to attach to the ECS service. Default: - the defaultCloudMapNamespace associated to the cluster
        :param dns_record_type: The DNS record type that you want AWS Cloud Map to create. The supported record types are A or SRV. Default: DnsRecordType.A
        :param dns_ttl: The amount of time that you want DNS resolvers to cache the settings for this record. Default: 60
        :param failure_threshold: The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance. NOTE: This is used for HealthCheckCustomConfig
        :param name: The name of the Cloud Map service to attach to the ECS service. Default: CloudFormation-generated name

        return
        :return: The created CloudMap service
        """
        options = CloudMapOptions(cloud_map_namespace=cloud_map_namespace, dns_record_type=dns_record_type, dns_ttl=dns_ttl, failure_threshold=failure_threshold, name=name)

        return jsii.invoke(self, "enableCloudMap", [options])

    @jsii.member(jsii_name="loadBalancerTarget")
    def load_balancer_target(self, *, container_name: str, container_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None) -> "IEcsLoadBalancerTarget":
        """Return a load balancing target for a specific container and port.

        Use this function to create a load balancer target if you want to load balance to
        another container than the first essential container or the first mapped port on
        the container.

        Use the return value of this function where you would normally use a load balancer
        target, instead of the ``Service`` object itself.

        :param options: -
        :param container_name: The name of the container.
        :param container_port: The port number of the container. Only applicable when using application/network load balancers. Default: - Container port of the first added port mapping.
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: Protocol.TCP

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            listener.add_targets(service.load_balancer_target(
                container_name="MyContainer",
                container_port=1234
            ))
        """
        options = LoadBalancerTargetOptions(container_name=container_name, container_port=container_port, protocol=protocol)

        return jsii.invoke(self, "loadBalancerTarget", [options])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the specified CloudWatch metric name for this service.

        :param metric_name: -
        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuUtilization")
    def metric_cpu_utilization(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters CPU utilization.

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricCpuUtilization", [props])

    @jsii.member(jsii_name="metricMemoryUtilization")
    def metric_memory_utilization(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters memory utilization.

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: average over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricMemoryUtilization", [props])

    @jsii.member(jsii_name="registerLoadBalancerTargets")
    def register_load_balancer_targets(self, *targets: "EcsTarget") -> None:
        """Use this function to create all load balancer targets to be registered in this service, add them to target groups, and attach target groups to listeners accordingly.

        Alternatively, you can use ``listener.addTargets()`` to create targets and add them to target groups.

        :param targets: -

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            service.register_load_balancer_targets(
                container_target={
                    "container_name": "web",
                    "container_port": 80
                },
                target_group_id="ECS",
                listener=ecs.ListenerConfig.application_listener(listener,
                    protocol=elbv2.ApplicationProtocol.HTTPS
                )
            )
        """
        return jsii.invoke(self, "registerLoadBalancerTargets", [*targets])

    @property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "ICluster":
        """The cluster that hosts the service."""
        return jsii.get(self, "cluster")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups which manage the allowed network traffic for the service."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service."""
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """The name of the service.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceName")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        """The task definition to use for tasks in the service."""
        return jsii.get(self, "taskDefinition")

    @property
    @jsii.member(jsii_name="cloudMapService")
    def cloud_map_service(self) -> typing.Optional[aws_cdk.aws_servicediscovery.IService]:
        """The CloudMap service created for this service, if any."""
        return jsii.get(self, "cloudMapService")

    @property
    @jsii.member(jsii_name="loadBalancers")
    def _load_balancers(self) -> typing.List["CfnService.LoadBalancerProperty"]:
        """A list of Elastic Load Balancing load balancer objects, containing the load balancer name, the container name (as it appears in a container definition), and the container port to access from the load balancer."""
        return jsii.get(self, "loadBalancers")

    @_load_balancers.setter
    def _load_balancers(self, value: typing.List["CfnService.LoadBalancerProperty"]):
        return jsii.set(self, "loadBalancers", value)

    @property
    @jsii.member(jsii_name="serviceRegistries")
    def _service_registries(self) -> typing.List["CfnService.ServiceRegistryProperty"]:
        """The details of the service discovery registries to assign to this service. For more information, see Service Discovery."""
        return jsii.get(self, "serviceRegistries")

    @_service_registries.setter
    def _service_registries(self, value: typing.List["CfnService.ServiceRegistryProperty"]):
        return jsii.set(self, "serviceRegistries", value)

    @property
    @jsii.member(jsii_name="cloudmapService")
    def _cloudmap_service(self) -> typing.Optional[aws_cdk.aws_servicediscovery.Service]:
        """The details of the AWS Cloud Map service."""
        return jsii.get(self, "cloudmapService")

    @_cloudmap_service.setter
    def _cloudmap_service(self, value: typing.Optional[aws_cdk.aws_servicediscovery.Service]):
        return jsii.set(self, "cloudmapService", value)

    @property
    @jsii.member(jsii_name="networkConfiguration")
    def _network_configuration(self) -> typing.Optional["CfnService.NetworkConfigurationProperty"]:
        """A list of Elastic Load Balancing load balancer objects, containing the load balancer name, the container name (as it appears in a container definition), and the container port to access from the load balancer."""
        return jsii.get(self, "networkConfiguration")

    @_network_configuration.setter
    def _network_configuration(self, value: typing.Optional["CfnService.NetworkConfigurationProperty"]):
        return jsii.set(self, "networkConfiguration", value)


class _BaseServiceProxy(BaseService, jsii.proxy_for(aws_cdk.core.Resource)):
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IEc2Service")
class IEc2Service(IService, jsii.compat.Protocol):
    """The interface for a service using the EC2 launch type on an ECS cluster."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IEc2ServiceProxy

    pass

class _IEc2ServiceProxy(jsii.proxy_for(IService)):
    """The interface for a service using the EC2 launch type on an ECS cluster."""
    __jsii_type__ = "@aws-cdk/aws-ecs.IEc2Service"
    pass

@jsii.implements(IEc2Service)
class Ec2Service(BaseService, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Ec2Service"):
    """This creates a service using the EC2 launch type on an ECS cluster.

    resource:
    :resource:: AWS::ECS::Service
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, daemon: typing.Optional[bool]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, placement_strategies: typing.Optional[typing.List["PlacementStrategy"]]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the Ec2Service class.

        :param scope: -
        :param id: -
        :param props: -
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. This property is only used for tasks that use the awsvpc network mode. Default: - Use subnet default.
        :param daemon: Specifies whether the service will use the daemon scheduling strategy. If true, the service scheduler deploys exactly one task on each container instance in your cluster. When you are using this strategy, do not specify a desired number of tasks orany task placement strategies. Default: false
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. This property is only used for tasks that use the awsvpc network mode. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. This property is only used for tasks that use the awsvpc network mode. Default: - Private subnets.
        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        """
        props = Ec2ServiceProps(task_definition=task_definition, assign_public_ip=assign_public_ip, daemon=daemon, placement_constraints=placement_constraints, placement_strategies=placement_strategies, propagate_task_tags_from=propagate_task_tags_from, security_group=security_group, vpc_subnets=vpc_subnets, cluster=cluster, cloud_map_options=cloud_map_options, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, service_name=service_name)

        jsii.create(Ec2Service, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2ServiceArn")
    @classmethod
    def from_ec2_service_arn(cls, scope: aws_cdk.core.Construct, id: str, ec2_service_arn: str) -> "IEc2Service":
        """Imports from the specified service ARN.

        :param scope: -
        :param id: -
        :param ec2_service_arn: -
        """
        return jsii.sinvoke(cls, "fromEc2ServiceArn", [scope, id, ec2_service_arn])

    @jsii.member(jsii_name="addPlacementConstraints")
    def add_placement_constraints(self, *constraints: "PlacementConstraint") -> None:
        """Adds one or more placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        :param constraints: -
        """
        return jsii.invoke(self, "addPlacementConstraints", [*constraints])

    @jsii.member(jsii_name="addPlacementStrategies")
    def add_placement_strategies(self, *strategies: "PlacementStrategy") -> None:
        """Adds one or more placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        :param strategies: -
        """
        return jsii.invoke(self, "addPlacementStrategies", [*strategies])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validates this Ec2Service."""
        return jsii.invoke(self, "validate", [])


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IFargateService")
class IFargateService(IService, jsii.compat.Protocol):
    """The interface for a service using the Fargate launch type on an ECS cluster."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IFargateServiceProxy

    pass

class _IFargateServiceProxy(jsii.proxy_for(IService)):
    """The interface for a service using the Fargate launch type on an ECS cluster."""
    __jsii_type__ = "@aws-cdk/aws-ecs.IFargateService"
    pass

@jsii.implements(IFargateService)
class FargateService(BaseService, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.FargateService"):
    """This creates a service using the Fargate launch type on an ECS cluster.

    resource:
    :resource:: AWS::ECS::Service
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional["FargatePlatformVersion"]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the FargateService class.

        :param scope: -
        :param id: -
        :param props: -
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: - Use subnet default.
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. Default: - Private subnets.
        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        """
        props = FargateServiceProps(task_definition=task_definition, assign_public_ip=assign_public_ip, platform_version=platform_version, propagate_task_tags_from=propagate_task_tags_from, security_group=security_group, vpc_subnets=vpc_subnets, cluster=cluster, cloud_map_options=cloud_map_options, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, service_name=service_name)

        jsii.create(FargateService, self, [scope, id, props])

    @jsii.member(jsii_name="fromFargateServiceArn")
    @classmethod
    def from_fargate_service_arn(cls, scope: aws_cdk.core.Construct, id: str, fargate_service_arn: str) -> "IFargateService":
        """Import a task definition from the specified task definition ARN.

        :param scope: -
        :param id: -
        :param fargate_service_arn: -
        """
        return jsii.sinvoke(cls, "fromFargateServiceArn", [scope, id, fargate_service_arn])


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ITaskDefinition")
class ITaskDefinition(aws_cdk.core.IResource, jsii.compat.Protocol):
    """The interface for all task definitions."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ITaskDefinitionProxy

    @property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """What launch types this task definition should be compatible with."""
        ...

    @property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster."""
        ...

    @property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster."""
        ...

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """ARN of this task definition.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role for this task definition."""
        ...


class _ITaskDefinitionProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """The interface for all task definitions."""
    __jsii_type__ = "@aws-cdk/aws-ecs.ITaskDefinition"
    @property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """What launch types this task definition should be compatible with."""
        return jsii.get(self, "compatibility")

    @property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster."""
        return jsii.get(self, "isEc2Compatible")

    @property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster."""
        return jsii.get(self, "isFargateCompatible")

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """ARN of this task definition.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "taskDefinitionArn")

    @property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role for this task definition."""
        return jsii.get(self, "executionRole")


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IEc2TaskDefinition")
class IEc2TaskDefinition(ITaskDefinition, jsii.compat.Protocol):
    """The interface of a task definition run on an EC2 cluster."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IEc2TaskDefinitionProxy

    pass

class _IEc2TaskDefinitionProxy(jsii.proxy_for(ITaskDefinition)):
    """The interface of a task definition run on an EC2 cluster."""
    __jsii_type__ = "@aws-cdk/aws-ecs.IEc2TaskDefinition"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IFargateTaskDefinition")
class IFargateTaskDefinition(ITaskDefinition, jsii.compat.Protocol):
    """The interface of a task definition run on a Fargate cluster."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IFargateTaskDefinitionProxy

    pass

class _IFargateTaskDefinitionProxy(jsii.proxy_for(ITaskDefinition)):
    """The interface of a task definition run on a Fargate cluster."""
    __jsii_type__ = "@aws-cdk/aws-ecs.IFargateTaskDefinition"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ITaskDefinitionExtension")
class ITaskDefinitionExtension(jsii.compat.Protocol):
    """An extension for Task Definitions.

    Classes that want to make changes to a TaskDefinition (such as
    adding helper containers) can implement this interface, and can
    then be "added" to a TaskDefinition like so::

       taskDefinition.addExtension(new MyExtension("some_parameter"));
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ITaskDefinitionExtensionProxy

    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        """Apply the extension to the given TaskDefinition.

        :param task_definition: [disable-awslint:ref-via-interface].
        """
        ...


class _ITaskDefinitionExtensionProxy():
    """An extension for Task Definitions.

    Classes that want to make changes to a TaskDefinition (such as
    adding helper containers) can implement this interface, and can
    then be "added" to a TaskDefinition like so::

       taskDefinition.addExtension(new MyExtension("some_parameter"));
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.ITaskDefinitionExtension"
    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        """Apply the extension to the given TaskDefinition.

        :param task_definition: [disable-awslint:ref-via-interface].
        """
        return jsii.invoke(self, "extend", [task_definition])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.JournaldLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag'})
class JournaldLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None):
        """Specifies the journald log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/journald/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag

    @property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env
        """
        return self._values.get('env')

    @property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex
        """
        return self._values.get('env_regex')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels
        """
        return self._values.get('labels')

    @property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID
        """
        return self._values.get('tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JournaldLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.JsonFileLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'compress': 'compress', 'max_file': 'maxFile', 'max_size': 'maxSize'})
class JsonFileLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, compress: typing.Optional[bool]=None, max_file: typing.Optional[jsii.Number]=None, max_size: typing.Optional[str]=None):
        """Specifies the json-file log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/json-file/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param compress: Toggles compression for rotated logs. Default: - false
        :param max_file: The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. Only effective when max-size is also set. A positive integer. Default: - 1
        :param max_size: The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g). Default: - -1 (unlimited)
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if compress is not None: self._values["compress"] = compress
        if max_file is not None: self._values["max_file"] = max_file
        if max_size is not None: self._values["max_size"] = max_size

    @property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env
        """
        return self._values.get('env')

    @property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex
        """
        return self._values.get('env_regex')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels
        """
        return self._values.get('labels')

    @property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID
        """
        return self._values.get('tag')

    @property
    def compress(self) -> typing.Optional[bool]:
        """Toggles compression for rotated logs.

        default
        :default: - false
        """
        return self._values.get('compress')

    @property
    def max_file(self) -> typing.Optional[jsii.Number]:
        """The maximum number of log files that can be present.

        If rolling the logs creates
        excess files, the oldest file is removed. Only effective when max-size is also set.
        A positive integer.

        default
        :default: - 1
        """
        return self._values.get('max_file')

    @property
    def max_size(self) -> typing.Optional[str]:
        """The maximum size of the log before it is rolled.

        A positive integer plus a modifier
        representing the unit of measure (k, m, or g).

        default
        :default: - -1 (unlimited)
        """
        return self._values.get('max_size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JsonFileLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.LaunchType")
class LaunchType(enum.Enum):
    """The launch type of an ECS service."""
    EC2 = "EC2"
    """The service will be launched using the EC2 launch type."""
    FARGATE = "FARGATE"
    """The service will be launched using the FARGATE launch type."""

class LinuxParameters(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.LinuxParameters"):
    """Linux-specific options that are applied to the container."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, init_process_enabled: typing.Optional[bool]=None, shared_memory_size: typing.Optional[jsii.Number]=None) -> None:
        """Constructs a new instance of the LinuxParameters class.

        :param scope: -
        :param id: -
        :param props: -
        :param init_process_enabled: Specifies whether to run an init process inside the container that forwards signals and reaps processes. Default: false
        :param shared_memory_size: The value for the size (in MiB) of the /dev/shm volume. Default: No shared memory.
        """
        props = LinuxParametersProps(init_process_enabled=init_process_enabled, shared_memory_size=shared_memory_size)

        jsii.create(LinuxParameters, self, [scope, id, props])

    @jsii.member(jsii_name="addCapabilities")
    def add_capabilities(self, *cap: "Capability") -> None:
        """Adds one or more Linux capabilities to the Docker configuration of a container.

        Only works with EC2 launch type.

        :param cap: -
        """
        return jsii.invoke(self, "addCapabilities", [*cap])

    @jsii.member(jsii_name="addDevices")
    def add_devices(self, *device: "Device") -> None:
        """Adds one or more host devices to a container.

        :param device: -
        """
        return jsii.invoke(self, "addDevices", [*device])

    @jsii.member(jsii_name="addTmpfs")
    def add_tmpfs(self, *tmpfs: "Tmpfs") -> None:
        """Specifies the container path, mount options, and size (in MiB) of the tmpfs mount for a container.

        Only works with EC2 launch type.

        :param tmpfs: -
        """
        return jsii.invoke(self, "addTmpfs", [*tmpfs])

    @jsii.member(jsii_name="dropCapabilities")
    def drop_capabilities(self, *cap: "Capability") -> None:
        """Removes one or more Linux capabilities to the Docker configuration of a container.

        Only works with EC2 launch type.

        :param cap: -
        """
        return jsii.invoke(self, "dropCapabilities", [*cap])

    @jsii.member(jsii_name="renderLinuxParameters")
    def render_linux_parameters(self) -> "CfnTaskDefinition.LinuxParametersProperty":
        """Renders the Linux parameters to a CloudFormation object."""
        return jsii.invoke(self, "renderLinuxParameters", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LinuxParametersProps", jsii_struct_bases=[], name_mapping={'init_process_enabled': 'initProcessEnabled', 'shared_memory_size': 'sharedMemorySize'})
class LinuxParametersProps():
    def __init__(self, *, init_process_enabled: typing.Optional[bool]=None, shared_memory_size: typing.Optional[jsii.Number]=None):
        """The properties for defining Linux-specific options that are applied to the container.

        :param init_process_enabled: Specifies whether to run an init process inside the container that forwards signals and reaps processes. Default: false
        :param shared_memory_size: The value for the size (in MiB) of the /dev/shm volume. Default: No shared memory.
        """
        self._values = {
        }
        if init_process_enabled is not None: self._values["init_process_enabled"] = init_process_enabled
        if shared_memory_size is not None: self._values["shared_memory_size"] = shared_memory_size

    @property
    def init_process_enabled(self) -> typing.Optional[bool]:
        """Specifies whether to run an init process inside the container that forwards signals and reaps processes.

        default
        :default: false
        """
        return self._values.get('init_process_enabled')

    @property
    def shared_memory_size(self) -> typing.Optional[jsii.Number]:
        """The value for the size (in MiB) of the /dev/shm volume.

        default
        :default: No shared memory.
        """
        return self._values.get('shared_memory_size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LinuxParametersProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ListenerConfig(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.ListenerConfig"):
    """Base class for configuring listener when registering targets."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ListenerConfigProxy

    def __init__(self) -> None:
        jsii.create(ListenerConfig, self, [])

    @jsii.member(jsii_name="applicationListener")
    @classmethod
    def application_listener(cls, listener: aws_cdk.aws_elasticloadbalancingv2.ApplicationListener, *, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.HealthCheck]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None, slow_start: typing.Optional[aws_cdk.core.Duration]=None, stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None) -> "ListenerConfig":
        """Create a config for adding target group to ALB listener.

        :param listener: -
        :param props: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        """
        props = aws_cdk.aws_elasticloadbalancingv2.AddApplicationTargetsProps(deregistration_delay=deregistration_delay, health_check=health_check, port=port, protocol=protocol, slow_start=slow_start, stickiness_cookie_duration=stickiness_cookie_duration, target_group_name=target_group_name, targets=targets, host_header=host_header, path_pattern=path_pattern, priority=priority)

        return jsii.sinvoke(cls, "applicationListener", [listener, props])

    @jsii.member(jsii_name="networkListener")
    @classmethod
    def network_listener(cls, listener: aws_cdk.aws_elasticloadbalancingv2.NetworkListener, *, port: jsii.Number, deregistration_delay: typing.Optional[aws_cdk.core.Duration]=None, health_check: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.HealthCheck]=None, proxy_protocol_v2: typing.Optional[bool]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget]]=None) -> "ListenerConfig":
        """Create a config for adding target group to NLB listener.

        :param listener: -
        :param props: -
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.
        """
        props = aws_cdk.aws_elasticloadbalancingv2.AddNetworkTargetsProps(port=port, deregistration_delay=deregistration_delay, health_check=health_check, proxy_protocol_v2=proxy_protocol_v2, target_group_name=target_group_name, targets=targets)

        return jsii.sinvoke(cls, "networkListener", [listener, props])

    @jsii.member(jsii_name="addTargets")
    @abc.abstractmethod
    def add_targets(self, id: str, target: "LoadBalancerTargetOptions", service: "BaseService") -> None:
        """Create and attach a target group to listener.

        :param id: -
        :param target: -
        :param service: -
        """
        ...


class _ListenerConfigProxy(ListenerConfig):
    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, target: "LoadBalancerTargetOptions", service: "BaseService") -> None:
        """Create and attach a target group to listener.

        :param id: -
        :param target: -
        :param service: -
        """
        return jsii.invoke(self, "addTargets", [id, target, service])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LoadBalancerTargetOptions", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'container_port': 'containerPort', 'protocol': 'protocol'})
class LoadBalancerTargetOptions():
    def __init__(self, *, container_name: str, container_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None):
        """Properties for defining an ECS target.

        The port mapping for it must already have been created through addPortMapping().

        :param container_name: The name of the container.
        :param container_port: The port number of the container. Only applicable when using application/network load balancers. Default: - Container port of the first added port mapping.
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: Protocol.TCP
        """
        self._values = {
            'container_name': container_name,
        }
        if container_port is not None: self._values["container_port"] = container_port
        if protocol is not None: self._values["protocol"] = protocol

    @property
    def container_name(self) -> str:
        """The name of the container."""
        return self._values.get('container_name')

    @property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number of the container.

        Only applicable when using application/network load balancers.

        default
        :default: - Container port of the first added port mapping.
        """
        return self._values.get('container_port')

    @property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol used for the port mapping.

        Only applicable when using application load balancers.

        default
        :default: Protocol.TCP
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancerTargetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LogDriver(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.LogDriver"):
    """The base class for log drivers."""
    @staticmethod
    def __jsii_proxy_class__():
        return _LogDriverProxy

    def __init__(self) -> None:
        jsii.create(LogDriver, self, [])

    @jsii.member(jsii_name="awsLogs")
    @classmethod
    def aws_logs(cls, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, multiline_pattern: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to CloudWatch Logs.

        :param props: -
        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.
        """
        props = AwsLogDriverProps(stream_prefix=stream_prefix, datetime_format=datetime_format, log_group=log_group, log_retention=log_retention, multiline_pattern=multiline_pattern)

        return jsii.sinvoke(cls, "awsLogs", [props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param scope: -
        :param container_definition: -
        """
        ...


class _LogDriverProxy(LogDriver):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param scope: -
        :param container_definition: -
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


class AwsLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.AwsLogDriver"):
    """A log driver that sends log information to CloudWatch Logs."""
    def __init__(self, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, multiline_pattern: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the AwsLogDriver class.

        :param props: the awslogs log driver configuration options.
        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.
        """
        props = AwsLogDriverProps(stream_prefix=stream_prefix, datetime_format=datetime_format, log_group=log_group, log_retention=log_retention, multiline_pattern=multiline_pattern)

        jsii.create(AwsLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param scope: -
        :param container_definition: -
        """
        return jsii.invoke(self, "bind", [scope, container_definition])

    @property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        """The log group to send log streams to.

        Only available after the LogDriver has been bound to a ContainerDefinition.
        """
        return jsii.get(self, "logGroup")

    @log_group.setter
    def log_group(self, value: typing.Optional[aws_cdk.aws_logs.ILogGroup]):
        return jsii.set(self, "logGroup", value)


class FluentdLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.FluentdLogDriver"):
    """A log driver that sends log information to journald Logs."""
    def __init__(self, *, address: typing.Optional[str]=None, async_connect: typing.Optional[bool]=None, buffer_limit: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, retry_wait: typing.Optional[aws_cdk.core.Duration]=None, sub_second_precision: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the FluentdLogDriver class.

        :param props: the fluentd log driver configuration options.
        :param address: By default, the logging driver connects to localhost:24224. Supply the address option to connect to a different address. tcp(default) and unix sockets are supported. Default: - address not set.
        :param async_connect: Docker connects to Fluentd in the background. Messages are buffered until the connection is established. Default: - false
        :param buffer_limit: The amount of data to buffer before flushing to disk. Default: - The amount of RAM available to the container.
        :param max_retries: The maximum number of retries. Default: - 4294967295 (2**32 - 1).
        :param retry_wait: How long to wait between retries. Default: - 1 second
        :param sub_second_precision: Generates event logs in nanosecond resolution. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = FluentdLogDriverProps(address=address, async_connect=async_connect, buffer_limit=buffer_limit, max_retries=max_retries, retry_wait=retry_wait, sub_second_precision=sub_second_precision, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(FluentdLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


class GelfLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.GelfLogDriver"):
    """A log driver that sends log information to journald Logs."""
    def __init__(self, *, address: str, compression_level: typing.Optional[jsii.Number]=None, compression_type: typing.Optional["GelfCompressionType"]=None, tcp_max_reconnect: typing.Optional[jsii.Number]=None, tcp_reconnect_delay: typing.Optional[aws_cdk.core.Duration]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the GelfLogDriver class.

        :param props: the gelf log driver configuration options.
        :param address: The address of the GELF server. tcp and udp are the only supported URI specifier and you must specify the port.
        :param compression_level: UDP Only The level of compression when gzip or zlib is the gelf-compression-type. An integer in the range of -1 to 9 (BestCompression). Higher levels provide more compression at lower speed. Either -1 or 0 disables compression. Default: - 1
        :param compression_type: UDP Only The type of compression the GELF driver uses to compress each log message. Allowed values are gzip, zlib and none. Default: - gzip
        :param tcp_max_reconnect: TCP Only The maximum number of reconnection attempts when the connection drop. A positive integer. Default: - 3
        :param tcp_reconnect_delay: TCP Only The number of seconds to wait between reconnection attempts. A positive integer. Default: - 1
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = GelfLogDriverProps(address=address, compression_level=compression_level, compression_type=compression_type, tcp_max_reconnect=tcp_max_reconnect, tcp_reconnect_delay=tcp_reconnect_delay, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(GelfLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


class JournaldLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.JournaldLogDriver"):
    """A log driver that sends log information to journald Logs."""
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the JournaldLogDriver class.

        :param props: the journald log driver configuration options.
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = JournaldLogDriverProps(env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(JournaldLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


class JsonFileLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.JsonFileLogDriver"):
    """A log driver that sends log information to json-file Logs."""
    def __init__(self, *, compress: typing.Optional[bool]=None, max_file: typing.Optional[jsii.Number]=None, max_size: typing.Optional[str]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the JsonFileLogDriver class.

        :param props: the json-file log driver configuration options.
        :param compress: Toggles compression for rotated logs. Default: - false
        :param max_file: The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. Only effective when max-size is also set. A positive integer. Default: - 1
        :param max_size: The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g). Default: - -1 (unlimited)
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = JsonFileLogDriverProps(compress=compress, max_file=max_file, max_size=max_size, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(JsonFileLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LogDriverConfig", jsii_struct_bases=[], name_mapping={'log_driver': 'logDriver', 'options': 'options'})
class LogDriverConfig():
    def __init__(self, *, log_driver: str, options: typing.Optional[typing.Mapping[str,str]]=None):
        """The configuration to use when creating a log driver.

        :param log_driver: The log driver to use for the container. The valid values listed for this parameter are log drivers that the Amazon ECS container agent can communicate with by default. For tasks using the Fargate launch type, the supported log drivers are awslogs and splunk. For tasks using the EC2 launch type, the supported log drivers are awslogs, syslog, gelf, fluentd, splunk, journald, and json-file. For more information about using the awslogs log driver, see `Using the awslogs Log Driver <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html>`_ in the Amazon Elastic Container Service Developer Guide.
        :param options: The configuration options to send to the log driver.
        """
        self._values = {
            'log_driver': log_driver,
        }
        if options is not None: self._values["options"] = options

    @property
    def log_driver(self) -> str:
        """The log driver to use for the container.

        The valid values listed for this parameter are log drivers
        that the Amazon ECS container agent can communicate with by default.

        For tasks using the Fargate launch type, the supported log drivers are awslogs and splunk.
        For tasks using the EC2 launch type, the supported log drivers are awslogs, syslog, gelf, fluentd, splunk, journald, and json-file.

        For more information about using the awslogs log driver, see
        `Using the awslogs Log Driver <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html>`_
        in the Amazon Elastic Container Service Developer Guide.
        """
        return self._values.get('log_driver')

    @property
    def options(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The configuration options to send to the log driver."""
        return self._values.get('options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogDriverConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LogDrivers(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.LogDrivers"):
    """The base class for log drivers."""
    def __init__(self) -> None:
        jsii.create(LogDrivers, self, [])

    @jsii.member(jsii_name="awsLogs")
    @classmethod
    def aws_logs(cls, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, multiline_pattern: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to CloudWatch Logs.

        :param props: -
        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.
        """
        props = AwsLogDriverProps(stream_prefix=stream_prefix, datetime_format=datetime_format, log_group=log_group, log_retention=log_retention, multiline_pattern=multiline_pattern)

        return jsii.sinvoke(cls, "awsLogs", [props])

    @jsii.member(jsii_name="fluentd")
    @classmethod
    def fluentd(cls, *, address: typing.Optional[str]=None, async_connect: typing.Optional[bool]=None, buffer_limit: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, retry_wait: typing.Optional[aws_cdk.core.Duration]=None, sub_second_precision: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to fluentd Logs.

        :param props: -
        :param address: By default, the logging driver connects to localhost:24224. Supply the address option to connect to a different address. tcp(default) and unix sockets are supported. Default: - address not set.
        :param async_connect: Docker connects to Fluentd in the background. Messages are buffered until the connection is established. Default: - false
        :param buffer_limit: The amount of data to buffer before flushing to disk. Default: - The amount of RAM available to the container.
        :param max_retries: The maximum number of retries. Default: - 4294967295 (2**32 - 1).
        :param retry_wait: How long to wait between retries. Default: - 1 second
        :param sub_second_precision: Generates event logs in nanosecond resolution. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = FluentdLogDriverProps(address=address, async_connect=async_connect, buffer_limit=buffer_limit, max_retries=max_retries, retry_wait=retry_wait, sub_second_precision=sub_second_precision, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "fluentd", [props])

    @jsii.member(jsii_name="gelf")
    @classmethod
    def gelf(cls, *, address: str, compression_level: typing.Optional[jsii.Number]=None, compression_type: typing.Optional["GelfCompressionType"]=None, tcp_max_reconnect: typing.Optional[jsii.Number]=None, tcp_reconnect_delay: typing.Optional[aws_cdk.core.Duration]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to gelf Logs.

        :param props: -
        :param address: The address of the GELF server. tcp and udp are the only supported URI specifier and you must specify the port.
        :param compression_level: UDP Only The level of compression when gzip or zlib is the gelf-compression-type. An integer in the range of -1 to 9 (BestCompression). Higher levels provide more compression at lower speed. Either -1 or 0 disables compression. Default: - 1
        :param compression_type: UDP Only The type of compression the GELF driver uses to compress each log message. Allowed values are gzip, zlib and none. Default: - gzip
        :param tcp_max_reconnect: TCP Only The maximum number of reconnection attempts when the connection drop. A positive integer. Default: - 3
        :param tcp_reconnect_delay: TCP Only The number of seconds to wait between reconnection attempts. A positive integer. Default: - 1
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = GelfLogDriverProps(address=address, compression_level=compression_level, compression_type=compression_type, tcp_max_reconnect=tcp_max_reconnect, tcp_reconnect_delay=tcp_reconnect_delay, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "gelf", [props])

    @jsii.member(jsii_name="journald")
    @classmethod
    def journald(cls, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to journald Logs.

        :param props: -
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = JournaldLogDriverProps(env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "journald", [props])

    @jsii.member(jsii_name="jsonFile")
    @classmethod
    def json_file(cls, *, compress: typing.Optional[bool]=None, max_file: typing.Optional[jsii.Number]=None, max_size: typing.Optional[str]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to json-file Logs.

        :param props: -
        :param compress: Toggles compression for rotated logs. Default: - false
        :param max_file: The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. Only effective when max-size is also set. A positive integer. Default: - 1
        :param max_size: The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g). Default: - -1 (unlimited)
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = JsonFileLogDriverProps(compress=compress, max_file=max_file, max_size=max_size, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "jsonFile", [props])

    @jsii.member(jsii_name="splunk")
    @classmethod
    def splunk(cls, *, token: aws_cdk.core.SecretValue, url: str, ca_name: typing.Optional[str]=None, ca_path: typing.Optional[str]=None, format: typing.Optional["SplunkLogFormat"]=None, gzip: typing.Optional[bool]=None, gzip_level: typing.Optional[jsii.Number]=None, index: typing.Optional[str]=None, insecure_skip_verify: typing.Optional[str]=None, source: typing.Optional[str]=None, source_type: typing.Optional[str]=None, verify_connection: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to splunk Logs.

        :param props: -
        :param token: Splunk HTTP Event Collector token.
        :param url: Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com.
        :param ca_name: Name to use for validating server certificate. Default: - The hostname of the splunk-url
        :param ca_path: Path to root certificate. Default: - caPath not set.
        :param format: Message format. Can be inline, json or raw. Default: - inline
        :param gzip: Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Default: - false
        :param gzip_level: Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Default: - -1 (Default Compression)
        :param index: Event index. Default: - index not set.
        :param insecure_skip_verify: Ignore server certificate validation. Default: - insecureSkipVerify not set.
        :param source: Event source. Default: - source not set.
        :param source_type: Event source type. Default: - sourceType not set.
        :param verify_connection: Verify on start, that docker can connect to Splunk server. Default: - true
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = SplunkLogDriverProps(token=token, url=url, ca_name=ca_name, ca_path=ca_path, format=format, gzip=gzip, gzip_level=gzip_level, index=index, insecure_skip_verify=insecure_skip_verify, source=source, source_type=source_type, verify_connection=verify_connection, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "splunk", [props])

    @jsii.member(jsii_name="syslog")
    @classmethod
    def syslog(cls, *, address: typing.Optional[str]=None, facility: typing.Optional[str]=None, format: typing.Optional[str]=None, tls_ca_cert: typing.Optional[str]=None, tls_cert: typing.Optional[str]=None, tls_key: typing.Optional[str]=None, tls_skip_verify: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to syslog Logs.

        :param props: -
        :param address: The address of an external syslog server. The URI specifier may be [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path. Default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.
        :param facility: The syslog facility to use. Can be the number or name for any valid syslog facility. See the syslog documentation: https://tools.ietf.org/html/rfc5424#section-6.2.1. Default: - facility not set
        :param format: The syslog message format to use. If not specified the local UNIX syslog format is used, without a specified hostname. Specify rfc3164 for the RFC-3164 compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro for RFC-5424 compatible format with microsecond timestamp resolution. Default: - format not set
        :param tls_ca_cert: The absolute path to the trust certificates signed by the CA. Ignored if the address protocol is not tcp+tls. Default: - tlsCaCert not set
        :param tls_cert: The absolute path to the TLS certificate file. Ignored if the address protocol is not tcp+tls. Default: - tlsCert not set
        :param tls_key: The absolute path to the TLS key file. Ignored if the address protocol is not tcp+tls. Default: - tlsKey not set
        :param tls_skip_verify: If set to true, TLS verification is skipped when connecting to the syslog daemon. Ignored if the address protocol is not tcp+tls. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = SyslogLogDriverProps(address=address, facility=facility, format=format, tls_ca_cert=tls_ca_cert, tls_cert=tls_cert, tls_key=tls_key, tls_skip_verify=tls_skip_verify, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "syslog", [props])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.MemoryUtilizationScalingProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'target_utilization_percent': 'targetUtilizationPercent'})
class MemoryUtilizationScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None, target_utilization_percent: jsii.Number):
        """The properties for enabling scaling based on memory utilization.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        :param target_utilization_percent: The target value for memory utilization across all tasks in the service.
        """
        self._values = {
            'target_utilization_percent': target_utilization_percent,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('policy_name')

    @property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default: - No scale in cooldown.
        """
        return self._values.get('scale_in_cooldown')

    @property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default: - No scale out cooldown.
        """
        return self._values.get('scale_out_cooldown')

    @property
    def target_utilization_percent(self) -> jsii.Number:
        """The target value for memory utilization across all tasks in the service."""
        return self._values.get('target_utilization_percent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MemoryUtilizationScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.MountPoint", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'read_only': 'readOnly', 'source_volume': 'sourceVolume'})
class MountPoint():
    def __init__(self, *, container_path: str, read_only: bool, source_volume: str):
        """The details of data volume mount points for a container.

        :param container_path: The path on the container to mount the host volume at.
        :param read_only: Specifies whether to give the container read-only access to the volume. If this value is true, the container has read-only access to the volume. If this value is false, then the container can write to the volume.
        :param source_volume: The name of the volume to mount. Must be a volume name referenced in the name parameter of task definition volume.
        """
        self._values = {
            'container_path': container_path,
            'read_only': read_only,
            'source_volume': source_volume,
        }

    @property
    def container_path(self) -> str:
        """The path on the container to mount the host volume at."""
        return self._values.get('container_path')

    @property
    def read_only(self) -> bool:
        """Specifies whether to give the container read-only access to the volume.

        If this value is true, the container has read-only access to the volume.
        If this value is false, then the container can write to the volume.
        """
        return self._values.get('read_only')

    @property
    def source_volume(self) -> str:
        """The name of the volume to mount.

        Must be a volume name referenced in the name parameter of task definition volume.
        """
        return self._values.get('source_volume')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MountPoint(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.NetworkMode")
class NetworkMode(enum.Enum):
    """The networking mode to use for the containers in the task."""
    NONE = "NONE"
    """The task's containers do not have external connectivity and port mappings can't be specified in the container definition."""
    BRIDGE = "BRIDGE"
    """The task utilizes Docker's built-in virtual network which runs inside each container instance."""
    AWS_VPC = "AWS_VPC"
    """The task is allocated an elastic network interface."""
    HOST = "HOST"
    """The task bypasses Docker's built-in virtual network and maps container ports directly to the EC2 instance's network interface directly.

    In this mode, you can't run multiple instantiations of the same task on a
    single container instance when port mappings are used.
    """
    NAT = "NAT"
    """The task utilizes NAT network mode required by Windows containers.

    This is the only supported network mode for Windows containers. For more information, see
    `Task Definition Parameters <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#network_mode>`_.
    """

class PlacementConstraint(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.PlacementConstraint"):
    """The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

    Tasks will only be placed on instances that match these rules.
    """
    @jsii.member(jsii_name="distinctInstances")
    @classmethod
    def distinct_instances(cls) -> "PlacementConstraint":
        """Use distinctInstance to ensure that each task in a particular group is running on a different container instance."""
        return jsii.sinvoke(cls, "distinctInstances", [])

    @jsii.member(jsii_name="memberOf")
    @classmethod
    def member_of(cls, *expressions: str) -> "PlacementConstraint":
        """Use memberOf to restrict the selection to a group of valid candidates specified by a query expression.

        Multiple expressions can be specified. For more information, see
        `Cluster Query Language <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html>`_.

        You can specify multiple expressions in one call. The tasks will only be placed on instances matching all expressions.

        :param expressions: -

        see
        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html
        """
        return jsii.sinvoke(cls, "memberOf", [*expressions])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List["CfnService.PlacementConstraintProperty"]:
        """Return the placement JSON."""
        return jsii.invoke(self, "toJson", [])


class PlacementStrategy(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.PlacementStrategy"):
    """The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

    Tasks will preferentially be placed on instances that match these rules.
    """
    @jsii.member(jsii_name="packedBy")
    @classmethod
    def packed_by(cls, resource: "BinPackResource") -> "PlacementStrategy":
        """Places tasks on the container instances with the least available capacity of the specified resource.

        :param resource: -
        """
        return jsii.sinvoke(cls, "packedBy", [resource])

    @jsii.member(jsii_name="packedByCpu")
    @classmethod
    def packed_by_cpu(cls) -> "PlacementStrategy":
        """Places tasks on container instances with the least available amount of CPU capacity.

        This minimizes the number of instances in use.
        """
        return jsii.sinvoke(cls, "packedByCpu", [])

    @jsii.member(jsii_name="packedByMemory")
    @classmethod
    def packed_by_memory(cls) -> "PlacementStrategy":
        """Places tasks on container instances with the least available amount of memory capacity.

        This minimizes the number of instances in use.
        """
        return jsii.sinvoke(cls, "packedByMemory", [])

    @jsii.member(jsii_name="randomly")
    @classmethod
    def randomly(cls) -> "PlacementStrategy":
        """Places tasks randomly."""
        return jsii.sinvoke(cls, "randomly", [])

    @jsii.member(jsii_name="spreadAcross")
    @classmethod
    def spread_across(cls, *fields: str) -> "PlacementStrategy":
        """Places tasks evenly based on the specified value.

        You can use one of the built-in attributes found on ``BuiltInAttributes``
        or supply your own custom instance attributes. If more than one attribute
        is supplied, spreading is done in order.

        :param fields: -

        default
        :default: attributes instanceId
        """
        return jsii.sinvoke(cls, "spreadAcross", [*fields])

    @jsii.member(jsii_name="spreadAcrossInstances")
    @classmethod
    def spread_across_instances(cls) -> "PlacementStrategy":
        """Places tasks evenly across all container instances in the cluster."""
        return jsii.sinvoke(cls, "spreadAcrossInstances", [])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List["CfnService.PlacementStrategyProperty"]:
        """Return the placement JSON."""
        return jsii.invoke(self, "toJson", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.PortMapping", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'host_port': 'hostPort', 'protocol': 'protocol'})
class PortMapping():
    def __init__(self, *, container_port: jsii.Number, host_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None):
        """Port mappings allow containers to access ports on the host container instance to send or receive traffic.

        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. For more information, see hostPort. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.
        :param host_port: The port number on the container instance to reserve for your container. If you are using containers in a task with the awsvpc or host network mode, the hostPort can either be left blank or set to the same value as the containerPort. If you are using containers in a task with the bridge network mode, you can specify a non-reserved host port for your container port mapping, or you can omit the hostPort (or set it to 0) while specifying a containerPort and your container automatically receives a port in the ephemeral port range for your container instance operating system and Docker version.
        :param protocol: The protocol used for the port mapping. Valid values are Protocol.TCP and Protocol.UDP. Default: TCP
        """
        self._values = {
            'container_port': container_port,
        }
        if host_port is not None: self._values["host_port"] = host_port
        if protocol is not None: self._values["protocol"] = protocol

    @property
    def container_port(self) -> jsii.Number:
        """The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        For more information, see hostPort.
        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.
        """
        return self._values.get('container_port')

    @property
    def host_port(self) -> typing.Optional[jsii.Number]:
        """The port number on the container instance to reserve for your container.

        If you are using containers in a task with the awsvpc or host network mode,
        the hostPort can either be left blank or set to the same value as the containerPort.

        If you are using containers in a task with the bridge network mode,
        you can specify a non-reserved host port for your container port mapping, or
        you can omit the hostPort (or set it to 0) while specifying a containerPort and
        your container automatically receives a port in the ephemeral port range for
        your container instance operating system and Docker version.
        """
        return self._values.get('host_port')

    @property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol used for the port mapping.

        Valid values are Protocol.TCP and Protocol.UDP.

        default
        :default: TCP
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PortMapping(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.PropagatedTagSource")
class PropagatedTagSource(enum.Enum):
    """Propagate tags from either service or task definition."""
    SERVICE = "SERVICE"
    """Propagate tags from service."""
    TASK_DEFINITION = "TASK_DEFINITION"
    """Propagate tags from task definition."""
    NONE = "NONE"
    """Do not propagate."""

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Protocol")
class Protocol(enum.Enum):
    """Network protocol."""
    TCP = "TCP"
    """TCP."""
    UDP = "UDP"
    """UDP."""

class ProxyConfiguration(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.ProxyConfiguration"):
    """The base class for proxy configurations."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ProxyConfigurationProxy

    def __init__(self) -> None:
        jsii.create(ProxyConfiguration, self, [])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, _scope: aws_cdk.core.Construct, _task_definition: "TaskDefinition") -> "CfnTaskDefinition.ProxyConfigurationProperty":
        """Called when the proxy configuration is configured on a task definition.

        :param _scope: -
        :param _task_definition: -
        """
        ...


class _ProxyConfigurationProxy(ProxyConfiguration):
    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _task_definition: "TaskDefinition") -> "CfnTaskDefinition.ProxyConfigurationProperty":
        """Called when the proxy configuration is configured on a task definition.

        :param _scope: -
        :param _task_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _task_definition])


class AppMeshProxyConfiguration(ProxyConfiguration, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.AppMeshProxyConfiguration"):
    """The class for App Mesh proxy configurations.

    For tasks using the EC2 launch type, the container instances require at least version 1.26.0 of the container agent and at least version
    1.26.0-1 of the ecs-init package to enable a proxy configuration. If your container instances are launched from the Amazon ECS-optimized
    AMI version 20190301 or later, then they contain the required versions of the container agent and ecs-init.
    For more information, see `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_.

    For tasks using the Fargate launch type, the task or service requires platform version 1.3.0 or later.
    """
    def __init__(self, *, container_name: str, properties: "AppMeshProxyConfigurationProps") -> None:
        """Constructs a new instance of the AppMeshProxyConfiguration class.

        :param props: -
        :param container_name: The name of the container that will serve as the App Mesh proxy.
        :param properties: The set of network configuration parameters to provide the Container Network Interface (CNI) plugin.
        """
        props = AppMeshProxyConfigurationConfigProps(container_name=container_name, properties=properties)

        jsii.create(AppMeshProxyConfiguration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _task_definition: "TaskDefinition") -> "CfnTaskDefinition.ProxyConfigurationProperty":
        """Called when the proxy configuration is configured on a task definition.

        :param _scope: -
        :param _task_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _task_definition])


class ProxyConfigurations(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.ProxyConfigurations"):
    """The base class for proxy configurations."""
    def __init__(self) -> None:
        jsii.create(ProxyConfigurations, self, [])

    @jsii.member(jsii_name="appMeshProxyConfiguration")
    @classmethod
    def app_mesh_proxy_configuration(cls, *, container_name: str, properties: "AppMeshProxyConfigurationProps") -> "ProxyConfiguration":
        """Constructs a new instance of the ProxyConfiguration class.

        :param props: -
        :param container_name: The name of the container that will serve as the App Mesh proxy.
        :param properties: The set of network configuration parameters to provide the Container Network Interface (CNI) plugin.
        """
        props = AppMeshProxyConfigurationConfigProps(container_name=container_name, properties=properties)

        return jsii.sinvoke(cls, "appMeshProxyConfiguration", [props])


class RepositoryImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.RepositoryImage"):
    """An image hosted in a public or private repository.

    For images hosted in Amazon ECR, see
    `EcrImage <https://docs.aws.amazon.com/AmazonECR/latest/userguide/images.html>`_.
    """
    def __init__(self, image_name: str, *, credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> None:
        """Constructs a new instance of the RepositoryImage class.

        :param image_name: -
        :param props: -
        :param credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.
        """
        props = RepositoryImageProps(credentials=credentials)

        jsii.create(RepositoryImage, self, [image_name, props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.RepositoryImageProps", jsii_struct_bases=[], name_mapping={'credentials': 'credentials'})
class RepositoryImageProps():
    def __init__(self, *, credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None):
        """The properties for an image hosted in a public or private repository.

        :param credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.
        """
        self._values = {
        }
        if credentials is not None: self._values["credentials"] = credentials

    @property
    def credentials(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret."""
        return self._values.get('credentials')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RepositoryImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.RequestCountScalingProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'requests_per_target': 'requestsPerTarget', 'target_group': 'targetGroup'})
class RequestCountScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None, requests_per_target: jsii.Number, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup):
        """The properties for enabling scaling based on Application Load Balancer (ALB) request counts.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        :param requests_per_target: The number of ALB requests per target.
        :param target_group: The ALB target group name.
        """
        self._values = {
            'requests_per_target': requests_per_target,
            'target_group': target_group,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('policy_name')

    @property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default: - No scale in cooldown.
        """
        return self._values.get('scale_in_cooldown')

    @property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default: - No scale out cooldown.
        """
        return self._values.get('scale_out_cooldown')

    @property
    def requests_per_target(self) -> jsii.Number:
        """The number of ALB requests per target."""
        return self._values.get('requests_per_target')

    @property
    def target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup:
        """The ALB target group name."""
        return self._values.get('target_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RequestCountScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScalableTaskCount(aws_cdk.aws_applicationautoscaling.BaseScalableAttribute, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.ScalableTaskCount"):
    """The scalable attribute representing task count."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: aws_cdk.aws_applicationautoscaling.ServiceNamespace, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> None:
        """Constructs a new instance of the ScalableTaskCount class.

        :param scope: -
        :param id: -
        :param props: -
        :param dimension: Scalable dimension of the attribute.
        :param resource_id: Resource ID of the attribute.
        :param role: Role to use for scaling.
        :param service_namespace: Service namespace of the scalable attribute.
        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1
        """
        props = ScalableTaskCountProps(dimension=dimension, resource_id=resource_id, role=role, service_namespace=service_namespace, max_capacity=max_capacity, min_capacity=min_capacity)

        jsii.create(ScalableTaskCount, self, [scope, id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target CPU utilization.

        :param id: -
        :param props: -
        :param target_utilization_percent: The target value for CPU utilization across all tasks in the service.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props = CpuUtilizationScalingProps(target_utilization_percent=target_utilization_percent, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMemoryUtilization")
    def scale_on_memory_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target memory utilization.

        :param id: -
        :param props: -
        :param target_utilization_percent: The target value for memory utilization across all tasks in the service.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props = MemoryUtilizationScalingProps(target_utilization_percent=target_utilization_percent, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleOnMemoryUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval], adjustment_type: typing.Optional[aws_cdk.aws_applicationautoscaling.AdjustmentType]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """Scales in or out based on a specified metric value.

        :param id: -
        :param props: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props = aws_cdk.aws_applicationautoscaling.BasicStepScalingPolicyProps(metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, min_adjustment_magnitude=min_adjustment_magnitude)

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(self, id: str, *, requests_per_target: jsii.Number, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target Application Load Balancer request count per target.

        :param id: -
        :param props: -
        :param requests_per_target: The number of ALB requests per target.
        :param target_group: The ALB target group name.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props = RequestCountScalingProps(requests_per_target=requests_per_target, target_group=target_group, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: aws_cdk.aws_applicationautoscaling.Schedule, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """Scales in or out based on a specified scheduled time.

        :param id: -
        :param props: -
        :param schedule: When to perform this action.
        :param end_time: When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        props = aws_cdk.aws_applicationautoscaling.ScalingSchedule(schedule=schedule, end_time=end_time, max_capacity=max_capacity, min_capacity=min_capacity, start_time=start_time)

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackCustomMetric")
    def scale_to_track_custom_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, target_value: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target on a custom metric.

        :param id: -
        :param props: -
        :param metric: The custom CloudWatch metric to track. The metric must represent utilization; that is, you will always get the following behavior: - metric > targetValue => scale out - metric < targetValue => scale in
        :param target_value: The target value for the custom CloudWatch metric.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props = TrackCustomMetricProps(metric=metric, target_value=target_value, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleToTrackCustomMetric", [id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ScalableTaskCountProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseScalableAttributeProps], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'dimension': 'dimension', 'resource_id': 'resourceId', 'role': 'role', 'service_namespace': 'serviceNamespace'})
class ScalableTaskCountProps(aws_cdk.aws_applicationautoscaling.BaseScalableAttributeProps):
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: aws_cdk.aws_applicationautoscaling.ServiceNamespace):
        """The properties of a scalable attribute representing task count.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1
        :param dimension: Scalable dimension of the attribute.
        :param resource_id: Resource ID of the attribute.
        :param role: Role to use for scaling.
        :param service_namespace: Service namespace of the scalable attribute.
        """
        self._values = {
            'max_capacity': max_capacity,
            'dimension': dimension,
            'resource_id': resource_id,
            'role': role,
            'service_namespace': service_namespace,
        }
        if min_capacity is not None: self._values["min_capacity"] = min_capacity

    @property
    def max_capacity(self) -> jsii.Number:
        """Maximum capacity to scale to."""
        return self._values.get('max_capacity')

    @property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum capacity to scale to.

        default
        :default: 1
        """
        return self._values.get('min_capacity')

    @property
    def dimension(self) -> str:
        """Scalable dimension of the attribute."""
        return self._values.get('dimension')

    @property
    def resource_id(self) -> str:
        """Resource ID of the attribute."""
        return self._values.get('resource_id')

    @property
    def role(self) -> aws_cdk.aws_iam.IRole:
        """Role to use for scaling."""
        return self._values.get('role')

    @property
    def service_namespace(self) -> aws_cdk.aws_applicationautoscaling.ServiceNamespace:
        """Service namespace of the scalable attribute."""
        return self._values.get('service_namespace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScalableTaskCountProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Scope")
class Scope(enum.Enum):
    """The scope for the Docker volume that determines its lifecycle. Docker volumes that are scoped to a task are automatically provisioned when the task starts and destroyed when the task stops. Docker volumes that are scoped as shared persist after the task stops."""
    TASK = "TASK"
    """Docker volumes that are scoped to a task are automatically provisioned when the task starts and destroyed when the task stops."""
    SHARED = "SHARED"
    """Docker volumes that are scoped as shared persist after the task stops."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ScratchSpace", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'name': 'name', 'read_only': 'readOnly', 'source_path': 'sourcePath'})
class ScratchSpace():
    def __init__(self, *, container_path: str, name: str, read_only: bool, source_path: str):
        """The temporary disk space mounted to the container.

        :param container_path: The path on the container to mount the scratch volume at.
        :param name: The name of the scratch volume to mount. Must be a volume name referenced in the name parameter of task definition volume.
        :param read_only: Specifies whether to give the container read-only access to the scratch volume. If this value is true, the container has read-only access to the scratch volume. If this value is false, then the container can write to the scratch volume.
        :param source_path: 
        """
        self._values = {
            'container_path': container_path,
            'name': name,
            'read_only': read_only,
            'source_path': source_path,
        }

    @property
    def container_path(self) -> str:
        """The path on the container to mount the scratch volume at."""
        return self._values.get('container_path')

    @property
    def name(self) -> str:
        """The name of the scratch volume to mount.

        Must be a volume name referenced in the name parameter of task definition volume.
        """
        return self._values.get('name')

    @property
    def read_only(self) -> bool:
        """Specifies whether to give the container read-only access to the scratch volume.

        If this value is true, the container has read-only access to the scratch volume.
        If this value is false, then the container can write to the scratch volume.
        """
        return self._values.get('read_only')

    @property
    def source_path(self) -> str:
        return self._values.get('source_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScratchSpace(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Secret(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.Secret"):
    """A secret environment variable."""
    @staticmethod
    def __jsii_proxy_class__():
        return _SecretProxy

    def __init__(self) -> None:
        jsii.create(Secret, self, [])

    @jsii.member(jsii_name="fromSecretsManager")
    @classmethod
    def from_secrets_manager(cls, secret: aws_cdk.aws_secretsmanager.ISecret) -> "Secret":
        """Creates a environment variable value from a secret stored in AWS Secrets Manager.

        :param secret: -
        """
        return jsii.sinvoke(cls, "fromSecretsManager", [secret])

    @jsii.member(jsii_name="fromSsmParameter")
    @classmethod
    def from_ssm_parameter(cls, parameter: aws_cdk.aws_ssm.IParameter) -> "Secret":
        """Creates an environment variable value from a parameter stored in AWS Systems Manager Parameter Store.

        :param parameter: -
        """
        return jsii.sinvoke(cls, "fromSsmParameter", [parameter])

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """
        :param grantee: -
        """
        ...

    @property
    @jsii.member(jsii_name="arn")
    @abc.abstractmethod
    def arn(self) -> str:
        ...


class _SecretProxy(Secret):
    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """
        :param grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @property
    @jsii.member(jsii_name="arn")
    def arn(self) -> str:
        return jsii.get(self, "arn")


class SplunkLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.SplunkLogDriver"):
    """A log driver that sends log information to splunk Logs."""
    def __init__(self, *, token: aws_cdk.core.SecretValue, url: str, ca_name: typing.Optional[str]=None, ca_path: typing.Optional[str]=None, format: typing.Optional["SplunkLogFormat"]=None, gzip: typing.Optional[bool]=None, gzip_level: typing.Optional[jsii.Number]=None, index: typing.Optional[str]=None, insecure_skip_verify: typing.Optional[str]=None, source: typing.Optional[str]=None, source_type: typing.Optional[str]=None, verify_connection: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the SplunkLogDriver class.

        :param props: the splunk log driver configuration options.
        :param token: Splunk HTTP Event Collector token.
        :param url: Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com.
        :param ca_name: Name to use for validating server certificate. Default: - The hostname of the splunk-url
        :param ca_path: Path to root certificate. Default: - caPath not set.
        :param format: Message format. Can be inline, json or raw. Default: - inline
        :param gzip: Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Default: - false
        :param gzip_level: Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Default: - -1 (Default Compression)
        :param index: Event index. Default: - index not set.
        :param insecure_skip_verify: Ignore server certificate validation. Default: - insecureSkipVerify not set.
        :param source: Event source. Default: - source not set.
        :param source_type: Event source type. Default: - sourceType not set.
        :param verify_connection: Verify on start, that docker can connect to Splunk server. Default: - true
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = SplunkLogDriverProps(token=token, url=url, ca_name=ca_name, ca_path=ca_path, format=format, gzip=gzip, gzip_level=gzip_level, index=index, insecure_skip_verify=insecure_skip_verify, source=source, source_type=source_type, verify_connection=verify_connection, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(SplunkLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.SplunkLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'token': 'token', 'url': 'url', 'ca_name': 'caName', 'ca_path': 'caPath', 'format': 'format', 'gzip': 'gzip', 'gzip_level': 'gzipLevel', 'index': 'index', 'insecure_skip_verify': 'insecureSkipVerify', 'source': 'source', 'source_type': 'sourceType', 'verify_connection': 'verifyConnection'})
class SplunkLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, token: aws_cdk.core.SecretValue, url: str, ca_name: typing.Optional[str]=None, ca_path: typing.Optional[str]=None, format: typing.Optional["SplunkLogFormat"]=None, gzip: typing.Optional[bool]=None, gzip_level: typing.Optional[jsii.Number]=None, index: typing.Optional[str]=None, insecure_skip_verify: typing.Optional[str]=None, source: typing.Optional[str]=None, source_type: typing.Optional[str]=None, verify_connection: typing.Optional[bool]=None):
        """Specifies the splunk log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/splunk/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param token: Splunk HTTP Event Collector token.
        :param url: Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com.
        :param ca_name: Name to use for validating server certificate. Default: - The hostname of the splunk-url
        :param ca_path: Path to root certificate. Default: - caPath not set.
        :param format: Message format. Can be inline, json or raw. Default: - inline
        :param gzip: Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Default: - false
        :param gzip_level: Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Default: - -1 (Default Compression)
        :param index: Event index. Default: - index not set.
        :param insecure_skip_verify: Ignore server certificate validation. Default: - insecureSkipVerify not set.
        :param source: Event source. Default: - source not set.
        :param source_type: Event source type. Default: - sourceType not set.
        :param verify_connection: Verify on start, that docker can connect to Splunk server. Default: - true
        """
        self._values = {
            'token': token,
            'url': url,
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if ca_name is not None: self._values["ca_name"] = ca_name
        if ca_path is not None: self._values["ca_path"] = ca_path
        if format is not None: self._values["format"] = format
        if gzip is not None: self._values["gzip"] = gzip
        if gzip_level is not None: self._values["gzip_level"] = gzip_level
        if index is not None: self._values["index"] = index
        if insecure_skip_verify is not None: self._values["insecure_skip_verify"] = insecure_skip_verify
        if source is not None: self._values["source"] = source
        if source_type is not None: self._values["source_type"] = source_type
        if verify_connection is not None: self._values["verify_connection"] = verify_connection

    @property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env
        """
        return self._values.get('env')

    @property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex
        """
        return self._values.get('env_regex')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels
        """
        return self._values.get('labels')

    @property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID
        """
        return self._values.get('tag')

    @property
    def token(self) -> aws_cdk.core.SecretValue:
        """Splunk HTTP Event Collector token."""
        return self._values.get('token')

    @property
    def url(self) -> str:
        """Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com."""
        return self._values.get('url')

    @property
    def ca_name(self) -> typing.Optional[str]:
        """Name to use for validating server certificate.

        default
        :default: - The hostname of the splunk-url
        """
        return self._values.get('ca_name')

    @property
    def ca_path(self) -> typing.Optional[str]:
        """Path to root certificate.

        default
        :default: - caPath not set.
        """
        return self._values.get('ca_path')

    @property
    def format(self) -> typing.Optional["SplunkLogFormat"]:
        """Message format.

        Can be inline, json or raw.

        default
        :default: - inline
        """
        return self._values.get('format')

    @property
    def gzip(self) -> typing.Optional[bool]:
        """Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance.

        default
        :default: - false
        """
        return self._values.get('gzip')

    @property
    def gzip_level(self) -> typing.Optional[jsii.Number]:
        """Set compression level for gzip.

        Valid values are -1 (default), 0 (no compression),
        1 (best speed) ... 9 (best compression).

        default
        :default: - -1 (Default Compression)
        """
        return self._values.get('gzip_level')

    @property
    def index(self) -> typing.Optional[str]:
        """Event index.

        default
        :default: - index not set.
        """
        return self._values.get('index')

    @property
    def insecure_skip_verify(self) -> typing.Optional[str]:
        """Ignore server certificate validation.

        default
        :default: - insecureSkipVerify not set.
        """
        return self._values.get('insecure_skip_verify')

    @property
    def source(self) -> typing.Optional[str]:
        """Event source.

        default
        :default: - source not set.
        """
        return self._values.get('source')

    @property
    def source_type(self) -> typing.Optional[str]:
        """Event source type.

        default
        :default: - sourceType not set.
        """
        return self._values.get('source_type')

    @property
    def verify_connection(self) -> typing.Optional[bool]:
        """Verify on start, that docker can connect to Splunk server.

        default
        :default: - true
        """
        return self._values.get('verify_connection')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SplunkLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.SplunkLogFormat")
class SplunkLogFormat(enum.Enum):
    """Log Message Format."""
    INLINE = "INLINE"
    JSON = "JSON"
    RAW = "RAW"

class SyslogLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.SyslogLogDriver"):
    """A log driver that sends log information to syslog Logs."""
    def __init__(self, *, address: typing.Optional[str]=None, facility: typing.Optional[str]=None, format: typing.Optional[str]=None, tls_ca_cert: typing.Optional[str]=None, tls_cert: typing.Optional[str]=None, tls_key: typing.Optional[str]=None, tls_skip_verify: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the SyslogLogDriver class.

        :param props: the syslog log driver configuration options.
        :param address: The address of an external syslog server. The URI specifier may be [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path. Default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.
        :param facility: The syslog facility to use. Can be the number or name for any valid syslog facility. See the syslog documentation: https://tools.ietf.org/html/rfc5424#section-6.2.1. Default: - facility not set
        :param format: The syslog message format to use. If not specified the local UNIX syslog format is used, without a specified hostname. Specify rfc3164 for the RFC-3164 compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro for RFC-5424 compatible format with microsecond timestamp resolution. Default: - format not set
        :param tls_ca_cert: The absolute path to the trust certificates signed by the CA. Ignored if the address protocol is not tcp+tls. Default: - tlsCaCert not set
        :param tls_cert: The absolute path to the TLS certificate file. Ignored if the address protocol is not tcp+tls. Default: - tlsCert not set
        :param tls_key: The absolute path to the TLS key file. Ignored if the address protocol is not tcp+tls. Default: - tlsKey not set
        :param tls_skip_verify: If set to true, TLS verification is skipped when connecting to the syslog daemon. Ignored if the address protocol is not tcp+tls. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        """
        props = SyslogLogDriverProps(address=address, facility=facility, format=format, tls_ca_cert=tls_ca_cert, tls_cert=tls_cert, tls_key=tls_key, tls_skip_verify=tls_skip_verify, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(SyslogLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.SyslogLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'address': 'address', 'facility': 'facility', 'format': 'format', 'tls_ca_cert': 'tlsCaCert', 'tls_cert': 'tlsCert', 'tls_key': 'tlsKey', 'tls_skip_verify': 'tlsSkipVerify'})
class SyslogLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, address: typing.Optional[str]=None, facility: typing.Optional[str]=None, format: typing.Optional[str]=None, tls_ca_cert: typing.Optional[str]=None, tls_cert: typing.Optional[str]=None, tls_key: typing.Optional[str]=None, tls_skip_verify: typing.Optional[bool]=None):
        """Specifies the syslog log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/syslog/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param address: The address of an external syslog server. The URI specifier may be [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path. Default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.
        :param facility: The syslog facility to use. Can be the number or name for any valid syslog facility. See the syslog documentation: https://tools.ietf.org/html/rfc5424#section-6.2.1. Default: - facility not set
        :param format: The syslog message format to use. If not specified the local UNIX syslog format is used, without a specified hostname. Specify rfc3164 for the RFC-3164 compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro for RFC-5424 compatible format with microsecond timestamp resolution. Default: - format not set
        :param tls_ca_cert: The absolute path to the trust certificates signed by the CA. Ignored if the address protocol is not tcp+tls. Default: - tlsCaCert not set
        :param tls_cert: The absolute path to the TLS certificate file. Ignored if the address protocol is not tcp+tls. Default: - tlsCert not set
        :param tls_key: The absolute path to the TLS key file. Ignored if the address protocol is not tcp+tls. Default: - tlsKey not set
        :param tls_skip_verify: If set to true, TLS verification is skipped when connecting to the syslog daemon. Ignored if the address protocol is not tcp+tls. Default: - false
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if address is not None: self._values["address"] = address
        if facility is not None: self._values["facility"] = facility
        if format is not None: self._values["format"] = format
        if tls_ca_cert is not None: self._values["tls_ca_cert"] = tls_ca_cert
        if tls_cert is not None: self._values["tls_cert"] = tls_cert
        if tls_key is not None: self._values["tls_key"] = tls_key
        if tls_skip_verify is not None: self._values["tls_skip_verify"] = tls_skip_verify

    @property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env
        """
        return self._values.get('env')

    @property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex
        """
        return self._values.get('env_regex')

    @property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels
        """
        return self._values.get('labels')

    @property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID
        """
        return self._values.get('tag')

    @property
    def address(self) -> typing.Optional[str]:
        """The address of an external syslog server.

        The URI specifier may be
        [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path.

        default
        :default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.
        """
        return self._values.get('address')

    @property
    def facility(self) -> typing.Optional[str]:
        """The syslog facility to use.

        Can be the number or name for any valid
        syslog facility. See the syslog documentation:
        https://tools.ietf.org/html/rfc5424#section-6.2.1.

        default
        :default: - facility not set
        """
        return self._values.get('facility')

    @property
    def format(self) -> typing.Optional[str]:
        """The syslog message format to use.

        If not specified the local UNIX syslog
        format is used, without a specified hostname. Specify rfc3164 for the RFC-3164
        compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro
        for RFC-5424 compatible format with microsecond timestamp resolution.

        default
        :default: - format not set
        """
        return self._values.get('format')

    @property
    def tls_ca_cert(self) -> typing.Optional[str]:
        """The absolute path to the trust certificates signed by the CA.

        Ignored
        if the address protocol is not tcp+tls.

        default
        :default: - tlsCaCert not set
        """
        return self._values.get('tls_ca_cert')

    @property
    def tls_cert(self) -> typing.Optional[str]:
        """The absolute path to the TLS certificate file.

        Ignored if the address
        protocol is not tcp+tls.

        default
        :default: - tlsCert not set
        """
        return self._values.get('tls_cert')

    @property
    def tls_key(self) -> typing.Optional[str]:
        """The absolute path to the TLS key file.

        Ignored if the address protocol
        is not tcp+tls.

        default
        :default: - tlsKey not set
        """
        return self._values.get('tls_key')

    @property
    def tls_skip_verify(self) -> typing.Optional[bool]:
        """If set to true, TLS verification is skipped when connecting to the syslog daemon.

        Ignored if the address protocol is not tcp+tls.

        default
        :default: - false
        """
        return self._values.get('tls_skip_verify')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SyslogLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ITaskDefinition)
class TaskDefinition(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.TaskDefinition"):
    """The base class for all task definitions."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, compatibility: "Compatibility", cpu: typing.Optional[str]=None, memory_mib: typing.Optional[str]=None, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the TaskDefinition class.

        :param scope: -
        :param id: -
        :param props: -
        :param compatibility: The task launch type compatiblity requirement.
        :param cpu: The number of cpu units used by the task. If you are using the EC2 launch type, this field is optional and any value can be used. If you are using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: - CPU units are not specified.
        :param memory_mib: The amount (in MiB) of memory used by the task. If using the EC2 launch type, this field is optional and any value can be used. If using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: - Memory used by task is not specified.
        :param network_mode: The networking mode to use for the containers in the task. On Fargate, the only supported networking mode is AwsVpc. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param placement_constraints: The placement constraints to use for tasks in the service. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Not supported in Fargate. Default: - No placement constraints.
        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        """
        props = TaskDefinitionProps(compatibility=compatibility, cpu=cpu, memory_mib=memory_mib, network_mode=network_mode, placement_constraints=placement_constraints, execution_role=execution_role, family=family, proxy_configuration=proxy_configuration, task_role=task_role, volumes=volumes)

        jsii.create(TaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromTaskDefinitionArn")
    @classmethod
    def from_task_definition_arn(cls, scope: aws_cdk.core.Construct, id: str, task_definition_arn: str) -> "ITaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        The task will have a compatibility of EC2+Fargate.

        :param scope: -
        :param id: -
        :param task_definition_arn: -
        """
        return jsii.sinvoke(cls, "fromTaskDefinitionArn", [scope, id, task_definition_arn])

    @jsii.member(jsii_name="addContainer")
    def add_container(self, id: str, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str,"Secret"]]=None, start_timeout: typing.Optional[aws_cdk.core.Duration]=None, stop_timeout: typing.Optional[aws_cdk.core.Duration]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> "ContainerDefinition":
        """Adds a new container to the task definition.

        :param id: -
        :param props: -
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux paramters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /
        """
        props = ContainerDefinitionOptions(image=image, command=command, cpu=cpu, disable_networking=disable_networking, dns_search_domains=dns_search_domains, dns_servers=dns_servers, docker_labels=docker_labels, docker_security_options=docker_security_options, entry_point=entry_point, environment=environment, essential=essential, extra_hosts=extra_hosts, gpu_count=gpu_count, health_check=health_check, hostname=hostname, linux_parameters=linux_parameters, logging=logging, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, privileged=privileged, readonly_root_filesystem=readonly_root_filesystem, secrets=secrets, start_timeout=start_timeout, stop_timeout=stop_timeout, user=user, working_directory=working_directory)

        return jsii.invoke(self, "addContainer", [id, props])

    @jsii.member(jsii_name="addExtension")
    def add_extension(self, extension: "ITaskDefinitionExtension") -> None:
        """Adds the specified extention to the task definition.

        Extension can be used to apply a packaged modification to
        a task definition.

        :param extension: -
        """
        return jsii.invoke(self, "addExtension", [extension])

    @jsii.member(jsii_name="addPlacementConstraint")
    def add_placement_constraint(self, constraint: "PlacementConstraint") -> None:
        """Adds the specified placement constraint to the task definition.

        :param constraint: -
        """
        return jsii.invoke(self, "addPlacementConstraint", [constraint])

    @jsii.member(jsii_name="addToExecutionRolePolicy")
    def add_to_execution_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a policy statement to the task execution IAM role.

        :param statement: -
        """
        return jsii.invoke(self, "addToExecutionRolePolicy", [statement])

    @jsii.member(jsii_name="addToTaskRolePolicy")
    def add_to_task_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a policy statement to the task IAM role.

        :param statement: -
        """
        return jsii.invoke(self, "addToTaskRolePolicy", [statement])

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, *, name: str, docker_volume_configuration: typing.Optional["DockerVolumeConfiguration"]=None, host: typing.Optional["Host"]=None) -> None:
        """Adds a volume to the task definition.

        :param volume: -
        :param name: The name of the volume. Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed. This name is referenced in the sourceVolume parameter of container definition mountPoints.
        :param docker_volume_configuration: This property is specified when you are using Docker volumes. Docker volumes are only supported when you are using the EC2 launch type. Windows containers only support the use of the local driver. To use bind mounts, specify a host instead.
        :param host: This property is specified when you are using bind mount host volumes. Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types. The contents of the host parameter determine whether your bind mount host volume persists on the host container instance and where it is stored. If the host parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data is not guaranteed to persist after the containers associated with it stop running.
        """
        volume = Volume(name=name, docker_volume_configuration=docker_volume_configuration, host=host)

        return jsii.invoke(self, "addVolume", [volume])

    @jsii.member(jsii_name="obtainExecutionRole")
    def obtain_execution_role(self) -> aws_cdk.aws_iam.IRole:
        """Creates the task execution IAM role if it doesn't already exist."""
        return jsii.invoke(self, "obtainExecutionRole", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validates the task definition."""
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """The task launch type compatiblity requirement."""
        return jsii.get(self, "compatibility")

    @property
    @jsii.member(jsii_name="containers")
    def _containers(self) -> typing.List["ContainerDefinition"]:
        """The container definitions."""
        return jsii.get(self, "containers")

    @property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """The name of a family that this task definition is registered to. A family groups multiple versions of a task definition."""
        return jsii.get(self, "family")

    @property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster."""
        return jsii.get(self, "isEc2Compatible")

    @property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster."""
        return jsii.get(self, "isFargateCompatible")

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        """The networking mode to use for the containers in the task."""
        return jsii.get(self, "networkMode")

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """The full Amazon Resource Name (ARN) of the task definition.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "taskDefinitionArn")

    @property
    @jsii.member(jsii_name="taskRole")
    def task_role(self) -> aws_cdk.aws_iam.IRole:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf."""
        return jsii.get(self, "taskRole")

    @property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role for this task definition."""
        return jsii.get(self, "executionRole")

    @property
    @jsii.member(jsii_name="defaultContainer")
    def default_container(self) -> typing.Optional["ContainerDefinition"]:
        """Default container for this task.

        Load balancers will send traffic to this container. The first
        essential container that is added to this task will become the default
        container.
        """
        return jsii.get(self, "defaultContainer")

    @default_container.setter
    def default_container(self, value: typing.Optional["ContainerDefinition"]):
        return jsii.set(self, "defaultContainer", value)


@jsii.implements(IEc2TaskDefinition)
class Ec2TaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Ec2TaskDefinition"):
    """The details of a task definition run on an EC2 cluster.

    resource:
    :resource:: AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the Ec2TaskDefinition class.

        :param scope: -
        :param id: -
        :param props: -
        :param network_mode: The Docker networking mode to use for the containers in the task. The valid values are none, bridge, awsvpc, and host. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param placement_constraints: An array of placement constraint objects to use for the task. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Default: - No placement constraints.
        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        """
        props = Ec2TaskDefinitionProps(network_mode=network_mode, placement_constraints=placement_constraints, execution_role=execution_role, family=family, proxy_configuration=proxy_configuration, task_role=task_role, volumes=volumes)

        jsii.create(Ec2TaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2TaskDefinitionArn")
    @classmethod
    def from_ec2_task_definition_arn(cls, scope: aws_cdk.core.Construct, id: str, ec2_task_definition_arn: str) -> "IEc2TaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        :param scope: -
        :param id: -
        :param ec2_task_definition_arn: -
        """
        return jsii.sinvoke(cls, "fromEc2TaskDefinitionArn", [scope, id, ec2_task_definition_arn])


@jsii.implements(IFargateTaskDefinition)
class FargateTaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.FargateTaskDefinition"):
    """The details of a task definition run on a Fargate cluster.

    resource:
    :resource:: AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the FargateTaskDefinition class.

        :param scope: -
        :param id: -
        :param props: -
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 512
        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        """
        props = FargateTaskDefinitionProps(cpu=cpu, memory_limit_mib=memory_limit_mib, execution_role=execution_role, family=family, proxy_configuration=proxy_configuration, task_role=task_role, volumes=volumes)

        jsii.create(FargateTaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromFargateTaskDefinitionArn")
    @classmethod
    def from_fargate_task_definition_arn(cls, scope: aws_cdk.core.Construct, id: str, fargate_task_definition_arn: str) -> "IFargateTaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        :param scope: -
        :param id: -
        :param fargate_task_definition_arn: -
        """
        return jsii.sinvoke(cls, "fromFargateTaskDefinitionArn", [scope, id, fargate_task_definition_arn])

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        """The Docker networking mode to use for the containers in the task.

        Fargate tasks require the awsvpc network mode.
        """
        return jsii.get(self, "networkMode")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.TaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes', 'compatibility': 'compatibility', 'cpu': 'cpu', 'memory_mib': 'memoryMiB', 'network_mode': 'networkMode', 'placement_constraints': 'placementConstraints'})
class TaskDefinitionProps(CommonTaskDefinitionProps):
    def __init__(self, *, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None, compatibility: "Compatibility", cpu: typing.Optional[str]=None, memory_mib: typing.Optional[str]=None, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None):
        """The properties for task definitions.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        :param compatibility: The task launch type compatiblity requirement.
        :param cpu: The number of cpu units used by the task. If you are using the EC2 launch type, this field is optional and any value can be used. If you are using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: - CPU units are not specified.
        :param memory_mib: The amount (in MiB) of memory used by the task. If using the EC2 launch type, this field is optional and any value can be used. If using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: - Memory used by task is not specified.
        :param network_mode: The networking mode to use for the containers in the task. On Fargate, the only supported networking mode is AwsVpc. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param placement_constraints: The placement constraints to use for tasks in the service. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Not supported in Fargate. Default: - No placement constraints.
        """
        self._values = {
            'compatibility': compatibility,
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes
        if cpu is not None: self._values["cpu"] = cpu
        if memory_mib is not None: self._values["memory_mib"] = memory_mib
        if network_mode is not None: self._values["network_mode"] = network_mode
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints

    @property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.
        """
        return self._values.get('execution_role')

    @property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.
        """
        return self._values.get('proxy_configuration')

    @property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    @property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.
        """
        return self._values.get('volumes')

    @property
    def compatibility(self) -> "Compatibility":
        """The task launch type compatiblity requirement."""
        return self._values.get('compatibility')

    @property
    def cpu(self) -> typing.Optional[str]:
        """The number of cpu units used by the task.

        If you are using the EC2 launch type, this field is optional and any value can be used.
        If you are using the Fargate launch type, this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)
        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)
        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)
        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)
        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        default
        :default: - CPU units are not specified.
        """
        return self._values.get('cpu')

    @property
    def memory_mib(self) -> typing.Optional[str]:
        """The amount (in MiB) of memory used by the task.

        If using the EC2 launch type, this field is optional and any value can be used.
        If using the Fargate launch type, this field is required and you must use one of the following values,
        which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)
        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)
        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)
        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)
        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        default
        :default: - Memory used by task is not specified.
        """
        return self._values.get('memory_mib')

    @property
    def network_mode(self) -> typing.Optional["NetworkMode"]:
        """The networking mode to use for the containers in the task.

        On Fargate, the only supported networking mode is AwsVpc.

        default
        :default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        """
        return self._values.get('network_mode')

    @property
    def placement_constraints(self) -> typing.Optional[typing.List["PlacementConstraint"]]:
        """The placement constraints to use for tasks in the service.

        You can specify a maximum of 10 constraints per task (this limit includes
        constraints in the task definition and those specified at run time).

        Not supported in Fargate.

        default
        :default: - No placement constraints.
        """
        return self._values.get('placement_constraints')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Tmpfs", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'size': 'size', 'mount_options': 'mountOptions'})
class Tmpfs():
    def __init__(self, *, container_path: str, size: jsii.Number, mount_options: typing.Optional[typing.List["TmpfsMountOption"]]=None):
        """The details of a tmpfs mount for a container.

        :param container_path: The absolute file path where the tmpfs volume is to be mounted.
        :param size: The size (in MiB) of the tmpfs volume.
        :param mount_options: The list of tmpfs volume mount options. For more information, see `TmpfsMountOptions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html>`_.
        """
        self._values = {
            'container_path': container_path,
            'size': size,
        }
        if mount_options is not None: self._values["mount_options"] = mount_options

    @property
    def container_path(self) -> str:
        """The absolute file path where the tmpfs volume is to be mounted."""
        return self._values.get('container_path')

    @property
    def size(self) -> jsii.Number:
        """The size (in MiB) of the tmpfs volume."""
        return self._values.get('size')

    @property
    def mount_options(self) -> typing.Optional[typing.List["TmpfsMountOption"]]:
        """The list of tmpfs volume mount options.

        For more information, see
        `TmpfsMountOptions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html>`_.
        """
        return self._values.get('mount_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Tmpfs(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.TmpfsMountOption")
class TmpfsMountOption(enum.Enum):
    """The supported options for a tmpfs mount for a container."""
    DEFAULTS = "DEFAULTS"
    RO = "RO"
    RW = "RW"
    SUID = "SUID"
    NOSUID = "NOSUID"
    DEV = "DEV"
    NODEV = "NODEV"
    EXEC = "EXEC"
    NOEXEC = "NOEXEC"
    SYNC = "SYNC"
    ASYNC = "ASYNC"
    DIRSYNC = "DIRSYNC"
    REMOUNT = "REMOUNT"
    MAND = "MAND"
    NOMAND = "NOMAND"
    ATIME = "ATIME"
    NOATIME = "NOATIME"
    DIRATIME = "DIRATIME"
    NODIRATIME = "NODIRATIME"
    BIND = "BIND"
    RBIND = "RBIND"
    UNBINDABLE = "UNBINDABLE"
    RUNBINDABLE = "RUNBINDABLE"
    PRIVATE = "PRIVATE"
    RPRIVATE = "RPRIVATE"
    SHARED = "SHARED"
    RSHARED = "RSHARED"
    SLAVE = "SLAVE"
    RSLAVE = "RSLAVE"
    RELATIME = "RELATIME"
    NORELATIME = "NORELATIME"
    STRICTATIME = "STRICTATIME"
    NOSTRICTATIME = "NOSTRICTATIME"
    MODE = "MODE"
    UID = "UID"
    GID = "GID"
    NR_INODES = "NR_INODES"
    NR_BLOCKS = "NR_BLOCKS"
    MPOL = "MPOL"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.TrackCustomMetricProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'metric': 'metric', 'target_value': 'targetValue'})
class TrackCustomMetricProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None, metric: aws_cdk.aws_cloudwatch.IMetric, target_value: jsii.Number):
        """The properties for enabling target tracking scaling based on a custom CloudWatch metric.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        :param metric: The custom CloudWatch metric to track. The metric must represent utilization; that is, you will always get the following behavior: - metric > targetValue => scale out - metric < targetValue => scale in
        :param target_value: The target value for the custom CloudWatch metric.
        """
        self._values = {
            'metric': metric,
            'target_value': target_value,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false
        """
        return self._values.get('disable_scale_in')

    @property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('policy_name')

    @property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default: - No scale in cooldown.
        """
        return self._values.get('scale_in_cooldown')

    @property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default: - No scale out cooldown.
        """
        return self._values.get('scale_out_cooldown')

    @property
    def metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """The custom CloudWatch metric to track.

        The metric must represent utilization; that is, you will always get the following behavior:

        - metric > targetValue => scale out
        - metric < targetValue => scale in
        """
        return self._values.get('metric')

    @property
    def target_value(self) -> jsii.Number:
        """The target value for the custom CloudWatch metric."""
        return self._values.get('target_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TrackCustomMetricProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ulimit", jsii_struct_bases=[], name_mapping={'hard_limit': 'hardLimit', 'name': 'name', 'soft_limit': 'softLimit'})
class Ulimit():
    def __init__(self, *, hard_limit: jsii.Number, name: "UlimitName", soft_limit: jsii.Number):
        """The ulimit settings to pass to the container.

        NOTE: Does not work for Windows containers.

        :param hard_limit: The hard limit for the ulimit type.
        :param name: The type of the ulimit. For more information, see `UlimitName <https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-ecs/ulimitname.html#aws_ecs_UlimitName>`_.
        :param soft_limit: The soft limit for the ulimit type.
        """
        self._values = {
            'hard_limit': hard_limit,
            'name': name,
            'soft_limit': soft_limit,
        }

    @property
    def hard_limit(self) -> jsii.Number:
        """The hard limit for the ulimit type."""
        return self._values.get('hard_limit')

    @property
    def name(self) -> "UlimitName":
        """The type of the ulimit.

        For more information, see `UlimitName <https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-ecs/ulimitname.html#aws_ecs_UlimitName>`_.
        """
        return self._values.get('name')

    @property
    def soft_limit(self) -> jsii.Number:
        """The soft limit for the ulimit type."""
        return self._values.get('soft_limit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ulimit(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.UlimitName")
class UlimitName(enum.Enum):
    """Type of resource to set a limit on."""
    CORE = "CORE"
    CPU = "CPU"
    DATA = "DATA"
    FSIZE = "FSIZE"
    LOCKS = "LOCKS"
    MEMLOCK = "MEMLOCK"
    MSGQUEUE = "MSGQUEUE"
    NICE = "NICE"
    NOFILE = "NOFILE"
    NPROC = "NPROC"
    RSS = "RSS"
    RTPRIO = "RTPRIO"
    RTTIME = "RTTIME"
    SIGPENDING = "SIGPENDING"
    STACK = "STACK"

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Volume", jsii_struct_bases=[], name_mapping={'name': 'name', 'docker_volume_configuration': 'dockerVolumeConfiguration', 'host': 'host'})
class Volume():
    def __init__(self, *, name: str, docker_volume_configuration: typing.Optional["DockerVolumeConfiguration"]=None, host: typing.Optional["Host"]=None):
        """A data volume used in a task definition.

        For tasks that use a Docker volume, specify a DockerVolumeConfiguration.
        For tasks that use a bind mount host volume, specify a host and optional sourcePath.

        For more information, see `Using Data Volumes in Tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html>`_.

        :param name: The name of the volume. Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed. This name is referenced in the sourceVolume parameter of container definition mountPoints.
        :param docker_volume_configuration: This property is specified when you are using Docker volumes. Docker volumes are only supported when you are using the EC2 launch type. Windows containers only support the use of the local driver. To use bind mounts, specify a host instead.
        :param host: This property is specified when you are using bind mount host volumes. Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types. The contents of the host parameter determine whether your bind mount host volume persists on the host container instance and where it is stored. If the host parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data is not guaranteed to persist after the containers associated with it stop running.
        """
        if isinstance(docker_volume_configuration, dict): docker_volume_configuration = DockerVolumeConfiguration(**docker_volume_configuration)
        if isinstance(host, dict): host = Host(**host)
        self._values = {
            'name': name,
        }
        if docker_volume_configuration is not None: self._values["docker_volume_configuration"] = docker_volume_configuration
        if host is not None: self._values["host"] = host

    @property
    def name(self) -> str:
        """The name of the volume.

        Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed.
        This name is referenced in the sourceVolume parameter of container definition mountPoints.
        """
        return self._values.get('name')

    @property
    def docker_volume_configuration(self) -> typing.Optional["DockerVolumeConfiguration"]:
        """This property is specified when you are using Docker volumes.

        Docker volumes are only supported when you are using the EC2 launch type.
        Windows containers only support the use of the local driver.
        To use bind mounts, specify a host instead.
        """
        return self._values.get('docker_volume_configuration')

    @property
    def host(self) -> typing.Optional["Host"]:
        """This property is specified when you are using bind mount host volumes.

        Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types.
        The contents of the host parameter determine whether your bind mount host volume persists on the
        host container instance and where it is stored. If the host parameter is empty, then the Docker
        daemon assigns a host path for your data volume. However, the data is not guaranteed to persist
        after the containers associated with it stop running.
        """
        return self._values.get('host')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Volume(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.VolumeFrom", jsii_struct_bases=[], name_mapping={'read_only': 'readOnly', 'source_container': 'sourceContainer'})
class VolumeFrom():
    def __init__(self, *, read_only: bool, source_container: str):
        """The details on a data volume from another container in the same task definition.

        :param read_only: Specifies whether the container has read-only access to the volume. If this value is true, the container has read-only access to the volume. If this value is false, then the container can write to the volume.
        :param source_container: The name of another container within the same task definition from which to mount volumes.
        """
        self._values = {
            'read_only': read_only,
            'source_container': source_container,
        }

    @property
    def read_only(self) -> bool:
        """Specifies whether the container has read-only access to the volume.

        If this value is true, the container has read-only access to the volume.
        If this value is false, then the container can write to the volume.
        """
        return self._values.get('read_only')

    @property
    def source_container(self) -> str:
        """The name of another container within the same task definition from which to mount volumes."""
        return self._values.get('source_container')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VolumeFrom(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.WindowsOptimizedVersion")
class WindowsOptimizedVersion(enum.Enum):
    """ECS-optimized Windows version list."""
    SERVER_2019 = "SERVER_2019"
    SERVER_2016 = "SERVER_2016"

__all__ = ["AddAutoScalingGroupCapacityOptions", "AddCapacityOptions", "AmiHardwareType", "AppMeshProxyConfiguration", "AppMeshProxyConfigurationConfigProps", "AppMeshProxyConfigurationProps", "AssetImage", "AssetImageProps", "AwsLogDriver", "AwsLogDriverProps", "BaseLogDriverProps", "BaseService", "BaseServiceOptions", "BaseServiceProps", "BinPackResource", "BuiltInAttributes", "Capability", "CfnCluster", "CfnClusterProps", "CfnService", "CfnServiceProps", "CfnTaskDefinition", "CfnTaskDefinitionProps", "CloudMapNamespaceOptions", "CloudMapOptions", "Cluster", "ClusterAttributes", "ClusterProps", "CommonTaskDefinitionProps", "Compatibility", "ContainerDefinition", "ContainerDefinitionOptions", "ContainerDefinitionProps", "ContainerDependency", "ContainerDependencyCondition", "ContainerImage", "ContainerImageConfig", "CpuUtilizationScalingProps", "Device", "DevicePermission", "DockerVolumeConfiguration", "Ec2Service", "Ec2ServiceProps", "Ec2TaskDefinition", "Ec2TaskDefinitionProps", "EcrImage", "EcsOptimizedAmi", "EcsOptimizedAmiProps", "EcsOptimizedImage", "EcsTarget", "FargatePlatformVersion", "FargateService", "FargateServiceProps", "FargateTaskDefinition", "FargateTaskDefinitionProps", "FluentdLogDriver", "FluentdLogDriverProps", "GelfCompressionType", "GelfLogDriver", "GelfLogDriverProps", "HealthCheck", "Host", "ICluster", "IEc2Service", "IEc2TaskDefinition", "IEcsLoadBalancerTarget", "IFargateService", "IFargateTaskDefinition", "IService", "ITaskDefinition", "ITaskDefinitionExtension", "JournaldLogDriver", "JournaldLogDriverProps", "JsonFileLogDriver", "JsonFileLogDriverProps", "LaunchType", "LinuxParameters", "LinuxParametersProps", "ListenerConfig", "LoadBalancerTargetOptions", "LogDriver", "LogDriverConfig", "LogDrivers", "MemoryUtilizationScalingProps", "MountPoint", "NetworkMode", "PlacementConstraint", "PlacementStrategy", "PortMapping", "PropagatedTagSource", "Protocol", "ProxyConfiguration", "ProxyConfigurations", "RepositoryImage", "RepositoryImageProps", "RequestCountScalingProps", "ScalableTaskCount", "ScalableTaskCountProps", "Scope", "ScratchSpace", "Secret", "SplunkLogDriver", "SplunkLogDriverProps", "SplunkLogFormat", "SyslogLogDriver", "SyslogLogDriverProps", "TaskDefinition", "TaskDefinitionProps", "Tmpfs", "TmpfsMountOption", "TrackCustomMetricProps", "Ulimit", "UlimitName", "Volume", "VolumeFrom", "WindowsOptimizedVersion", "__jsii_assembly__"]

publication.publish()
