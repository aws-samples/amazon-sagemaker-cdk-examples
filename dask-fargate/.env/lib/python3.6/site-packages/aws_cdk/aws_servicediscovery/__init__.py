"""
## Amazon ECS Service Discovery Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

This package contains constructs for working with **AWS Cloud Map**

AWS Cloud Map is a fully managed service that you can use to create and
maintain a map of the backend services and resources that your applications
depend on.

For further information on AWS Cloud Map,
see the [AWS Cloud Map documentation](https://docs.aws.amazon.com/cloud-map)

### HTTP Namespace Example

The following example creates an AWS Cloud Map namespace that
supports API calls, creates a service in that namespace, and
registers an instance to it:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import ...lib as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
    name="covfefe"
)

service1 = namespace.create_service("NonIpService",
    description="service registering non-ip instances"
)

service1.register_non_ip_instance("NonIpInstance",
    custom_attributes={"arn": "arn:aws:s3:::mybucket"}
)

service2 = namespace.create_service("IpService",
    description="service registering ip instances",
    health_check={
        "type": servicediscovery.HealthCheckType.HTTP,
        "resource_path": "/check"
    }
)

service2.register_ip_instance("IpInstance", {
    "ipv4": "54.239.25.192"
})

app.synth()
```

### Private DNS Namespace Example

The following example creates an AWS Cloud Map namespace that
supports both API calls and DNS queries within a vpc, creates a
service in that namespace, and registers a loadbalancer as an
instance:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.core as cdk
import ...lib as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

vpc = ec2.Vpc(stack, "Vpc", max_azs=2)

namespace = servicediscovery.PrivateDnsNamespace(stack, "Namespace",
    name="boobar.com",
    vpc=vpc
)

service = namespace.create_service("Service",
    dns_record_type=servicediscovery.DnsRecordType.A_AAAA,
    dns_ttl=cdk.Duration.seconds(30),
    load_balancer=True
)

loadbalancer = elbv2.ApplicationLoadBalancer(stack, "LB", vpc=vpc, internet_facing=True)

service.register_load_balancer("Loadbalancer", loadbalancer)

app.synth()
```

### Public DNS Namespace Example

The following example creates an AWS Cloud Map namespace that
supports both API calls and public DNS queries, creates a service in
that namespace, and registers an IP instance:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import ...lib as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
    name="foobar.com"
)

service = namespace.create_service("Service",
    name="foo",
    dns_record_type=servicediscovery.DnsRecordType.A,
    dns_ttl=cdk.Duration.seconds(30),
    health_check={
        "type": servicediscovery.HealthCheckType.HTTPS,
        "resource_path": "/healthcheck",
        "failure_threshold": 2
    }
)

service.register_ip_instance("IpInstance", {
    "ipv4": "54.239.25.192",
    "port": 443
})

app.synth()
```

For DNS namespaces, you can also register instances to services with CNAME records:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import ...lib as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
    name="foobar.com"
)

service = namespace.create_service("Service",
    name="foo",
    dns_record_type=servicediscovery.DnsRecordType.CNAME,
    dns_ttl=cdk.Duration.seconds(30)
)

service.register_cname_instance("CnameInstance",
    instance_cname="service.pizza"
)

app.synth()
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

import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_route53
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-servicediscovery", "1.18.0", __name__, "aws-servicediscovery@1.18.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.BaseInstanceProps", jsii_struct_bases=[], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId'})
class BaseInstanceProps():
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None):
        """Used when the resource that's associated with the service instance is accessible using values other than an IP address or a domain name (CNAME), i.e. for non-ip-instances.

        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        self._values = {
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.AliasTargetInstanceProps", jsii_struct_bases=[BaseInstanceProps], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId', 'dns_name': 'dnsName', 'service': 'service'})
class AliasTargetInstanceProps(BaseInstanceProps):
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None, dns_name: str, service: "IService"):
        """
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param dns_name: DNS name of the target.
        :param service: The Cloudmap service this resource is registered to.
        """
        self._values = {
            'dns_name': dns_name,
            'service': service,
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    @property
    def dns_name(self) -> str:
        """DNS name of the target."""
        return self._values.get('dns_name')

    @property
    def service(self) -> "IService":
        """The Cloudmap service this resource is registered to."""
        return self._values.get('service')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AliasTargetInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.BaseNamespaceProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'description': 'description'})
class BaseNamespaceProps():
    def __init__(self, *, name: str, description: typing.Optional[str]=None):
        """
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        """
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description

    @property
    def name(self) -> str:
        """A name for the Namespace."""
        return self._values.get('name')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the Namespace.

        default
        :default: none
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseNamespaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.BaseServiceProps", jsii_struct_bases=[], name_mapping={'custom_health_check': 'customHealthCheck', 'description': 'description', 'health_check': 'healthCheck', 'name': 'name'})
class BaseServiceProps():
    def __init__(self, *, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None):
        """Basic props needed to create a service in a given namespace.

        Used by HttpNamespace.createService

        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html. Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        """
        if isinstance(custom_health_check, dict): custom_health_check = HealthCheckCustomConfig(**custom_health_check)
        if isinstance(health_check, dict): health_check = HealthCheckConfig(**health_check)
        self._values = {
        }
        if custom_health_check is not None: self._values["custom_health_check"] = custom_health_check
        if description is not None: self._values["description"] = description
        if health_check is not None: self._values["health_check"] = health_check
        if name is not None: self._values["name"] = name

    @property
    def custom_health_check(self) -> typing.Optional["HealthCheckCustomConfig"]:
        """Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html.

        default
        :default: none
        """
        return self._values.get('custom_health_check')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the service.

        default
        :default: none
        """
        return self._values.get('description')

    @property
    def health_check(self) -> typing.Optional["HealthCheckConfig"]:
        """Settings for an optional health check.

        If you specify health check settings, AWS Cloud Map associates the health
        check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can
        be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to
        this service.

        default
        :default: none
        """
        return self._values.get('health_check')

    @property
    def name(self) -> typing.Optional[str]:
        """A name for the Service.

        default
        :default: CloudFormation-generated name
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnHttpNamespace(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnHttpNamespace"):
    """A CloudFormation ``AWS::ServiceDiscovery::HttpNamespace``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html
    cloudformationResource:
    :cloudformationResource:: AWS::ServiceDiscovery::HttpNamespace
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceDiscovery::HttpNamespace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param name: ``AWS::ServiceDiscovery::HttpNamespace.Name``.
        :param description: ``AWS::ServiceDiscovery::HttpNamespace.Description``.
        """
        props = CfnHttpNamespaceProps(name=name, description=description)

        jsii.create(CfnHttpNamespace, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ServiceDiscovery::HttpNamespace.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::HttpNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnHttpNamespaceProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'description': 'description'})
