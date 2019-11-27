"""
## Amazon Elastic Load Balancing Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

The `@aws-cdk/aws-elasticloadbalancing` package provides constructs for configuring
classic load balancers.

### Configuring a Load Balancer

Load balancers send traffic to one or more AutoScalingGroups. Create a load
balancer, set up listeners and a health check, and supply the fleet(s) you want
to load balance to in the `targets` property.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
lb = elb.LoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True,
    health_check={
        "port": 80
    }
)

lb.add_target(my_auto_scaling_group)
lb.add_listener(
    external_port=80
)
```

The load balancer allows all connections by default. If you want to change that,
pass the `allowConnectionsFrom` property while setting up the listener:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
lb.add_listener(
    external_port=80,
    allow_connections_from=[my_security_group]
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

import aws_cdk.aws_ec2
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticloadbalancing", "1.18.0", __name__, "aws-elasticloadbalancing@1.18.0.jsii.tgz")
@jsii.implements(aws_cdk.core.IInspectable)
class CfnLoadBalancer(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer"):
    """A CloudFormation ``AWS::ElasticLoadBalancing::LoadBalancer``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html
    cloudformationResource:
    :cloudformationResource:: AWS::ElasticLoadBalancing::LoadBalancer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, listeners: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ListenersProperty", aws_cdk.core.IResolvable]]], access_logging_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLoggingPolicyProperty"]]]=None, app_cookie_stickiness_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AppCookieStickinessPolicyProperty"]]]]]=None, availability_zones: typing.Optional[typing.List[str]]=None, connection_draining_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionDrainingPolicyProperty"]]]=None, connection_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionSettingsProperty"]]]=None, cross_zone: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, health_check: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckProperty"]]]=None, instances: typing.Optional[typing.List[str]]=None, lb_cookie_stickiness_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LBCookieStickinessPolicyProperty"]]]]]=None, load_balancer_name: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PoliciesProperty"]]]]]=None, scheme: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, subnets: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ElasticLoadBalancing::LoadBalancer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param listeners: ``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.
        :param access_logging_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.
        :param app_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.
        :param availability_zones: ``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.
        :param connection_draining_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.
        :param connection_settings: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.
        :param cross_zone: ``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.
        :param health_check: ``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.
        :param instances: ``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.
        :param lb_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.
        :param load_balancer_name: ``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.
        :param policies: ``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.
        :param scheme: ``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.
        :param subnets: ``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.
        """
        props = CfnLoadBalancerProps(listeners=listeners, access_logging_policy=access_logging_policy, app_cookie_stickiness_policy=app_cookie_stickiness_policy, availability_zones=availability_zones, connection_draining_policy=connection_draining_policy, connection_settings=connection_settings, cross_zone=cross_zone, health_check=health_check, instances=instances, lb_cookie_stickiness_policy=lb_cookie_stickiness_policy, load_balancer_name=load_balancer_name, policies=policies, scheme=scheme, security_groups=security_groups, subnets=subnets, tags=tags)

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCanonicalHostedZoneName")
    def attr_canonical_hosted_zone_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CanonicalHostedZoneName
        """
        return jsii.get(self, "attrCanonicalHostedZoneName")

    @property
    @jsii.member(jsii_name="attrCanonicalHostedZoneNameId")
    def attr_canonical_hosted_zone_name_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CanonicalHostedZoneNameID
        """
        return jsii.get(self, "attrCanonicalHostedZoneNameId")

    @property
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DNSName
        """
        return jsii.get(self, "attrDnsName")

    @property
    @jsii.member(jsii_name="attrSourceSecurityGroupGroupName")
    def attr_source_security_group_group_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SourceSecurityGroup.GroupName
        """
        return jsii.get(self, "attrSourceSecurityGroupGroupName")

    @property
    @jsii.member(jsii_name="attrSourceSecurityGroupOwnerAlias")
    def attr_source_security_group_owner_alias(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: SourceSecurityGroup.OwnerAlias
        """
        return jsii.get(self, "attrSourceSecurityGroupOwnerAlias")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-elasticloadbalancing-loadbalancer-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="listeners")
    def listeners(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ListenersProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-listeners
        """
        return jsii.get(self, "listeners")

    @listeners.setter
    def listeners(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ListenersProperty", aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "listeners", value)

    @property
    @jsii.member(jsii_name="accessLoggingPolicy")
    def access_logging_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLoggingPolicyProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-accessloggingpolicy
        """
        return jsii.get(self, "accessLoggingPolicy")

    @access_logging_policy.setter
    def access_logging_policy(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AccessLoggingPolicyProperty"]]]):
        return jsii.set(self, "accessLoggingPolicy", value)

    @property
    @jsii.member(jsii_name="appCookieStickinessPolicy")
    def app_cookie_stickiness_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AppCookieStickinessPolicyProperty"]]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-appcookiestickinesspolicy
        """
        return jsii.get(self, "appCookieStickinessPolicy")

    @app_cookie_stickiness_policy.setter
    def app_cookie_stickiness_policy(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "AppCookieStickinessPolicyProperty"]]]]]):
        return jsii.set(self, "appCookieStickinessPolicy", value)

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter
    def availability_zones(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "availabilityZones", value)

    @property
    @jsii.member(jsii_name="connectionDrainingPolicy")
    def connection_draining_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionDrainingPolicyProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectiondrainingpolicy
        """
        return jsii.get(self, "connectionDrainingPolicy")

    @connection_draining_policy.setter
    def connection_draining_policy(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionDrainingPolicyProperty"]]]):
        return jsii.set(self, "connectionDrainingPolicy", value)

    @property
    @jsii.member(jsii_name="connectionSettings")
    def connection_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionSettingsProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectionsettings
        """
        return jsii.get(self, "connectionSettings")

    @connection_settings.setter
    def connection_settings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionSettingsProperty"]]]):
        return jsii.set(self, "connectionSettings", value)

    @property
    @jsii.member(jsii_name="crossZone")
    def cross_zone(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-crosszone
        """
        return jsii.get(self, "crossZone")

    @cross_zone.setter
    def cross_zone(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "crossZone", value)

    @property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-healthcheck
        """
        return jsii.get(self, "healthCheck")

    @health_check.setter
    def health_check(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["HealthCheckProperty"]]]):
        return jsii.set(self, "healthCheck", value)

    @property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-instances
        """
        return jsii.get(self, "instances")

    @instances.setter
    def instances(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "instances", value)

    @property
    @jsii.member(jsii_name="lbCookieStickinessPolicy")
    def lb_cookie_stickiness_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LBCookieStickinessPolicyProperty"]]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-lbcookiestickinesspolicy
        """
        return jsii.get(self, "lbCookieStickinessPolicy")

    @lb_cookie_stickiness_policy.setter
    def lb_cookie_stickiness_policy(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LBCookieStickinessPolicyProperty"]]]]]):
        return jsii.set(self, "lbCookieStickinessPolicy", value)

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-elbname
        """
        return jsii.get(self, "loadBalancerName")

    @load_balancer_name.setter
    def load_balancer_name(self, value: typing.Optional[str]):
        return jsii.set(self, "loadBalancerName", value)

    @property
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PoliciesProperty"]]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-policies
        """
        return jsii.get(self, "policies")

    @policies.setter
    def policies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "PoliciesProperty"]]]]]):
        return jsii.set(self, "policies", value)

    @property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-scheme
        """
        return jsii.get(self, "scheme")

    @scheme.setter
    def scheme(self, value: typing.Optional[str]):
        return jsii.set(self, "scheme", value)

    @property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter
    def security_groups(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "securityGroups", value)

    @property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-subnets
        """
        return jsii.get(self, "subnets")

    @subnets.setter
    def subnets(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "subnets", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.AccessLoggingPolicyProperty", jsii_struct_bases=[], name_mapping={'enabled': 'enabled', 's3_bucket_name': 's3BucketName', 'emit_interval': 'emitInterval', 's3_bucket_prefix': 's3BucketPrefix'})
    class AccessLoggingPolicyProperty():
        def __init__(self, *, enabled: typing.Union[bool, aws_cdk.core.IResolvable], s3_bucket_name: str, emit_interval: typing.Optional[jsii.Number]=None, s3_bucket_prefix: typing.Optional[str]=None):
            """
            :param enabled: ``CfnLoadBalancer.AccessLoggingPolicyProperty.Enabled``.
            :param s3_bucket_name: ``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketName``.
            :param emit_interval: ``CfnLoadBalancer.AccessLoggingPolicyProperty.EmitInterval``.
            :param s3_bucket_prefix: ``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html
            """
            self._values = {
                'enabled': enabled,
                's3_bucket_name': s3_bucket_name,
            }
            if emit_interval is not None: self._values["emit_interval"] = emit_interval
            if s3_bucket_prefix is not None: self._values["s3_bucket_prefix"] = s3_bucket_prefix

        @property
        def enabled(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-enabled
            """
            return self._values.get('enabled')

        @property
        def s3_bucket_name(self) -> str:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-s3bucketname
            """
            return self._values.get('s3_bucket_name')

        @property
        def emit_interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.EmitInterval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-emitinterval
            """
            return self._values.get('emit_interval')

        @property
        def s3_bucket_prefix(self) -> typing.Optional[str]:
            """``CfnLoadBalancer.AccessLoggingPolicyProperty.S3BucketPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-accessloggingpolicy.html#cfn-elb-accessloggingpolicy-s3bucketprefix
            """
            return self._values.get('s3_bucket_prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccessLoggingPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.AppCookieStickinessPolicyProperty", jsii_struct_bases=[], name_mapping={'cookie_name': 'cookieName', 'policy_name': 'policyName'})
    class AppCookieStickinessPolicyProperty():
        def __init__(self, *, cookie_name: str, policy_name: str):
            """
            :param cookie_name: ``CfnLoadBalancer.AppCookieStickinessPolicyProperty.CookieName``.
            :param policy_name: ``CfnLoadBalancer.AppCookieStickinessPolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html
            """
            self._values = {
                'cookie_name': cookie_name,
                'policy_name': policy_name,
            }

        @property
        def cookie_name(self) -> str:
            """``CfnLoadBalancer.AppCookieStickinessPolicyProperty.CookieName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html#cfn-elb-appcookiestickinesspolicy-cookiename
            """
            return self._values.get('cookie_name')

        @property
        def policy_name(self) -> str:
            """``CfnLoadBalancer.AppCookieStickinessPolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-AppCookieStickinessPolicy.html#cfn-elb-appcookiestickinesspolicy-policyname
            """
            return self._values.get('policy_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AppCookieStickinessPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ConnectionDrainingPolicyProperty", jsii_struct_bases=[], name_mapping={'enabled': 'enabled', 'timeout': 'timeout'})
    class ConnectionDrainingPolicyProperty():
        def __init__(self, *, enabled: typing.Union[bool, aws_cdk.core.IResolvable], timeout: typing.Optional[jsii.Number]=None):
            """
            :param enabled: ``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Enabled``.
            :param timeout: ``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html
            """
            self._values = {
                'enabled': enabled,
            }
            if timeout is not None: self._values["timeout"] = timeout

        @property
        def enabled(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html#cfn-elb-connectiondrainingpolicy-enabled
            """
            return self._values.get('enabled')

        @property
        def timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnLoadBalancer.ConnectionDrainingPolicyProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectiondrainingpolicy.html#cfn-elb-connectiondrainingpolicy-timeout
            """
            return self._values.get('timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConnectionDrainingPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ConnectionSettingsProperty", jsii_struct_bases=[], name_mapping={'idle_timeout': 'idleTimeout'})
    class ConnectionSettingsProperty():
        def __init__(self, *, idle_timeout: jsii.Number):
            """
            :param idle_timeout: ``CfnLoadBalancer.ConnectionSettingsProperty.IdleTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectionsettings.html
            """
            self._values = {
                'idle_timeout': idle_timeout,
            }

        @property
        def idle_timeout(self) -> jsii.Number:
            """``CfnLoadBalancer.ConnectionSettingsProperty.IdleTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-connectionsettings.html#cfn-elb-connectionsettings-idletimeout
            """
            return self._values.get('idle_timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConnectionSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.HealthCheckProperty", jsii_struct_bases=[], name_mapping={'healthy_threshold': 'healthyThreshold', 'interval': 'interval', 'target': 'target', 'timeout': 'timeout', 'unhealthy_threshold': 'unhealthyThreshold'})
    class HealthCheckProperty():
        def __init__(self, *, healthy_threshold: str, interval: str, target: str, timeout: str, unhealthy_threshold: str):
            """
            :param healthy_threshold: ``CfnLoadBalancer.HealthCheckProperty.HealthyThreshold``.
            :param interval: ``CfnLoadBalancer.HealthCheckProperty.Interval``.
            :param target: ``CfnLoadBalancer.HealthCheckProperty.Target``.
            :param timeout: ``CfnLoadBalancer.HealthCheckProperty.Timeout``.
            :param unhealthy_threshold: ``CfnLoadBalancer.HealthCheckProperty.UnhealthyThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html
            """
            self._values = {
                'healthy_threshold': healthy_threshold,
                'interval': interval,
                'target': target,
                'timeout': timeout,
                'unhealthy_threshold': unhealthy_threshold,
            }

        @property
        def healthy_threshold(self) -> str:
            """``CfnLoadBalancer.HealthCheckProperty.HealthyThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-healthythreshold
            """
            return self._values.get('healthy_threshold')

        @property
        def interval(self) -> str:
            """``CfnLoadBalancer.HealthCheckProperty.Interval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-interval
            """
            return self._values.get('interval')

        @property
        def target(self) -> str:
            """``CfnLoadBalancer.HealthCheckProperty.Target``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-target
            """
            return self._values.get('target')

        @property
        def timeout(self) -> str:
            """``CfnLoadBalancer.HealthCheckProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-timeout
            """
            return self._values.get('timeout')

        @property
        def unhealthy_threshold(self) -> str:
            """``CfnLoadBalancer.HealthCheckProperty.UnhealthyThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-health-check.html#cfn-elb-healthcheck-unhealthythreshold
            """
            return self._values.get('unhealthy_threshold')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.LBCookieStickinessPolicyProperty", jsii_struct_bases=[], name_mapping={'cookie_expiration_period': 'cookieExpirationPeriod', 'policy_name': 'policyName'})
    class LBCookieStickinessPolicyProperty():
        def __init__(self, *, cookie_expiration_period: typing.Optional[str]=None, policy_name: typing.Optional[str]=None):
            """
            :param cookie_expiration_period: ``CfnLoadBalancer.LBCookieStickinessPolicyProperty.CookieExpirationPeriod``.
            :param policy_name: ``CfnLoadBalancer.LBCookieStickinessPolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html
            """
            self._values = {
            }
            if cookie_expiration_period is not None: self._values["cookie_expiration_period"] = cookie_expiration_period
            if policy_name is not None: self._values["policy_name"] = policy_name

        @property
        def cookie_expiration_period(self) -> typing.Optional[str]:
            """``CfnLoadBalancer.LBCookieStickinessPolicyProperty.CookieExpirationPeriod``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html#cfn-elb-lbcookiestickinesspolicy-cookieexpirationperiod
            """
            return self._values.get('cookie_expiration_period')

        @property
        def policy_name(self) -> typing.Optional[str]:
            """``CfnLoadBalancer.LBCookieStickinessPolicyProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-LBCookieStickinessPolicy.html#cfn-elb-lbcookiestickinesspolicy-policyname
            """
            return self._values.get('policy_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LBCookieStickinessPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.ListenersProperty", jsii_struct_bases=[], name_mapping={'instance_port': 'instancePort', 'load_balancer_port': 'loadBalancerPort', 'protocol': 'protocol', 'instance_protocol': 'instanceProtocol', 'policy_names': 'policyNames', 'ssl_certificate_id': 'sslCertificateId'})
    class ListenersProperty():
        def __init__(self, *, instance_port: str, load_balancer_port: str, protocol: str, instance_protocol: typing.Optional[str]=None, policy_names: typing.Optional[typing.List[str]]=None, ssl_certificate_id: typing.Optional[str]=None):
            """
            :param instance_port: ``CfnLoadBalancer.ListenersProperty.InstancePort``.
            :param load_balancer_port: ``CfnLoadBalancer.ListenersProperty.LoadBalancerPort``.
            :param protocol: ``CfnLoadBalancer.ListenersProperty.Protocol``.
            :param instance_protocol: ``CfnLoadBalancer.ListenersProperty.InstanceProtocol``.
            :param policy_names: ``CfnLoadBalancer.ListenersProperty.PolicyNames``.
            :param ssl_certificate_id: ``CfnLoadBalancer.ListenersProperty.SSLCertificateId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html
            """
            self._values = {
                'instance_port': instance_port,
                'load_balancer_port': load_balancer_port,
                'protocol': protocol,
            }
            if instance_protocol is not None: self._values["instance_protocol"] = instance_protocol
            if policy_names is not None: self._values["policy_names"] = policy_names
            if ssl_certificate_id is not None: self._values["ssl_certificate_id"] = ssl_certificate_id

        @property
        def instance_port(self) -> str:
            """``CfnLoadBalancer.ListenersProperty.InstancePort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-instanceport
            """
            return self._values.get('instance_port')

        @property
        def load_balancer_port(self) -> str:
            """``CfnLoadBalancer.ListenersProperty.LoadBalancerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-loadbalancerport
            """
            return self._values.get('load_balancer_port')

        @property
        def protocol(self) -> str:
            """``CfnLoadBalancer.ListenersProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-protocol
            """
            return self._values.get('protocol')

        @property
        def instance_protocol(self) -> typing.Optional[str]:
            """``CfnLoadBalancer.ListenersProperty.InstanceProtocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-instanceprotocol
            """
            return self._values.get('instance_protocol')

        @property
        def policy_names(self) -> typing.Optional[typing.List[str]]:
            """``CfnLoadBalancer.ListenersProperty.PolicyNames``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-policynames
            """
            return self._values.get('policy_names')

        @property
        def ssl_certificate_id(self) -> typing.Optional[str]:
            """``CfnLoadBalancer.ListenersProperty.SSLCertificateId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-listener.html#cfn-ec2-elb-listener-sslcertificateid
            """
            return self._values.get('ssl_certificate_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ListenersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancer.PoliciesProperty", jsii_struct_bases=[], name_mapping={'attributes': 'attributes', 'policy_name': 'policyName', 'policy_type': 'policyType', 'instance_ports': 'instancePorts', 'load_balancer_ports': 'loadBalancerPorts'})
    class PoliciesProperty():
        def __init__(self, *, attributes: typing.Union[typing.List[typing.Any], aws_cdk.core.IResolvable], policy_name: str, policy_type: str, instance_ports: typing.Optional[typing.List[str]]=None, load_balancer_ports: typing.Optional[typing.List[str]]=None):
            """
            :param attributes: ``CfnLoadBalancer.PoliciesProperty.Attributes``.
            :param policy_name: ``CfnLoadBalancer.PoliciesProperty.PolicyName``.
            :param policy_type: ``CfnLoadBalancer.PoliciesProperty.PolicyType``.
            :param instance_ports: ``CfnLoadBalancer.PoliciesProperty.InstancePorts``.
            :param load_balancer_ports: ``CfnLoadBalancer.PoliciesProperty.LoadBalancerPorts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html
            """
            self._values = {
                'attributes': attributes,
                'policy_name': policy_name,
                'policy_type': policy_type,
            }
            if instance_ports is not None: self._values["instance_ports"] = instance_ports
            if load_balancer_ports is not None: self._values["load_balancer_ports"] = load_balancer_ports

        @property
        def attributes(self) -> typing.Union[typing.List[typing.Any], aws_cdk.core.IResolvable]:
            """``CfnLoadBalancer.PoliciesProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-attributes
            """
            return self._values.get('attributes')

        @property
        def policy_name(self) -> str:
            """``CfnLoadBalancer.PoliciesProperty.PolicyName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-policyname
            """
            return self._values.get('policy_name')

        @property
        def policy_type(self) -> str:
            """``CfnLoadBalancer.PoliciesProperty.PolicyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-policytype
            """
            return self._values.get('policy_type')

        @property
        def instance_ports(self) -> typing.Optional[typing.List[str]]:
            """``CfnLoadBalancer.PoliciesProperty.InstancePorts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-instanceports
            """
            return self._values.get('instance_ports')

        @property
        def load_balancer_ports(self) -> typing.Optional[typing.List[str]]:
            """``CfnLoadBalancer.PoliciesProperty.LoadBalancerPorts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb-policy.html#cfn-ec2-elb-policy-loadbalancerports
            """
            return self._values.get('load_balancer_ports')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PoliciesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.CfnLoadBalancerProps", jsii_struct_bases=[], name_mapping={'listeners': 'listeners', 'access_logging_policy': 'accessLoggingPolicy', 'app_cookie_stickiness_policy': 'appCookieStickinessPolicy', 'availability_zones': 'availabilityZones', 'connection_draining_policy': 'connectionDrainingPolicy', 'connection_settings': 'connectionSettings', 'cross_zone': 'crossZone', 'health_check': 'healthCheck', 'instances': 'instances', 'lb_cookie_stickiness_policy': 'lbCookieStickinessPolicy', 'load_balancer_name': 'loadBalancerName', 'policies': 'policies', 'scheme': 'scheme', 'security_groups': 'securityGroups', 'subnets': 'subnets', 'tags': 'tags'})
class CfnLoadBalancerProps():
    def __init__(self, *, listeners: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", aws_cdk.core.IResolvable]]], access_logging_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.AccessLoggingPolicyProperty"]]]=None, app_cookie_stickiness_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AppCookieStickinessPolicyProperty"]]]]]=None, availability_zones: typing.Optional[typing.List[str]]=None, connection_draining_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.ConnectionDrainingPolicyProperty"]]]=None, connection_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.ConnectionSettingsProperty"]]]=None, cross_zone: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, health_check: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.HealthCheckProperty"]]]=None, instances: typing.Optional[typing.List[str]]=None, lb_cookie_stickiness_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LBCookieStickinessPolicyProperty"]]]]]=None, load_balancer_name: typing.Optional[str]=None, policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.PoliciesProperty"]]]]]=None, scheme: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, subnets: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::ElasticLoadBalancing::LoadBalancer``.

        :param listeners: ``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.
        :param access_logging_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.
        :param app_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.
        :param availability_zones: ``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.
        :param connection_draining_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.
        :param connection_settings: ``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.
        :param cross_zone: ``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.
        :param health_check: ``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.
        :param instances: ``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.
        :param lb_cookie_stickiness_policy: ``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.
        :param load_balancer_name: ``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.
        :param policies: ``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.
        :param scheme: ``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.
        :param subnets: ``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html
        """
        self._values = {
            'listeners': listeners,
        }
        if access_logging_policy is not None: self._values["access_logging_policy"] = access_logging_policy
        if app_cookie_stickiness_policy is not None: self._values["app_cookie_stickiness_policy"] = app_cookie_stickiness_policy
        if availability_zones is not None: self._values["availability_zones"] = availability_zones
        if connection_draining_policy is not None: self._values["connection_draining_policy"] = connection_draining_policy
        if connection_settings is not None: self._values["connection_settings"] = connection_settings
        if cross_zone is not None: self._values["cross_zone"] = cross_zone
        if health_check is not None: self._values["health_check"] = health_check
        if instances is not None: self._values["instances"] = instances
        if lb_cookie_stickiness_policy is not None: self._values["lb_cookie_stickiness_policy"] = lb_cookie_stickiness_policy
        if load_balancer_name is not None: self._values["load_balancer_name"] = load_balancer_name
        if policies is not None: self._values["policies"] = policies
        if scheme is not None: self._values["scheme"] = scheme
        if security_groups is not None: self._values["security_groups"] = security_groups
        if subnets is not None: self._values["subnets"] = subnets
        if tags is not None: self._values["tags"] = tags

    @property
    def listeners(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnLoadBalancer.ListenersProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Listeners``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-listeners
        """
        return self._values.get('listeners')

    @property
    def access_logging_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.AccessLoggingPolicyProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AccessLoggingPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-accessloggingpolicy
        """
        return self._values.get('access_logging_policy')

    @property
    def app_cookie_stickiness_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.AppCookieStickinessPolicyProperty"]]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AppCookieStickinessPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-appcookiestickinesspolicy
        """
        return self._values.get('app_cookie_stickiness_policy')

    @property
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-availabilityzones
        """
        return self._values.get('availability_zones')

    @property
    def connection_draining_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.ConnectionDrainingPolicyProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionDrainingPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectiondrainingpolicy
        """
        return self._values.get('connection_draining_policy')

    @property
    def connection_settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.ConnectionSettingsProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.ConnectionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-connectionsettings
        """
        return self._values.get('connection_settings')

    @property
    def cross_zone(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.CrossZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-crosszone
        """
        return self._values.get('cross_zone')

    @property
    def health_check(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnLoadBalancer.HealthCheckProperty"]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.HealthCheck``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-healthcheck
        """
        return self._values.get('health_check')

    @property
    def instances(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Instances``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-instances
        """
        return self._values.get('instances')

    @property
    def lb_cookie_stickiness_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.LBCookieStickinessPolicyProperty"]]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LBCookieStickinessPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-lbcookiestickinesspolicy
        """
        return self._values.get('lb_cookie_stickiness_policy')

    @property
    def load_balancer_name(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.LoadBalancerName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-elbname
        """
        return self._values.get('load_balancer_name')

    @property
    def policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLoadBalancer.PoliciesProperty"]]]]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Policies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-policies
        """
        return self._values.get('policies')

    @property
    def scheme(self) -> typing.Optional[str]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Scheme``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-scheme
        """
        return self._values.get('scheme')

    @property
    def security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-securitygroups
        """
        return self._values.get('security_groups')

    @property
    def subnets(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-ec2-elb-subnets
        """
        return self._values.get('subnets')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ElasticLoadBalancing::LoadBalancer.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-elb.html#cfn-elasticloadbalancing-loadbalancer-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.HealthCheck", jsii_struct_bases=[], name_mapping={'port': 'port', 'healthy_threshold': 'healthyThreshold', 'interval': 'interval', 'path': 'path', 'protocol': 'protocol', 'timeout': 'timeout', 'unhealthy_threshold': 'unhealthyThreshold'})
class HealthCheck():
    def __init__(self, *, port: jsii.Number, healthy_threshold: typing.Optional[jsii.Number]=None, interval: typing.Optional[aws_cdk.core.Duration]=None, path: typing.Optional[str]=None, protocol: typing.Optional["LoadBalancingProtocol"]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, unhealthy_threshold: typing.Optional[jsii.Number]=None):
        """Describe the health check to a load balancer.

        :param port: What port number to health check on.
        :param healthy_threshold: After how many successful checks is an instance considered healthy. Default: 2
        :param interval: Number of seconds between health checks. Default: Duration.seconds(30)
        :param path: What path to use for HTTP or HTTPS health check (must return 200). For SSL and TCP health checks, accepting connections is enough to be considered healthy. Default: "/"
        :param protocol: What protocol to use for health checking. The protocol is automatically determined from the port if it's not supplied. Default: Automatic
        :param timeout: Health check timeout. Default: Duration.seconds(5)
        :param unhealthy_threshold: After how many unsuccessful checks is an instance considered unhealthy. Default: 5
        """
        self._values = {
            'port': port,
        }
        if healthy_threshold is not None: self._values["healthy_threshold"] = healthy_threshold
        if interval is not None: self._values["interval"] = interval
        if path is not None: self._values["path"] = path
        if protocol is not None: self._values["protocol"] = protocol
        if timeout is not None: self._values["timeout"] = timeout
        if unhealthy_threshold is not None: self._values["unhealthy_threshold"] = unhealthy_threshold

    @property
    def port(self) -> jsii.Number:
        """What port number to health check on."""
        return self._values.get('port')

    @property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        """After how many successful checks is an instance considered healthy.

        default
        :default: 2
        """
        return self._values.get('healthy_threshold')

    @property
    def interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Number of seconds between health checks.

        default
        :default: Duration.seconds(30)
        """
        return self._values.get('interval')

    @property
    def path(self) -> typing.Optional[str]:
        """What path to use for HTTP or HTTPS health check (must return 200).

        For SSL and TCP health checks, accepting connections is enough to be considered
        healthy.

        default
        :default: "/"
        """
        return self._values.get('path')

    @property
    def protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        """What protocol to use for health checking.

        The protocol is automatically determined from the port if it's not supplied.

        default
        :default: Automatic
        """
        return self._values.get('protocol')

    @property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Health check timeout.

        default
        :default: Duration.seconds(5)
        """
        return self._values.get('timeout')

    @property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        """After how many unsuccessful checks is an instance considered unhealthy.

        default
        :default: 5
        """
        return self._values.get('unhealthy_threshold')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HealthCheck(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-elasticloadbalancing.ILoadBalancerTarget")
class ILoadBalancerTarget(aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """Interface that is going to be implemented by constructs that you can load balance to."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerTargetProxy

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        """Attach load-balanced target to a classic ELB.

        :param load_balancer: [disable-awslint:ref-via-interface] The load balancer to attach the target to.
        """
        ...


class _ILoadBalancerTargetProxy(jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """Interface that is going to be implemented by constructs that you can load balance to."""
    __jsii_type__ = "@aws-cdk/aws-elasticloadbalancing.ILoadBalancerTarget"
    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: "LoadBalancer") -> None:
        """Attach load-balanced target to a classic ELB.

        :param load_balancer: [disable-awslint:ref-via-interface] The load balancer to attach the target to.
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class ListenerPort(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancing.ListenerPort"):
    """Reference to a listener's port just created.

    This implements IConnectable with a default port (the port that an ELB
    listener was just created on) for a given security group so that it can be
    conveniently used just like any Connectable. E.g::

       const listener = elb.addListener(...);

       listener.connections.allowDefaultPortFromAnyIPv4();
       // or
       instance.connections.allowToDefaultPort(listener);
    """
    def __init__(self, security_group: aws_cdk.aws_ec2.ISecurityGroup, default_port: aws_cdk.aws_ec2.Port) -> None:
        """
        :param security_group: -
        :param default_port: -
        """
        jsii.create(ListenerPort, self, [security_group, default_port])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class LoadBalancer(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancer"):
    """A load balancer with a single listener.

    Routes to a fleet of of instances in a VPC.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpc, cross_zone: typing.Optional[bool]=None, health_check: typing.Optional["HealthCheck"]=None, internet_facing: typing.Optional[bool]=None, listeners: typing.Optional[typing.List["LoadBalancerListener"]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, targets: typing.Optional[typing.List["ILoadBalancerTarget"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param vpc: VPC network of the fleet instances.
        :param cross_zone: Whether cross zone load balancing is enabled. This controls whether the load balancer evenly distributes requests across each availability zone Default: true
        :param health_check: Health check settings for the load balancing targets. Not required but recommended. Default: - None.
        :param internet_facing: Whether this is an internet-facing Load Balancer. This controls whether the LB has a public IP address assigned. It does not open up the Load Balancer's security groups to public internet access. Default: false
        :param listeners: What listeners to set up for the load balancer. Can also be added by .addListener() Default: -
        :param subnet_selection: Which subnets to deploy the load balancer. Can be used to define a specific set of subnets to deploy the load balancer to. Useful multiple public or private subnets are covering the same availability zone. Default: - Public subnets if internetFacing, Private subnets otherwise
        :param targets: What targets to load balance to. Can also be added by .addTarget() Default: - None.
        """
        props = LoadBalancerProps(vpc=vpc, cross_zone=cross_zone, health_check=health_check, internet_facing=internet_facing, listeners=listeners, subnet_selection=subnet_selection, targets=targets)

        jsii.create(LoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="addListener")
    def add_listener(self, *, external_port: jsii.Number, allow_connections_from: typing.Optional[typing.List[aws_cdk.aws_ec2.IConnectable]]=None, external_protocol: typing.Optional["LoadBalancingProtocol"]=None, internal_port: typing.Optional[jsii.Number]=None, internal_protocol: typing.Optional["LoadBalancingProtocol"]=None, policy_names: typing.Optional[typing.List[str]]=None, ssl_certificate_id: typing.Optional[str]=None) -> "ListenerPort":
        """Add a backend to the load balancer.

        :param listener: -
        :param external_port: External listening port.
        :param allow_connections_from: Allow connections to the load balancer from the given set of connection peers. By default, connections will be allowed from anywhere. Set this to an empty list to deny connections, or supply a custom list of peers to allow connections from (IP ranges or security groups). Default: Anywhere
        :param external_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the external port is either 80 or 443.
        :param internal_port: Instance listening port. Same as the externalPort if not specified. Default: externalPort
        :param internal_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the internal port is either 80 or 443. The instance protocol is 'tcp' if the front-end protocol is 'tcp' or 'ssl', the instance protocol is 'http' if the front-end protocol is 'https'.
        :param policy_names: SSL policy names.
        :param ssl_certificate_id: ID of SSL certificate.

        return
        :return: A ListenerPort object that controls connections to the listener port
        """
        listener = LoadBalancerListener(external_port=external_port, allow_connections_from=allow_connections_from, external_protocol=external_protocol, internal_port=internal_port, internal_protocol=internal_protocol, policy_names=policy_names, ssl_certificate_id=ssl_certificate_id)

        return jsii.invoke(self, "addListener", [listener])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: "ILoadBalancerTarget") -> None:
        """
        :param target: -
        """
        return jsii.invoke(self, "addTarget", [target])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Control all connections from and to this load balancer."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="listenerPorts")
    def listener_ports(self) -> typing.List["ListenerPort"]:
        """An object controlling specifically the connections for each listener added to this load balancer."""
        return jsii.get(self, "listenerPorts")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneName")
    def load_balancer_canonical_hosted_zone_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneName")

    @property
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneNameId")
    def load_balancer_canonical_hosted_zone_name_id(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "loadBalancerCanonicalHostedZoneNameId")

    @property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "loadBalancerDnsName")

    @property
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "loadBalancerName")

    @property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupGroupName")
    def load_balancer_source_security_group_group_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "loadBalancerSourceSecurityGroupGroupName")

    @property
    @jsii.member(jsii_name="loadBalancerSourceSecurityGroupOwnerAlias")
    def load_balancer_source_security_group_owner_alias(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "loadBalancerSourceSecurityGroupOwnerAlias")


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancerListener", jsii_struct_bases=[], name_mapping={'external_port': 'externalPort', 'allow_connections_from': 'allowConnectionsFrom', 'external_protocol': 'externalProtocol', 'internal_port': 'internalPort', 'internal_protocol': 'internalProtocol', 'policy_names': 'policyNames', 'ssl_certificate_id': 'sslCertificateId'})
class LoadBalancerListener():
    def __init__(self, *, external_port: jsii.Number, allow_connections_from: typing.Optional[typing.List[aws_cdk.aws_ec2.IConnectable]]=None, external_protocol: typing.Optional["LoadBalancingProtocol"]=None, internal_port: typing.Optional[jsii.Number]=None, internal_protocol: typing.Optional["LoadBalancingProtocol"]=None, policy_names: typing.Optional[typing.List[str]]=None, ssl_certificate_id: typing.Optional[str]=None):
        """Add a backend to the load balancer.

        :param external_port: External listening port.
        :param allow_connections_from: Allow connections to the load balancer from the given set of connection peers. By default, connections will be allowed from anywhere. Set this to an empty list to deny connections, or supply a custom list of peers to allow connections from (IP ranges or security groups). Default: Anywhere
        :param external_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the external port is either 80 or 443.
        :param internal_port: Instance listening port. Same as the externalPort if not specified. Default: externalPort
        :param internal_protocol: What public protocol to use for load balancing. Either 'tcp', 'ssl', 'http' or 'https'. May be omitted if the internal port is either 80 or 443. The instance protocol is 'tcp' if the front-end protocol is 'tcp' or 'ssl', the instance protocol is 'http' if the front-end protocol is 'https'.
        :param policy_names: SSL policy names.
        :param ssl_certificate_id: ID of SSL certificate.
        """
        self._values = {
            'external_port': external_port,
        }
        if allow_connections_from is not None: self._values["allow_connections_from"] = allow_connections_from
        if external_protocol is not None: self._values["external_protocol"] = external_protocol
        if internal_port is not None: self._values["internal_port"] = internal_port
        if internal_protocol is not None: self._values["internal_protocol"] = internal_protocol
        if policy_names is not None: self._values["policy_names"] = policy_names
        if ssl_certificate_id is not None: self._values["ssl_certificate_id"] = ssl_certificate_id

    @property
    def external_port(self) -> jsii.Number:
        """External listening port."""
        return self._values.get('external_port')

    @property
    def allow_connections_from(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.IConnectable]]:
        """Allow connections to the load balancer from the given set of connection peers.

        By default, connections will be allowed from anywhere. Set this to an empty list
        to deny connections, or supply a custom list of peers to allow connections from
        (IP ranges or security groups).

        default
        :default: Anywhere
        """
        return self._values.get('allow_connections_from')

    @property
    def external_protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        """What public protocol to use for load balancing.

        Either 'tcp', 'ssl', 'http' or 'https'.

        May be omitted if the external port is either 80 or 443.
        """
        return self._values.get('external_protocol')

    @property
    def internal_port(self) -> typing.Optional[jsii.Number]:
        """Instance listening port.

        Same as the externalPort if not specified.

        default
        :default: externalPort
        """
        return self._values.get('internal_port')

    @property
    def internal_protocol(self) -> typing.Optional["LoadBalancingProtocol"]:
        """What public protocol to use for load balancing.

        Either 'tcp', 'ssl', 'http' or 'https'.

        May be omitted if the internal port is either 80 or 443.

        The instance protocol is 'tcp' if the front-end protocol
        is 'tcp' or 'ssl', the instance protocol is 'http' if the
        front-end protocol is 'https'.
        """
        return self._values.get('internal_protocol')

    @property
    def policy_names(self) -> typing.Optional[typing.List[str]]:
        """SSL policy names."""
        return self._values.get('policy_names')

    @property
    def ssl_certificate_id(self) -> typing.Optional[str]:
        """ID of SSL certificate."""
        return self._values.get('ssl_certificate_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancerListener(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancerProps", jsii_struct_bases=[], name_mapping={'vpc': 'vpc', 'cross_zone': 'crossZone', 'health_check': 'healthCheck', 'internet_facing': 'internetFacing', 'listeners': 'listeners', 'subnet_selection': 'subnetSelection', 'targets': 'targets'})
class LoadBalancerProps():
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, cross_zone: typing.Optional[bool]=None, health_check: typing.Optional["HealthCheck"]=None, internet_facing: typing.Optional[bool]=None, listeners: typing.Optional[typing.List["LoadBalancerListener"]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, targets: typing.Optional[typing.List["ILoadBalancerTarget"]]=None):
        """Construction properties for a LoadBalancer.

        :param vpc: VPC network of the fleet instances.
        :param cross_zone: Whether cross zone load balancing is enabled. This controls whether the load balancer evenly distributes requests across each availability zone Default: true
        :param health_check: Health check settings for the load balancing targets. Not required but recommended. Default: - None.
        :param internet_facing: Whether this is an internet-facing Load Balancer. This controls whether the LB has a public IP address assigned. It does not open up the Load Balancer's security groups to public internet access. Default: false
        :param listeners: What listeners to set up for the load balancer. Can also be added by .addListener() Default: -
        :param subnet_selection: Which subnets to deploy the load balancer. Can be used to define a specific set of subnets to deploy the load balancer to. Useful multiple public or private subnets are covering the same availability zone. Default: - Public subnets if internetFacing, Private subnets otherwise
        :param targets: What targets to load balance to. Can also be added by .addTarget() Default: - None.
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        if isinstance(subnet_selection, dict): subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {
            'vpc': vpc,
        }
        if cross_zone is not None: self._values["cross_zone"] = cross_zone
        if health_check is not None: self._values["health_check"] = health_check
        if internet_facing is not None: self._values["internet_facing"] = internet_facing
        if listeners is not None: self._values["listeners"] = listeners
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if targets is not None: self._values["targets"] = targets

    @property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC network of the fleet instances."""
        return self._values.get('vpc')

    @property
    def cross_zone(self) -> typing.Optional[bool]:
        """Whether cross zone load balancing is enabled.

        This controls whether the load balancer evenly distributes requests
        across each availability zone

        default
        :default: true
        """
        return self._values.get('cross_zone')

    @property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Health check settings for the load balancing targets.

        Not required but recommended.

        default
        :default: - None.
        """
        return self._values.get('health_check')

    @property
    def internet_facing(self) -> typing.Optional[bool]:
        """Whether this is an internet-facing Load Balancer.

        This controls whether the LB has a public IP address assigned. It does
        not open up the Load Balancer's security groups to public internet access.

        default
        :default: false
        """
        return self._values.get('internet_facing')

    @property
    def listeners(self) -> typing.Optional[typing.List["LoadBalancerListener"]]:
        """What listeners to set up for the load balancer.

        Can also be added by .addListener()

        default
        :default: -
        """
        return self._values.get('listeners')

    @property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Which subnets to deploy the load balancer.

        Can be used to define a specific set of subnets to deploy the load balancer to.
        Useful multiple public or private subnets are covering the same availability zone.

        default
        :default: - Public subnets if internetFacing, Private subnets otherwise
        """
        return self._values.get('subnet_selection')

    @property
    def targets(self) -> typing.Optional[typing.List["ILoadBalancerTarget"]]:
        """What targets to load balance to.

        Can also be added by .addTarget()

        default
        :default: - None.
        """
        return self._values.get('targets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-elasticloadbalancing.LoadBalancingProtocol")
class LoadBalancingProtocol(enum.Enum):
    TCP = "TCP"
    SSL = "SSL"
    HTTP = "HTTP"
    HTTPS = "HTTPS"

__all__ = ["CfnLoadBalancer", "CfnLoadBalancerProps", "HealthCheck", "ILoadBalancerTarget", "ListenerPort", "LoadBalancer", "LoadBalancerListener", "LoadBalancerProps", "LoadBalancingProtocol", "__jsii_assembly__"]

publication.publish()
