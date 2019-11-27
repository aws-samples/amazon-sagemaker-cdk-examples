"""
# Route53 Alias Record Targets for the CDK Route53 Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains Route53 Alias Record targets for:

* API Gateway custom domains

  ```python
  # Example automatically generated. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ApiGateway(rest_api))
  )
  ```
* CloudFront distributions

  ```python
  # Example automatically generated. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.CloudFrontTarget(distribution))
  )
  ```
* ELBv2 load balancers

  ```python
  # Example automatically generated. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.LoadBalancerTarget(elbv2))
  )
  ```
* Classic load balancers

  ```python
  # Example automatically generated. See https://github.com/aws/jsii/issues/826
  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(alias.ClassicLoadBalancerTarget(elb))
  )
  ```
* S3 Bucket WebSite:

**Important:** The Bucket name must strictly match the full DNS name.
See [the Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html) for more info.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
[recordName, domainName] = ["www", "example.com"]

bucket_website = Bucket(self, "BucketWebsite",
    bucket_name=[record_name, domain_name].join("."), # www.example.com
    public_read_access=True,
    website_index_document="index.html"
)

zone = HostedZone.from_lookup(self, "Zone", domain_name=domain_name)# example.com

route53.ARecord(self, "AliasRecord",
    zone=zone,
    record_name=record_name, # www
    target=route53.RecordTarget.from_alias(alias.BucketWebsiteTarget(bucket))
)
```

See the documentation of `@aws-cdk/aws-route53` for more information.
"""
import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_apigateway
import aws_cdk.aws_cloudfront
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_route53
import aws_cdk.aws_s3
import aws_cdk.core
import aws_cdk.region_info
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-route53-targets", "1.18.0", __name__, "aws-route53-targets@1.18.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class ApiGatewayDomain(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.ApiGatewayDomain"):
    """Defines an API Gateway domain name as the alias target.

    Use the ``ApiGateway`` class if you wish to map the alias to an REST API with a
    domain name defined throug the ``RestApiProps.domainName`` prop.
    """
    def __init__(self, domain_name: aws_cdk.aws_apigateway.IDomainName) -> None:
        """
        :param domain_name: -
        """
        jsii.create(ApiGatewayDomain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


class ApiGateway(ApiGatewayDomain, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.ApiGateway"):
    """Defines an API Gateway REST API as the alias target. Requires that the domain name will be defined through ``RestApiProps.domainName``.

    You can direct the alias to any ``apigateway.DomainName`` resource through the
    ``ApiGatewayDomain`` class.
    """
    def __init__(self, api: aws_cdk.aws_apigateway.RestApi) -> None:
        """
        :param api: -
        """
        jsii.create(ApiGateway, self, [api])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class BucketWebsiteTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.BucketWebsiteTarget"):
    """Use a S3 as an alias record target."""
    def __init__(self, bucket: aws_cdk.aws_s3.IBucket) -> None:
        """
        :param bucket: -
        """
        jsii.create(BucketWebsiteTarget, self, [bucket])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class ClassicLoadBalancerTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.ClassicLoadBalancerTarget"):
    """Use a classic ELB as an alias record target."""
    def __init__(self, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> None:
        """
        :param load_balancer: -
        """
        jsii.create(ClassicLoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class CloudFrontTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.CloudFrontTarget"):
    """Use a CloudFront Distribution as an alias record target."""
    def __init__(self, distribution: aws_cdk.aws_cloudfront.CloudFrontWebDistribution) -> None:
        """
        :param distribution: -
        """
        jsii.create(CloudFrontTarget, self, [distribution])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class LoadBalancerTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.LoadBalancerTarget"):
    """Use an ELBv2 as an alias record target."""
    def __init__(self, load_balancer: aws_cdk.aws_elasticloadbalancingv2.ILoadBalancerV2) -> None:
        """
        :param load_balancer: -
        """
        jsii.create(LoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        """
        return jsii.invoke(self, "bind", [_record])


__all__ = ["ApiGateway", "ApiGatewayDomain", "BucketWebsiteTarget", "ClassicLoadBalancerTarget", "CloudFrontTarget", "LoadBalancerTarget", "__jsii_assembly__"]

publication.publish()