class CfnHttpNamespaceProps():
    def __init__(self, *, name: str, description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ServiceDiscovery::HttpNamespace``.

        :param name: ``AWS::ServiceDiscovery::HttpNamespace.Name``.
        :param description: ``AWS::ServiceDiscovery::HttpNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html
        """
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description

    @property
    def name(self) -> str:
        """``AWS::ServiceDiscovery::HttpNamespace.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-name
        """
        return self._values.get('name')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::HttpNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-description
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnHttpNamespaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnInstance(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnInstance"):
    """A CloudFormation ``AWS::ServiceDiscovery::Instance``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html
    cloudformationResource:
    :cloudformationResource:: AWS::ServiceDiscovery::Instance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, instance_attributes: typing.Any, service_id: str, instance_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceDiscovery::Instance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param instance_attributes: ``AWS::ServiceDiscovery::Instance.InstanceAttributes``.
        :param service_id: ``AWS::ServiceDiscovery::Instance.ServiceId``.
        :param instance_id: ``AWS::ServiceDiscovery::Instance.InstanceId``.
        """
        props = CfnInstanceProps(instance_attributes=instance_attributes, service_id=service_id, instance_id=instance_id)

        jsii.create(CfnInstance, self, [scope, id, props])

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
    @jsii.member(jsii_name="instanceAttributes")
    def instance_attributes(self) -> typing.Any:
        """``AWS::ServiceDiscovery::Instance.InstanceAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceattributes
        """
        return jsii.get(self, "instanceAttributes")

    @instance_attributes.setter
    def instance_attributes(self, value: typing.Any):
        return jsii.set(self, "instanceAttributes", value)

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        """``AWS::ServiceDiscovery::Instance.ServiceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-serviceid
        """
        return jsii.get(self, "serviceId")

    @service_id.setter
    def service_id(self, value: str):
        return jsii.set(self, "serviceId", value)

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Instance.InstanceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceid
        """
        return jsii.get(self, "instanceId")

    @instance_id.setter
    def instance_id(self, value: typing.Optional[str]):
        return jsii.set(self, "instanceId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnInstanceProps", jsii_struct_bases=[], name_mapping={'instance_attributes': 'instanceAttributes', 'service_id': 'serviceId', 'instance_id': 'instanceId'})
class CfnInstanceProps():
    def __init__(self, *, instance_attributes: typing.Any, service_id: str, instance_id: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ServiceDiscovery::Instance``.

        :param instance_attributes: ``AWS::ServiceDiscovery::Instance.InstanceAttributes``.
        :param service_id: ``AWS::ServiceDiscovery::Instance.ServiceId``.
        :param instance_id: ``AWS::ServiceDiscovery::Instance.InstanceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html
        """
        self._values = {
            'instance_attributes': instance_attributes,
            'service_id': service_id,
        }
        if instance_id is not None: self._values["instance_id"] = instance_id

    @property
    def instance_attributes(self) -> typing.Any:
        """``AWS::ServiceDiscovery::Instance.InstanceAttributes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceattributes
        """
        return self._values.get('instance_attributes')

    @property
    def service_id(self) -> str:
        """``AWS::ServiceDiscovery::Instance.ServiceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-serviceid
        """
        return self._values.get('service_id')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Instance.InstanceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceid
        """
        return self._values.get('instance_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPrivateDnsNamespace(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespace"):
    """A CloudFormation ``AWS::ServiceDiscovery::PrivateDnsNamespace``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html
    cloudformationResource:
    :cloudformationResource:: AWS::ServiceDiscovery::PrivateDnsNamespace
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, vpc: str, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceDiscovery::PrivateDnsNamespace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param name: ``AWS::ServiceDiscovery::PrivateDnsNamespace.Name``.
        :param vpc: ``AWS::ServiceDiscovery::PrivateDnsNamespace.Vpc``.
        :param description: ``AWS::ServiceDiscovery::PrivateDnsNamespace.Description``.
        """
        props = CfnPrivateDnsNamespaceProps(name=name, vpc=vpc, description=description)

        jsii.create(CfnPrivateDnsNamespace, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ServiceDiscovery::PrivateDnsNamespace.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> str:
        """``AWS::ServiceDiscovery::PrivateDnsNamespace.Vpc``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-vpc
        """
        return jsii.get(self, "vpc")

    @vpc.setter
    def vpc(self, value: str):
        return jsii.set(self, "vpc", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::PrivateDnsNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespaceProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'vpc': 'vpc', 'description': 'description'})
class CfnPrivateDnsNamespaceProps():
    def __init__(self, *, name: str, vpc: str, description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ServiceDiscovery::PrivateDnsNamespace``.

        :param name: ``AWS::ServiceDiscovery::PrivateDnsNamespace.Name``.
        :param vpc: ``AWS::ServiceDiscovery::PrivateDnsNamespace.Vpc``.
        :param description: ``AWS::ServiceDiscovery::PrivateDnsNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html
        """
        self._values = {
            'name': name,
            'vpc': vpc,
        }
        if description is not None: self._values["description"] = description

    @property
    def name(self) -> str:
        """``AWS::ServiceDiscovery::PrivateDnsNamespace.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-name
        """
        return self._values.get('name')

    @property
    def vpc(self) -> str:
        """``AWS::ServiceDiscovery::PrivateDnsNamespace.Vpc``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-vpc
        """
        return self._values.get('vpc')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::PrivateDnsNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-description
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPrivateDnsNamespaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPublicDnsNamespace(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespace"):
    """A CloudFormation ``AWS::ServiceDiscovery::PublicDnsNamespace``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html
    cloudformationResource:
    :cloudformationResource:: AWS::ServiceDiscovery::PublicDnsNamespace
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceDiscovery::PublicDnsNamespace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param name: ``AWS::ServiceDiscovery::PublicDnsNamespace.Name``.
        :param description: ``AWS::ServiceDiscovery::PublicDnsNamespace.Description``.
        """
        props = CfnPublicDnsNamespaceProps(name=name, description=description)

        jsii.create(CfnPublicDnsNamespace, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ServiceDiscovery::PublicDnsNamespace.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::PublicDnsNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespaceProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'description': 'description'})
class CfnPublicDnsNamespaceProps():
    def __init__(self, *, name: str, description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ServiceDiscovery::PublicDnsNamespace``.

        :param name: ``AWS::ServiceDiscovery::PublicDnsNamespace.Name``.
        :param description: ``AWS::ServiceDiscovery::PublicDnsNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html
        """
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description

    @property
    def name(self) -> str:
        """``AWS::ServiceDiscovery::PublicDnsNamespace.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-name
        """
        return self._values.get('name')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::PublicDnsNamespace.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-description
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPublicDnsNamespaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnService(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CfnService"):
    """A CloudFormation ``AWS::ServiceDiscovery::Service``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html
    cloudformationResource:
    :cloudformationResource:: AWS::ServiceDiscovery::Service
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, dns_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DnsConfigProperty"]]]=None, health_check_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckConfigProperty"]]]=None, health_check_custom_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckCustomConfigProperty"]]]=None, name: typing.Optional[str]=None, namespace_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ServiceDiscovery::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param description: ``AWS::ServiceDiscovery::Service.Description``.
        :param dns_config: ``AWS::ServiceDiscovery::Service.DnsConfig``.
        :param health_check_config: ``AWS::ServiceDiscovery::Service.HealthCheckConfig``.
        :param health_check_custom_config: ``AWS::ServiceDiscovery::Service.HealthCheckCustomConfig``.
        :param name: ``AWS::ServiceDiscovery::Service.Name``.
        :param namespace_id: ``AWS::ServiceDiscovery::Service.NamespaceId``.
        """
        props = CfnServiceProps(description=description, dns_config=dns_config, health_check_config=health_check_config, health_check_custom_config=health_check_custom_config, name=name, namespace_id=namespace_id)

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

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
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Service.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="dnsConfig")
    def dns_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DnsConfigProperty"]]]:
        """``AWS::ServiceDiscovery::Service.DnsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-dnsconfig
        """
        return jsii.get(self, "dnsConfig")

    @dns_config.setter
    def dns_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DnsConfigProperty"]]]):
        return jsii.set(self, "dnsConfig", value)

    @property
    @jsii.member(jsii_name="healthCheckConfig")
    def health_check_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckConfigProperty"]]]:
        """``AWS::ServiceDiscovery::Service.HealthCheckConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckconfig
        """
        return jsii.get(self, "healthCheckConfig")

    @health_check_config.setter
    def health_check_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckConfigProperty"]]]):
        return jsii.set(self, "healthCheckConfig", value)

    @property
    @jsii.member(jsii_name="healthCheckCustomConfig")
    def health_check_custom_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckCustomConfigProperty"]]]:
        """``AWS::ServiceDiscovery::Service.HealthCheckCustomConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckcustomconfig
        """
        return jsii.get(self, "healthCheckCustomConfig")

    @health_check_custom_config.setter
    def health_check_custom_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckCustomConfigProperty"]]]):
        return jsii.set(self, "healthCheckCustomConfig", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Service.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Service.NamespaceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-namespaceid
        """
        return jsii.get(self, "namespaceId")

    @namespace_id.setter
    def namespace_id(self, value: typing.Optional[str]):
        return jsii.set(self, "namespaceId", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.DnsConfigProperty", jsii_struct_bases=[], name_mapping={'dns_records': 'dnsRecords', 'namespace_id': 'namespaceId', 'routing_policy': 'routingPolicy'})
    class DnsConfigProperty():
        def __init__(self, *, dns_records: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.DnsRecordProperty"]]], namespace_id: typing.Optional[str]=None, routing_policy: typing.Optional[str]=None):
            """
            :param dns_records: ``CfnService.DnsConfigProperty.DnsRecords``.
            :param namespace_id: ``CfnService.DnsConfigProperty.NamespaceId``.
            :param routing_policy: ``CfnService.DnsConfigProperty.RoutingPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html
            """
            self._values = {
                'dns_records': dns_records,
            }
            if namespace_id is not None: self._values["namespace_id"] = namespace_id
            if routing_policy is not None: self._values["routing_policy"] = routing_policy

        @property
        def dns_records(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnService.DnsRecordProperty"]]]:
            """``CfnService.DnsConfigProperty.DnsRecords``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-dnsrecords
            """
            return self._values.get('dns_records')

        @property
        def namespace_id(self) -> typing.Optional[str]:
            """``CfnService.DnsConfigProperty.NamespaceId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-namespaceid
            """
            return self._values.get('namespace_id')

        @property
        def routing_policy(self) -> typing.Optional[str]:
            """``CfnService.DnsConfigProperty.RoutingPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-routingpolicy
            """
            return self._values.get('routing_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DnsConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.DnsRecordProperty", jsii_struct_bases=[], name_mapping={'ttl': 'ttl', 'type': 'type'})
    class DnsRecordProperty():
        def __init__(self, *, ttl: jsii.Number, type: str):
            """
            :param ttl: ``CfnService.DnsRecordProperty.TTL``.
            :param type: ``CfnService.DnsRecordProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html
            """
            self._values = {
                'ttl': ttl,
                'type': type,
            }

        @property
        def ttl(self) -> jsii.Number:
            """``CfnService.DnsRecordProperty.TTL``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html#cfn-servicediscovery-service-dnsrecord-ttl
            """
            return self._values.get('ttl')

        @property
        def type(self) -> str:
            """``CfnService.DnsRecordProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html#cfn-servicediscovery-service-dnsrecord-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DnsRecordProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.HealthCheckConfigProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'failure_threshold': 'failureThreshold', 'resource_path': 'resourcePath'})
    class HealthCheckConfigProperty():
        def __init__(self, *, type: str, failure_threshold: typing.Optional[jsii.Number]=None, resource_path: typing.Optional[str]=None):
            """
            :param type: ``CfnService.HealthCheckConfigProperty.Type``.
            :param failure_threshold: ``CfnService.HealthCheckConfigProperty.FailureThreshold``.
            :param resource_path: ``CfnService.HealthCheckConfigProperty.ResourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html
            """
            self._values = {
                'type': type,
            }
            if failure_threshold is not None: self._values["failure_threshold"] = failure_threshold
            if resource_path is not None: self._values["resource_path"] = resource_path

        @property
        def type(self) -> str:
            """``CfnService.HealthCheckConfigProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-type
            """
            return self._values.get('type')

        @property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnService.HealthCheckConfigProperty.FailureThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-failurethreshold
            """
            return self._values.get('failure_threshold')

        @property
        def resource_path(self) -> typing.Optional[str]:
            """``CfnService.HealthCheckConfigProperty.ResourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-resourcepath
            """
            return self._values.get('resource_path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnService.HealthCheckCustomConfigProperty", jsii_struct_bases=[], name_mapping={'failure_threshold': 'failureThreshold'})
    class HealthCheckCustomConfigProperty():
        def __init__(self, *, failure_threshold: typing.Optional[jsii.Number]=None):
            """
            :param failure_threshold: ``CfnService.HealthCheckCustomConfigProperty.FailureThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckcustomconfig.html
            """
            self._values = {
            }
            if failure_threshold is not None: self._values["failure_threshold"] = failure_threshold

        @property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnService.HealthCheckCustomConfigProperty.FailureThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckcustomconfig.html#cfn-servicediscovery-service-healthcheckcustomconfig-failurethreshold
            """
            return self._values.get('failure_threshold')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckCustomConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CfnServiceProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'dns_config': 'dnsConfig', 'health_check_config': 'healthCheckConfig', 'health_check_custom_config': 'healthCheckCustomConfig', 'name': 'name', 'namespace_id': 'namespaceId'})
class CfnServiceProps():
    def __init__(self, *, description: typing.Optional[str]=None, dns_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.DnsConfigProperty"]]]=None, health_check_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.HealthCheckConfigProperty"]]]=None, health_check_custom_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.HealthCheckCustomConfigProperty"]]]=None, name: typing.Optional[str]=None, namespace_id: typing.Optional[str]=None):
        """Properties for defining a ``AWS::ServiceDiscovery::Service``.

        :param description: ``AWS::ServiceDiscovery::Service.Description``.
        :param dns_config: ``AWS::ServiceDiscovery::Service.DnsConfig``.
        :param health_check_config: ``AWS::ServiceDiscovery::Service.HealthCheckConfig``.
        :param health_check_custom_config: ``AWS::ServiceDiscovery::Service.HealthCheckCustomConfig``.
        :param name: ``AWS::ServiceDiscovery::Service.Name``.
        :param namespace_id: ``AWS::ServiceDiscovery::Service.NamespaceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if dns_config is not None: self._values["dns_config"] = dns_config
        if health_check_config is not None: self._values["health_check_config"] = health_check_config
        if health_check_custom_config is not None: self._values["health_check_custom_config"] = health_check_custom_config
        if name is not None: self._values["name"] = name
        if namespace_id is not None: self._values["namespace_id"] = namespace_id

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Service.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-description
        """
        return self._values.get('description')

    @property
    def dns_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.DnsConfigProperty"]]]:
        """``AWS::ServiceDiscovery::Service.DnsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-dnsconfig
        """
        return self._values.get('dns_config')

    @property
    def health_check_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.HealthCheckConfigProperty"]]]:
        """``AWS::ServiceDiscovery::Service.HealthCheckConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckconfig
        """
        return self._values.get('health_check_config')

    @property
    def health_check_custom_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnService.HealthCheckCustomConfigProperty"]]]:
        """``AWS::ServiceDiscovery::Service.HealthCheckCustomConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckcustomconfig
        """
        return self._values.get('health_check_custom_config')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Service.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-name
        """
        return self._values.get('name')

    @property
    def namespace_id(self) -> typing.Optional[str]:
        """``AWS::ServiceDiscovery::Service.NamespaceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-namespaceid
        """
        return self._values.get('namespace_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CnameInstanceBaseProps", jsii_struct_bases=[BaseInstanceProps], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId', 'instance_cname': 'instanceCname'})
class CnameInstanceBaseProps(BaseInstanceProps):
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None, instance_cname: str):
        """
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.
        """
        self._values = {
            'instance_cname': instance_cname,
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    @property
    def instance_cname(self) -> str:
        """If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record."""
        return self._values.get('instance_cname')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CnameInstanceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.CnameInstanceProps", jsii_struct_bases=[CnameInstanceBaseProps], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId', 'instance_cname': 'instanceCname', 'service': 'service'})
class CnameInstanceProps(CnameInstanceBaseProps):
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None, instance_cname: str, service: "IService"):
        """
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.
        :param service: The Cloudmap service this resource is registered to.
        """
        self._values = {
            'instance_cname': instance_cname,
            'service': service,
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    @property
    def instance_cname(self) -> str:
        """If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record."""
        return self._values.get('instance_cname')

    @property
    def service(self) -> "IService":
        """The Cloudmap service this resource is registered to."""
        return self._values.get('service')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CnameInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.DnsRecordType")
class DnsRecordType(enum.Enum):
    A = "A"
    """An A record."""
    AAAA = "AAAA"
    """An AAAA record."""
    A_AAAA = "A_AAAA"
    """Both an A and AAAA record."""
    SRV = "SRV"
    """A Srv record."""
    CNAME = "CNAME"
    """A CNAME record."""

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.DnsServiceProps", jsii_struct_bases=[BaseServiceProps], name_mapping={'custom_health_check': 'customHealthCheck', 'description': 'description', 'health_check': 'healthCheck', 'name': 'name', 'dns_record_type': 'dnsRecordType', 'dns_ttl': 'dnsTtl', 'load_balancer': 'loadBalancer', 'routing_policy': 'routingPolicy'})
class DnsServiceProps(BaseServiceProps):
    def __init__(self, *, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None, dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl: typing.Optional[aws_cdk.core.Duration]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None):
        """Service props needed to create a service in a given namespace.

        Used by createService() for PrivateDnsNamespace and
        PublicDnsNamespace

        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html. Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        """
        if isinstance(custom_health_check, dict): custom_health_check = HealthCheckCustomConfig(**custom_health_check)
        if isinstance(health_check, dict): health_check = HealthCheckConfig(**health_check)
        self._values = {
        }
        if custom_health_check is not None: self._values["custom_health_check"] = custom_health_check
        if description is not None: self._values["description"] = description
        if health_check is not None: self._values["health_check"] = health_check
        if name is not None: self._values["name"] = name
        if dns_record_type is not None: self._values["dns_record_type"] = dns_record_type
        if dns_ttl is not None: self._values["dns_ttl"] = dns_ttl
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if routing_policy is not None: self._values["routing_policy"] = routing_policy

    @property
    def custom_health_check(self) -> typing.Optional["HealthCheckCustomConfig"]:
        """Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html.

        default
        :default: none
        """
        return self._values.get('custom_health_check')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the service.

        default
        :default: none
        """
        return self._values.get('description')

    @property
    def health_check(self) -> typing.Optional["HealthCheckConfig"]:
        """Settings for an optional health check.

        If you specify health check settings, AWS Cloud Map associates the health
        check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can
        be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to
        this service.

        default
        :default: none
        """
        return self._values.get('health_check')

    @property
    def name(self) -> typing.Optional[str]:
        """A name for the Service.

        default
        :default: CloudFormation-generated name
        """
        return self._values.get('name')

    @property
    def dns_record_type(self) -> typing.Optional["DnsRecordType"]:
        """The DNS type of the record that you want AWS Cloud Map to create.

        Supported record types
        include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV.

        default
        :default: A
        """
        return self._values.get('dns_record_type')

    @property
    def dns_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record.

        default
        :default: Duration.minutes(1)
        """
        return self._values.get('dns_ttl')

    @property
    def load_balancer(self) -> typing.Optional[bool]:
        """Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance.

        Setting this to ``true`` correctly configures the ``routingPolicy``
        and performs some additional validation.

        default
        :default: false
        """
        return self._values.get('load_balancer')

    @property
    def routing_policy(self) -> typing.Optional["RoutingPolicy"]:
        """The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service.

        default
        :default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        """
        return self._values.get('routing_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DnsServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckConfig", jsii_struct_bases=[], name_mapping={'failure_threshold': 'failureThreshold', 'resource_path': 'resourcePath', 'type': 'type'})
class HealthCheckConfig():
    def __init__(self, *, failure_threshold: typing.Optional[jsii.Number]=None, resource_path: typing.Optional[str]=None, type: typing.Optional["HealthCheckType"]=None):
        """Settings for an optional Amazon Route 53 health check.

        If you specify settings for a health check, AWS Cloud Map
        associates the health check with all the records that you specify in DnsConfig. Only valid with a PublicDnsNamespace.

        :param failure_threshold: The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or vice versa. Default: 1
        :param resource_path: The path that you want Route 53 to request when performing health checks. Do not use when health check type is TCP. Default: '/'
        :param type: The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. Cannot be modified once created. Supported values are HTTP, HTTPS, and TCP. Default: HTTP
        """
        self._values = {
        }
        if failure_threshold is not None: self._values["failure_threshold"] = failure_threshold
        if resource_path is not None: self._values["resource_path"] = resource_path
        if type is not None: self._values["type"] = type

    @property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        """The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or vice versa.

        default
        :default: 1
        """
        return self._values.get('failure_threshold')

    @property
    def resource_path(self) -> typing.Optional[str]:
        """The path that you want Route 53 to request when performing health checks.

        Do not use when health check type is TCP.

        default
        :default: '/'
        """
        return self._values.get('resource_path')

    @property
    def type(self) -> typing.Optional["HealthCheckType"]:
        """The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy.

        Cannot be modified once created. Supported values are HTTP, HTTPS, and TCP.

        default
        :default: HTTP
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HealthCheckConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckCustomConfig", jsii_struct_bases=[], name_mapping={'failure_threshold': 'failureThreshold'})
class HealthCheckCustomConfig():
    def __init__(self, *, failure_threshold: typing.Optional[jsii.Number]=None):
        """Specifies information about an optional custom health check.

        :param failure_threshold: The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance. Default: 1
        """
        self._values = {
        }
        if failure_threshold is not None: self._values["failure_threshold"] = failure_threshold

    @property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        """The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance.

        default
        :default: 1
        """
        return self._values.get('failure_threshold')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HealthCheckCustomConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckType")
class HealthCheckType(enum.Enum):
    HTTP = "HTTP"
    """Route 53 tries to establish a TCP connection.

    If successful, Route 53 submits an HTTP request and waits for an HTTP
    status code of 200 or greater and less than 400.
    """
    HTTPS = "HTTPS"
    """Route 53 tries to establish a TCP connection.

    If successful, Route 53 submits an HTTPS request and waits for an
    HTTP status code of 200 or greater and less than 400.  If you specify HTTPS for the value of Type, the endpoint
    must support TLS v1.0 or later.
    """
    TCP = "TCP"
    """Route 53 tries to establish a TCP connection. If you specify TCP for Type, don't specify a value for ResourcePath."""

@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespaceAttributes", jsii_struct_bases=[], name_mapping={'namespace_arn': 'namespaceArn', 'namespace_id': 'namespaceId', 'namespace_name': 'namespaceName'})
class HttpNamespaceAttributes():
    def __init__(self, *, namespace_arn: str, namespace_id: str, namespace_name: str):
        """
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        """
        self._values = {
            'namespace_arn': namespace_arn,
            'namespace_id': namespace_id,
            'namespace_name': namespace_name,
        }

    @property
    def namespace_arn(self) -> str:
        """Namespace ARN for the Namespace."""
        return self._values.get('namespace_arn')

    @property
    def namespace_id(self) -> str:
        """Namespace Id for the Namespace."""
        return self._values.get('namespace_id')

    @property
    def namespace_name(self) -> str:
        """A name for the Namespace."""
        return self._values.get('namespace_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpNamespaceAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespaceProps", jsii_struct_bases=[BaseNamespaceProps], name_mapping={'name': 'name', 'description': 'description'})
class HttpNamespaceProps(BaseNamespaceProps):
    def __init__(self, *, name: str, description: typing.Optional[str]=None):
        """
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        """
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description

    @property
    def name(self) -> str:
        """A name for the Namespace."""
        return self._values.get('name')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the Namespace.

        default
        :default: none
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpNamespaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IInstance")
class IInstance(aws_cdk.core.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IInstanceProxy

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """The id of the instance resource.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        """The Cloudmap service this resource is registered to."""
        ...


class _IInstanceProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.IInstance"
    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """The id of the instance resource.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        """The Cloudmap service this resource is registered to."""
        return jsii.get(self, "service")


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.INamespace")
class INamespace(aws_cdk.core.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _INamespaceProxy

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        """Namespace ARN for the Namespace.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        """Namespace Id for the Namespace.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        """A name for the Namespace.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        """Type of Namespace."""
        ...


class _INamespaceProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.INamespace"
    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        """Namespace ARN for the Namespace.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        """Namespace Id for the Namespace.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        """A name for the Namespace.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        """Type of Namespace."""
        return jsii.get(self, "type")


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IHttpNamespace")
class IHttpNamespace(INamespace, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IHttpNamespaceProxy

    pass

class _IHttpNamespaceProxy(jsii.proxy_for(INamespace)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.IHttpNamespace"
    pass

@jsii.implements(IHttpNamespace)
class HttpNamespace(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespace"):
    """Define an HTTP Namespace."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        """
        props = HttpNamespaceProps(name=name, description=description)

        jsii.create(HttpNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="fromHttpNamespaceAttributes")
    @classmethod
    def from_http_namespace_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, namespace_arn: str, namespace_id: str, namespace_name: str) -> "IHttpNamespace":
        """
        :param scope: -
        :param id: -
        :param attrs: -
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        """
        attrs = HttpNamespaceAttributes(namespace_arn=namespace_arn, namespace_id=namespace_id, namespace_name=namespace_name)

        return jsii.sinvoke(cls, "fromHttpNamespaceAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="createService")
    def create_service(self, id: str, *, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> "Service":
        """Creates a service within the namespace.

        :param id: -
        :param props: -
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html. Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        """
        props = BaseServiceProps(custom_health_check=custom_health_check, description=description, health_check=health_check, name=name)

        return jsii.invoke(self, "createService", [id, props])

    @property
    @jsii.member(jsii_name="httpNamespaceArn")
    def http_namespace_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "httpNamespaceArn")

    @property
    @jsii.member(jsii_name="httpNamespaceId")
    def http_namespace_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "httpNamespaceId")

    @property
    @jsii.member(jsii_name="httpNamespaceName")
    def http_namespace_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "httpNamespaceName")

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        """Namespace Arn for the namespace."""
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        """Namespace Id for the namespace."""
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        """A name for the namespace."""
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        """Type of the namespace."""
        return jsii.get(self, "type")


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IPrivateDnsNamespace")
class IPrivateDnsNamespace(INamespace, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPrivateDnsNamespaceProxy

    pass

class _IPrivateDnsNamespaceProxy(jsii.proxy_for(INamespace)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.IPrivateDnsNamespace"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IPublicDnsNamespace")
class IPublicDnsNamespace(INamespace, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPublicDnsNamespaceProxy

    pass

class _IPublicDnsNamespaceProxy(jsii.proxy_for(INamespace)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.IPublicDnsNamespace"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IService")
class IService(aws_cdk.core.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IServiceProxy

    @property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> "DnsRecordType":
        """The DnsRecordType used by the service."""
        ...

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> "INamespace":
        """The namespace for the Cloudmap Service."""
        ...

    @property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        """The Routing Policy used by the service."""
        ...

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Arn of the namespace that you want to use for DNS configuration.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        """The ID of the namespace that you want to use for DNS configuration.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """A name for the Cloudmap Service.

        attribute:
        :attribute:: true
        """
        ...


class _IServiceProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-servicediscovery.IService"
    @property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> "DnsRecordType":
        """The DnsRecordType used by the service."""
        return jsii.get(self, "dnsRecordType")

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> "INamespace":
        """The namespace for the Cloudmap Service."""
        return jsii.get(self, "namespace")

    @property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        """The Routing Policy used by the service."""
        return jsii.get(self, "routingPolicy")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Arn of the namespace that you want to use for DNS configuration.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        """The ID of the namespace that you want to use for DNS configuration.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceId")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """A name for the Cloudmap Service.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceName")


@jsii.implements(IInstance)
class InstanceBase(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-servicediscovery.InstanceBase"):
    @staticmethod
    def __jsii_proxy_class__():
        return _InstanceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = aws_cdk.core.ResourceProps(physical_name=physical_name)

        jsii.create(InstanceBase, self, [scope, id, props])

    @jsii.member(jsii_name="uniqueInstanceId")
    def _unique_instance_id(self) -> str:
        """Generate a unique instance Id that is safe to pass to CloudMap."""
        return jsii.invoke(self, "uniqueInstanceId", [])

    @property
    @jsii.member(jsii_name="instanceId")
    @abc.abstractmethod
    def instance_id(self) -> str:
        """The Id of the instance."""
        ...

    @property
    @jsii.member(jsii_name="service")
    @abc.abstractmethod
    def service(self) -> "IService":
        """The Cloudmap service to which the instance is registered."""
        ...


class _InstanceBaseProxy(InstanceBase, jsii.proxy_for(aws_cdk.core.Resource)):
    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """The Id of the instance."""
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        """The Cloudmap service to which the instance is registered."""
        return jsii.get(self, "service")


class AliasTargetInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.AliasTargetInstance"):
    """Instance that uses Route 53 Alias record type.

    Currently, the only resource types supported are Elastic Load
    Balancers.

    resource:
    :resource:: AWS::ServiceDiscovery::Instance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, dns_name: str, service: "IService", custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param dns_name: DNS name of the target.
        :param service: The Cloudmap service this resource is registered to.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        props = AliasTargetInstanceProps(dns_name=dns_name, service=service, custom_attributes=custom_attributes, instance_id=instance_id)

        jsii.create(AliasTargetInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        """The Route53 DNS name of the alias target."""
        return jsii.get(self, "dnsName")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """The Id of the instance."""
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        """The Cloudmap service to which the instance is registered."""
        return jsii.get(self, "service")


class CnameInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.CnameInstance"):
    """Instance that is accessible using a domain name (CNAME).

    resource:
    :resource:: AWS::ServiceDiscovery::Instance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, service: "IService", instance_cname: str, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param service: The Cloudmap service this resource is registered to.
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        props = CnameInstanceProps(service=service, instance_cname=instance_cname, custom_attributes=custom_attributes, instance_id=instance_id)

        jsii.create(CnameInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="cname")
    def cname(self) -> str:
        """The domain name returned by DNS queries for the instance."""
        return jsii.get(self, "cname")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """The Id of the instance."""
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        """The Cloudmap service to which the instance is registered."""
        return jsii.get(self, "service")


class IpInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.IpInstance"):
    """Instance that is accessible using an IP address.

    resource:
    :resource:: AWS::ServiceDiscovery::Instance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, service: "IService", ipv4: typing.Optional[str]=None, ipv6: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param service: The Cloudmap service this resource is registered to.
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        props = IpInstanceProps(service=service, ipv4=ipv4, ipv6=ipv6, port=port, custom_attributes=custom_attributes, instance_id=instance_id)

        jsii.create(IpInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """The Id of the instance."""
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> str:
        """The Ipv4 address of the instance, or blank string if none available."""
        return jsii.get(self, "ipv4")

    @property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> str:
        """The Ipv6 address of the instance, or blank string if none available."""
        return jsii.get(self, "ipv6")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """The exposed port of the instance."""
        return jsii.get(self, "port")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        """The Cloudmap service to which the instance is registered."""
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.IpInstanceBaseProps", jsii_struct_bases=[BaseInstanceProps], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId', 'ipv4': 'ipv4', 'ipv6': 'ipv6', 'port': 'port'})
class IpInstanceBaseProps(BaseInstanceProps):
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None, ipv4: typing.Optional[str]=None, ipv6: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None):
        """
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80
        """
        self._values = {
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id
        if ipv4 is not None: self._values["ipv4"] = ipv4
        if ipv6 is not None: self._values["ipv6"] = ipv6
        if port is not None: self._values["port"] = port

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    @property
    def ipv4(self) -> typing.Optional[str]:
        """If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record.

        default
        :default: none
        """
        return self._values.get('ipv4')

    @property
    def ipv6(self) -> typing.Optional[str]:
        """If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record.

        default
        :default: none
        """
        return self._values.get('ipv6')

    @property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on the endpoint that you want AWS Cloud Map to perform health checks on.

        This value is also used for
        the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a
        default port that is applied to all instances in the Service configuration.

        default
        :default: 80
        """
        return self._values.get('port')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'IpInstanceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.IpInstanceProps", jsii_struct_bases=[IpInstanceBaseProps], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId', 'ipv4': 'ipv4', 'ipv6': 'ipv6', 'port': 'port', 'service': 'service'})
class IpInstanceProps(IpInstanceBaseProps):
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None, ipv4: typing.Optional[str]=None, ipv6: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, service: "IService"):
        """
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80
        :param service: The Cloudmap service this resource is registered to.
        """
        self._values = {
            'service': service,
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id
        if ipv4 is not None: self._values["ipv4"] = ipv4
        if ipv6 is not None: self._values["ipv6"] = ipv6
        if port is not None: self._values["port"] = port

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    @property
    def ipv4(self) -> typing.Optional[str]:
        """If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record.

        default
        :default: none
        """
        return self._values.get('ipv4')

    @property
    def ipv6(self) -> typing.Optional[str]:
        """If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record.

        default
        :default: none
        """
        return self._values.get('ipv6')

    @property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on the endpoint that you want AWS Cloud Map to perform health checks on.

        This value is also used for
        the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a
        default port that is applied to all instances in the Service configuration.

        default
        :default: 80
        """
        return self._values.get('port')

    @property
    def service(self) -> "IService":
        """The Cloudmap service this resource is registered to."""
        return self._values.get('service')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'IpInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.NamespaceType")
class NamespaceType(enum.Enum):
    HTTP = "HTTP"
    """Choose this option if you want your application to use only API calls to discover registered instances."""
    DNS_PRIVATE = "DNS_PRIVATE"
    """Choose this option if you want your application to be able to discover instances using either API calls or using DNS queries in a VPC."""
    DNS_PUBLIC = "DNS_PUBLIC"
    """Choose this option if you want your application to be able to discover instances using either API calls or using public DNS queries.

    You aren't required to use both methods.
    """

class NonIpInstance(InstanceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstance"):
    """Instance accessible using values other than an IP address or a domain name (CNAME). Specify the other values in Custom attributes.

    resource:
    :resource:: AWS::ServiceDiscovery::Instance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, service: "IService", custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param service: The Cloudmap service this resource is registered to.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        props = NonIpInstanceProps(service=service, custom_attributes=custom_attributes, instance_id=instance_id)

        jsii.create(NonIpInstance, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        """The Id of the instance."""
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        """The Cloudmap service to which the instance is registered."""
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstanceBaseProps", jsii_struct_bases=[BaseInstanceProps], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId'})
class NonIpInstanceBaseProps(BaseInstanceProps):
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None):
        """
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        self._values = {
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NonIpInstanceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstanceProps", jsii_struct_bases=[NonIpInstanceBaseProps], name_mapping={'custom_attributes': 'customAttributes', 'instance_id': 'instanceId', 'service': 'service'})
class NonIpInstanceProps(NonIpInstanceBaseProps):
    def __init__(self, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None, service: "IService"):
        """
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param service: The Cloudmap service this resource is registered to.
        """
        self._values = {
            'service': service,
        }
        if custom_attributes is not None: self._values["custom_attributes"] = custom_attributes
        if instance_id is not None: self._values["instance_id"] = instance_id

    @property
    def custom_attributes(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Custom attributes of the instance.

        default
        :default: none
        """
        return self._values.get('custom_attributes')

    @property
    def instance_id(self) -> typing.Optional[str]:
        """The id of the instance resource.

        default
        :default: Automatically generated name
        """
        return self._values.get('instance_id')

    @property
    def service(self) -> "IService":
        """The Cloudmap service this resource is registered to."""
        return self._values.get('service')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NonIpInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IPrivateDnsNamespace)
class PrivateDnsNamespace(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespace"):
    """Define a Service Discovery HTTP Namespace."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpc, name: str, description: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param vpc: The Amazon VPC that you want to associate the namespace with.
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        """
        props = PrivateDnsNamespaceProps(vpc=vpc, name=name, description=description)

        jsii.create(PrivateDnsNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="fromPrivateDnsNamespaceAttributes")
    @classmethod
    def from_private_dns_namespace_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, namespace_arn: str, namespace_id: str, namespace_name: str) -> "IPrivateDnsNamespace":
        """
        :param scope: -
        :param id: -
        :param attrs: -
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        """
        attrs = PrivateDnsNamespaceAttributes(namespace_arn=namespace_arn, namespace_id=namespace_id, namespace_name=namespace_name)

        return jsii.sinvoke(cls, "fromPrivateDnsNamespaceAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="createService")
    def create_service(self, id: str, *, dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl: typing.Optional[aws_cdk.core.Duration]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> "Service":
        """Creates a service within the namespace.

        :param id: -
        :param props: -
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html. Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        """
        props = DnsServiceProps(dns_record_type=dns_record_type, dns_ttl=dns_ttl, load_balancer=load_balancer, routing_policy=routing_policy, custom_health_check=custom_health_check, description=description, health_check=health_check, name=name)

        return jsii.invoke(self, "createService", [id, props])

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        """Namespace Arn of the namespace."""
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        """Namespace Id of the PrivateDnsNamespace."""
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        """The name of the PrivateDnsNamespace."""
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="privateDnsNamespaceArn")
    def private_dns_namespace_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "privateDnsNamespaceArn")

    @property
    @jsii.member(jsii_name="privateDnsNamespaceId")
    def private_dns_namespace_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "privateDnsNamespaceId")

    @property
    @jsii.member(jsii_name="privateDnsNamespaceName")
    def private_dns_namespace_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "privateDnsNamespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        """Type of the namespace."""
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespaceAttributes", jsii_struct_bases=[], name_mapping={'namespace_arn': 'namespaceArn', 'namespace_id': 'namespaceId', 'namespace_name': 'namespaceName'})
class PrivateDnsNamespaceAttributes():
    def __init__(self, *, namespace_arn: str, namespace_id: str, namespace_name: str):
        """
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        """
        self._values = {
            'namespace_arn': namespace_arn,
            'namespace_id': namespace_id,
            'namespace_name': namespace_name,
        }

    @property
    def namespace_arn(self) -> str:
        """Namespace ARN for the Namespace."""
        return self._values.get('namespace_arn')

    @property
    def namespace_id(self) -> str:
        """Namespace Id for the Namespace."""
        return self._values.get('namespace_id')

    @property
    def namespace_name(self) -> str:
        """A name for the Namespace."""
        return self._values.get('namespace_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PrivateDnsNamespaceAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespaceProps", jsii_struct_bases=[BaseNamespaceProps], name_mapping={'name': 'name', 'description': 'description', 'vpc': 'vpc'})
class PrivateDnsNamespaceProps(BaseNamespaceProps):
    def __init__(self, *, name: str, description: typing.Optional[str]=None, vpc: aws_cdk.aws_ec2.IVpc):
        """
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        :param vpc: The Amazon VPC that you want to associate the namespace with.
        """
        self._values = {
            'name': name,
            'vpc': vpc,
        }
        if description is not None: self._values["description"] = description

    @property
    def name(self) -> str:
        """A name for the Namespace."""
        return self._values.get('name')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the Namespace.

        default
        :default: none
        """
        return self._values.get('description')

    @property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The Amazon VPC that you want to associate the namespace with."""
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PrivateDnsNamespaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IPublicDnsNamespace)
class PublicDnsNamespace(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespace"):
    """Define a Public DNS Namespace."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, description: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        """
        props = PublicDnsNamespaceProps(name=name, description=description)

        jsii.create(PublicDnsNamespace, self, [scope, id, props])

    @jsii.member(jsii_name="fromPublicDnsNamespaceAttributes")
    @classmethod
    def from_public_dns_namespace_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, namespace_arn: str, namespace_id: str, namespace_name: str) -> "IPublicDnsNamespace":
        """
        :param scope: -
        :param id: -
        :param attrs: -
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        """
        attrs = PublicDnsNamespaceAttributes(namespace_arn=namespace_arn, namespace_id=namespace_id, namespace_name=namespace_name)

        return jsii.sinvoke(cls, "fromPublicDnsNamespaceAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="createService")
    def create_service(self, id: str, *, dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl: typing.Optional[aws_cdk.core.Duration]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> "Service":
        """Creates a service within the namespace.

        :param id: -
        :param props: -
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html. Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        """
        props = DnsServiceProps(dns_record_type=dns_record_type, dns_ttl=dns_ttl, load_balancer=load_balancer, routing_policy=routing_policy, custom_health_check=custom_health_check, description=description, health_check=health_check, name=name)

        return jsii.invoke(self, "createService", [id, props])

    @property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> str:
        """Namespace Arn for the namespace."""
        return jsii.get(self, "namespaceArn")

    @property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> str:
        """Namespace Id for the namespace."""
        return jsii.get(self, "namespaceId")

    @property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> str:
        """A name for the namespace."""
        return jsii.get(self, "namespaceName")

    @property
    @jsii.member(jsii_name="publicDnsNamespaceArn")
    def public_dns_namespace_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "publicDnsNamespaceArn")

    @property
    @jsii.member(jsii_name="publicDnsNamespaceId")
    def public_dns_namespace_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "publicDnsNamespaceId")

    @property
    @jsii.member(jsii_name="publicDnsNamespaceName")
    def public_dns_namespace_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "publicDnsNamespaceName")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        """Type of the namespace."""
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespaceAttributes", jsii_struct_bases=[], name_mapping={'namespace_arn': 'namespaceArn', 'namespace_id': 'namespaceId', 'namespace_name': 'namespaceName'})
class PublicDnsNamespaceAttributes():
    def __init__(self, *, namespace_arn: str, namespace_id: str, namespace_name: str):
        """
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        """
        self._values = {
            'namespace_arn': namespace_arn,
            'namespace_id': namespace_id,
            'namespace_name': namespace_name,
        }

    @property
    def namespace_arn(self) -> str:
        """Namespace ARN for the Namespace."""
        return self._values.get('namespace_arn')

    @property
    def namespace_id(self) -> str:
        """Namespace Id for the Namespace."""
        return self._values.get('namespace_id')

    @property
    def namespace_name(self) -> str:
        """A name for the Namespace."""
        return self._values.get('namespace_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PublicDnsNamespaceAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespaceProps", jsii_struct_bases=[BaseNamespaceProps], name_mapping={'name': 'name', 'description': 'description'})
class PublicDnsNamespaceProps(BaseNamespaceProps):
    def __init__(self, *, name: str, description: typing.Optional[str]=None):
        """
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        """
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description

    @property
    def name(self) -> str:
        """A name for the Namespace."""
        return self._values.get('name')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the Namespace.

        default
        :default: none
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PublicDnsNamespaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.RoutingPolicy")
class RoutingPolicy(enum.Enum):
    WEIGHTED = "WEIGHTED"
    """Route 53 returns the applicable value from one randomly selected instance from among the instances that you registered using the same service."""
    MULTIVALUE = "MULTIVALUE"
    """If you define a health check for the service and the health check is healthy, Route 53 returns the applicable value for up to eight instances."""

@jsii.implements(IService)
class Service(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-servicediscovery.Service"):
    """Define a CloudMap Service."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, namespace: "INamespace", dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl: typing.Optional[aws_cdk.core.Duration]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param namespace: The ID of the namespace that you want to use for DNS configuration.
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html. Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        """
        props = ServiceProps(namespace=namespace, dns_record_type=dns_record_type, dns_ttl=dns_ttl, load_balancer=load_balancer, routing_policy=routing_policy, custom_health_check=custom_health_check, description=description, health_check=health_check, name=name)

        jsii.create(Service, self, [scope, id, props])

    @jsii.member(jsii_name="fromServiceAttributes")
    @classmethod
    def from_service_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, dns_record_type: "DnsRecordType", namespace: "INamespace", routing_policy: "RoutingPolicy", service_arn: str, service_id: str, service_name: str) -> "IService":
        """
        :param scope: -
        :param id: -
        :param attrs: -
        :param dns_record_type: 
        :param namespace: 
        :param routing_policy: 
        :param service_arn: 
        :param service_id: 
        :param service_name: 
        """
        attrs = ServiceAttributes(dns_record_type=dns_record_type, namespace=namespace, routing_policy=routing_policy, service_arn=service_arn, service_id=service_id, service_name=service_name)

        return jsii.sinvoke(cls, "fromServiceAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="registerCnameInstance")
    def register_cname_instance(self, id: str, *, instance_cname: str, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> "IInstance":
        """Registers a resource that is accessible using a CNAME.

        :param id: -
        :param props: -
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        props = CnameInstanceBaseProps(instance_cname=instance_cname, custom_attributes=custom_attributes, instance_id=instance_id)

        return jsii.invoke(self, "registerCnameInstance", [id, props])

    @jsii.member(jsii_name="registerIpInstance")
    def register_ip_instance(self, id: str, *, ipv4: typing.Optional[str]=None, ipv6: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> "IInstance":
        """Registers a resource that is accessible using an IP address.

        :param id: -
        :param props: -
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        props = IpInstanceBaseProps(ipv4=ipv4, ipv6=ipv6, port=port, custom_attributes=custom_attributes, instance_id=instance_id)

        return jsii.invoke(self, "registerIpInstance", [id, props])

    @jsii.member(jsii_name="registerLoadBalancer")
    def register_load_balancer(self, id: str, load_balancer: aws_cdk.aws_elasticloadbalancingv2.ILoadBalancerV2, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None) -> "IInstance":
        """Registers an ELB as a new instance with unique name instanceId in this service.

        :param id: -
        :param load_balancer: -
        :param custom_attributes: -
        """
        return jsii.invoke(self, "registerLoadBalancer", [id, load_balancer, custom_attributes])

    @jsii.member(jsii_name="registerNonIpInstance")
    def register_non_ip_instance(self, id: str, *, custom_attributes: typing.Optional[typing.Mapping[str,str]]=None, instance_id: typing.Optional[str]=None) -> "IInstance":
        """Registers a resource that is accessible using values other than an IP address or a domain name (CNAME).

        :param id: -
        :param props: -
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        """
        props = NonIpInstanceBaseProps(custom_attributes=custom_attributes, instance_id=instance_id)

        return jsii.invoke(self, "registerNonIpInstance", [id, props])

    @property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> "DnsRecordType":
        """The DnsRecordType used by the service."""
        return jsii.get(self, "dnsRecordType")

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> "INamespace":
        """The namespace for the Cloudmap Service."""
        return jsii.get(self, "namespace")

    @property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        """The Routing Policy used by the service."""
        return jsii.get(self, "routingPolicy")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Arn of the namespace that you want to use for DNS configuration."""
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> str:
        """The ID of the namespace that you want to use for DNS configuration."""
        return jsii.get(self, "serviceId")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """A name for the Cloudmap Service."""
        return jsii.get(self, "serviceName")


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.ServiceAttributes", jsii_struct_bases=[], name_mapping={'dns_record_type': 'dnsRecordType', 'namespace': 'namespace', 'routing_policy': 'routingPolicy', 'service_arn': 'serviceArn', 'service_id': 'serviceId', 'service_name': 'serviceName'})
class ServiceAttributes():
    def __init__(self, *, dns_record_type: "DnsRecordType", namespace: "INamespace", routing_policy: "RoutingPolicy", service_arn: str, service_id: str, service_name: str):
        """
        :param dns_record_type: 
        :param namespace: 
        :param routing_policy: 
        :param service_arn: 
        :param service_id: 
        :param service_name: 
        """
        self._values = {
            'dns_record_type': dns_record_type,
            'namespace': namespace,
            'routing_policy': routing_policy,
            'service_arn': service_arn,
            'service_id': service_id,
            'service_name': service_name,
        }

    @property
    def dns_record_type(self) -> "DnsRecordType":
        return self._values.get('dns_record_type')

    @property
    def namespace(self) -> "INamespace":
        return self._values.get('namespace')

    @property
    def routing_policy(self) -> "RoutingPolicy":
        return self._values.get('routing_policy')

    @property
    def service_arn(self) -> str:
        return self._values.get('service_arn')

    @property
    def service_id(self) -> str:
        return self._values.get('service_id')

    @property
    def service_name(self) -> str:
        return self._values.get('service_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServiceAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-servicediscovery.ServiceProps", jsii_struct_bases=[DnsServiceProps], name_mapping={'custom_health_check': 'customHealthCheck', 'description': 'description', 'health_check': 'healthCheck', 'name': 'name', 'dns_record_type': 'dnsRecordType', 'dns_ttl': 'dnsTtl', 'load_balancer': 'loadBalancer', 'routing_policy': 'routingPolicy', 'namespace': 'namespace'})
class ServiceProps(DnsServiceProps):
    def __init__(self, *, custom_health_check: typing.Optional["HealthCheckCustomConfig"]=None, description: typing.Optional[str]=None, health_check: typing.Optional["HealthCheckConfig"]=None, name: typing.Optional[str]=None, dns_record_type: typing.Optional["DnsRecordType"]=None, dns_ttl: typing.Optional[aws_cdk.core.Duration]=None, load_balancer: typing.Optional[bool]=None, routing_policy: typing.Optional["RoutingPolicy"]=None, namespace: "INamespace"):
        """
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html. Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param namespace: The ID of the namespace that you want to use for DNS configuration.
        """
        if isinstance(custom_health_check, dict): custom_health_check = HealthCheckCustomConfig(**custom_health_check)
        if isinstance(health_check, dict): health_check = HealthCheckConfig(**health_check)
        self._values = {
            'namespace': namespace,
        }
        if custom_health_check is not None: self._values["custom_health_check"] = custom_health_check
        if description is not None: self._values["description"] = description
        if health_check is not None: self._values["health_check"] = health_check
        if name is not None: self._values["name"] = name
        if dns_record_type is not None: self._values["dns_record_type"] = dns_record_type
        if dns_ttl is not None: self._values["dns_ttl"] = dns_ttl
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if routing_policy is not None: self._values["routing_policy"] = routing_policy

    @property
    def custom_health_check(self) -> typing.Optional["HealthCheckCustomConfig"]:
        """Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html.

        default
        :default: none
        """
        return self._values.get('custom_health_check')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the service.

        default
        :default: none
        """
        return self._values.get('description')

    @property
    def health_check(self) -> typing.Optional["HealthCheckConfig"]:
        """Settings for an optional health check.

        If you specify health check settings, AWS Cloud Map associates the health
        check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can
        be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to
        this service.

        default
        :default: none
        """
        return self._values.get('health_check')

    @property
    def name(self) -> typing.Optional[str]:
        """A name for the Service.

        default
        :default: CloudFormation-generated name
        """
        return self._values.get('name')

    @property
    def dns_record_type(self) -> typing.Optional["DnsRecordType"]:
        """The DNS type of the record that you want AWS Cloud Map to create.

        Supported record types
        include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV.

        default
        :default: A
        """
        return self._values.get('dns_record_type')

    @property
    def dns_ttl(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record.

        default
        :default: Duration.minutes(1)
        """
        return self._values.get('dns_ttl')

    @property
    def load_balancer(self) -> typing.Optional[bool]:
        """Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance.

        Setting this to ``true`` correctly configures the ``routingPolicy``
        and performs some additional validation.

        default
        :default: false
        """
        return self._values.get('load_balancer')

    @property
    def routing_policy(self) -> typing.Optional["RoutingPolicy"]:
        """The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service.

        default
        :default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        """
        return self._values.get('routing_policy')

    @property
    def namespace(self) -> "INamespace":
        """The ID of the namespace that you want to use for DNS configuration."""
        return self._values.get('namespace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["AliasTargetInstance", "AliasTargetInstanceProps", "BaseInstanceProps", "BaseNamespaceProps", "BaseServiceProps", "CfnHttpNamespace", "CfnHttpNamespaceProps", "CfnInstance", "CfnInstanceProps", "CfnPrivateDnsNamespace", "CfnPrivateDnsNamespaceProps", "CfnPublicDnsNamespace", "CfnPublicDnsNamespaceProps", "CfnService", "CfnServiceProps", "CnameInstance", "CnameInstanceBaseProps", "CnameInstanceProps", "DnsRecordType", "DnsServiceProps", "HealthCheckConfig", "HealthCheckCustomConfig", "HealthCheckType", "HttpNamespace", "HttpNamespaceAttributes", "HttpNamespaceProps", "IHttpNamespace", "IInstance", "INamespace", "IPrivateDnsNamespace", "IPublicDnsNamespace", "IService", "InstanceBase", "IpInstance", "IpInstanceBaseProps", "IpInstanceProps", "NamespaceType", "NonIpInstance", "NonIpInstanceBaseProps", "NonIpInstanceProps", "PrivateDnsNamespace", "PrivateDnsNamespaceAttributes", "PrivateDnsNamespaceProps", "PublicDnsNamespace", "PublicDnsNamespaceAttributes", "PublicDnsNamespaceProps", "RoutingPolicy", "Service", "ServiceAttributes", "ServiceProps", "__jsii_assembly__"]

publication.publish()
