"""
## Amazon ECR Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This package contains constructs for working with Amazon Elastic Container Registry.

### Repositories

Define a repository by creating a new instance of `Repository`. A repository
holds multiple verions of a single container image.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
repository = ecr.Repository(self, "Repository")
```

### Automatically clean up repositories

You can set life cycle rules to automatically clean up old images from your
repository. The first life cycle rule that matches an image will be applied
against that image. For example, the following deletes images older than
30 days, while keeping all images tagged with prod (note that the order
is important here):

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
repository.add_lifecycle_rule(tag_prefix_list=["prod"], max_image_count=9999)
repository.add_lifecycle_rule(max_image_age_days=cdk.Duration.days(30))
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

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecr", "1.18.0", __name__, "aws-ecr@1.18.0.jsii.tgz")
@jsii.implements(aws_cdk.core.IInspectable)
class CfnRepository(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecr.CfnRepository"):
    """A CloudFormation ``AWS::ECR::Repository``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECR::Repository
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, lifecycle_policy: typing.Optional[typing.Union[typing.Optional["LifecyclePolicyProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, repository_name: typing.Optional[str]=None, repository_policy_text: typing.Any=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ECR::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.
        """
        props = CfnRepositoryProps(lifecycle_policy=lifecycle_policy, repository_name=repository_name, repository_policy_text=repository_policy_text, tags=tags)

        jsii.create(CfnRepository, self, [scope, id, props])

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
        """``AWS::ECR::Repository.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="repositoryPolicyText")
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::Repository.RepositoryPolicyText``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        """
        return jsii.get(self, "repositoryPolicyText")

    @repository_policy_text.setter
    def repository_policy_text(self, value: typing.Any):
        return jsii.set(self, "repositoryPolicyText", value)

    @property
    @jsii.member(jsii_name="lifecyclePolicy")
    def lifecycle_policy(self) -> typing.Optional[typing.Union[typing.Optional["LifecyclePolicyProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ECR::Repository.LifecyclePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        """
        return jsii.get(self, "lifecyclePolicy")

    @lifecycle_policy.setter
    def lifecycle_policy(self, value: typing.Optional[typing.Union[typing.Optional["LifecyclePolicyProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "lifecyclePolicy", value)

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> typing.Optional[str]:
        """``AWS::ECR::Repository.RepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        """
        return jsii.get(self, "repositoryName")

    @repository_name.setter
    def repository_name(self, value: typing.Optional[str]):
        return jsii.set(self, "repositoryName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecr.CfnRepository.LifecyclePolicyProperty", jsii_struct_bases=[], name_mapping={'lifecycle_policy_text': 'lifecyclePolicyText', 'registry_id': 'registryId'})
    class LifecyclePolicyProperty():
        def __init__(self, *, lifecycle_policy_text: typing.Optional[str]=None, registry_id: typing.Optional[str]=None):
            """
            :param lifecycle_policy_text: ``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.
            :param registry_id: ``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html
            """
            self._values = {
            }
            if lifecycle_policy_text is not None: self._values["lifecycle_policy_text"] = lifecycle_policy_text
            if registry_id is not None: self._values["registry_id"] = registry_id

        @property
        def lifecycle_policy_text(self) -> typing.Optional[str]:
            """``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-lifecyclepolicytext
            """
            return self._values.get('lifecycle_policy_text')

        @property
        def registry_id(self) -> typing.Optional[str]:
            """``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-registryid
            """
            return self._values.get('registry_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LifecyclePolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.CfnRepositoryProps", jsii_struct_bases=[], name_mapping={'lifecycle_policy': 'lifecyclePolicy', 'repository_name': 'repositoryName', 'repository_policy_text': 'repositoryPolicyText', 'tags': 'tags'})
class CfnRepositoryProps():
    def __init__(self, *, lifecycle_policy: typing.Optional[typing.Union[typing.Optional["CfnRepository.LifecyclePolicyProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, repository_name: typing.Optional[str]=None, repository_policy_text: typing.Any=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::ECR::Repository``.

        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
        """
        self._values = {
        }
        if lifecycle_policy is not None: self._values["lifecycle_policy"] = lifecycle_policy
        if repository_name is not None: self._values["repository_name"] = repository_name
        if repository_policy_text is not None: self._values["repository_policy_text"] = repository_policy_text
        if tags is not None: self._values["tags"] = tags

    @property
    def lifecycle_policy(self) -> typing.Optional[typing.Union[typing.Optional["CfnRepository.LifecyclePolicyProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ECR::Repository.LifecyclePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        """
        return self._values.get('lifecycle_policy')

    @property
    def repository_name(self) -> typing.Optional[str]:
        """``AWS::ECR::Repository.RepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        """
        return self._values.get('repository_name')

    @property
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::Repository.RepositoryPolicyText``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        """
        return self._values.get('repository_policy_text')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ECR::Repository.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRepositoryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-ecr.IRepository")
class IRepository(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents an ECR repository."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of the repository.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The name of the repository.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> str:
        """The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        """
        ...

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull images in this repository.

        :param grantee: -
        """
        ...

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        """
        ...

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(self, id: str, *, image_tag: typing.Optional[str]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(self, id: str, *, image_tags: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(self, tag: typing.Optional[str]=None) -> str:
        """Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).
        """
        ...


class _IRepositoryProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents an ECR repository."""
    __jsii_type__ = "@aws-cdk/aws-ecr.IRepository"
    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of the repository.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The name of the repository.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "repositoryName")

    @property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> str:
        """The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "repositoryUri")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull images in this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(self, id: str, *, image_tag: typing.Optional[str]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailImagePushedOptions(image_tag=image_tag, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailImagePushed", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(self, id: str, *, image_tags: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnImageScanCompletedOptions(image_tags=image_tags, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onImageScanCompleted", [id, options])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(self, tag: typing.Optional[str]=None) -> str:
        """Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).
        """
        return jsii.invoke(self, "repositoryUriForTag", [tag])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.LifecycleRule", jsii_struct_bases=[], name_mapping={'description': 'description', 'max_image_age': 'maxImageAge', 'max_image_count': 'maxImageCount', 'rule_priority': 'rulePriority', 'tag_prefix_list': 'tagPrefixList', 'tag_status': 'tagStatus'})
class LifecycleRule():
    def __init__(self, *, description: typing.Optional[str]=None, max_image_age: typing.Optional[aws_cdk.core.Duration]=None, max_image_count: typing.Optional[jsii.Number]=None, rule_priority: typing.Optional[jsii.Number]=None, tag_prefix_list: typing.Optional[typing.List[str]]=None, tag_status: typing.Optional["TagStatus"]=None):
        """An ECR life cycle rule.

        :param description: Describes the purpose of the rule. Default: No description
        :param max_image_age: The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAgeDays.
        :param rule_priority: Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if max_image_age is not None: self._values["max_image_age"] = max_image_age
        if max_image_count is not None: self._values["max_image_count"] = max_image_count
        if rule_priority is not None: self._values["rule_priority"] = rule_priority
        if tag_prefix_list is not None: self._values["tag_prefix_list"] = tag_prefix_list
        if tag_status is not None: self._values["tag_status"] = tag_status

    @property
    def description(self) -> typing.Optional[str]:
        """Describes the purpose of the rule.

        default
        :default: No description
        """
        return self._values.get('description')

    @property
    def max_image_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum age of images to retain. The value must represent a number of days.

        Specify exactly one of maxImageCount and maxImageAge.
        """
        return self._values.get('max_image_age')

    @property
    def max_image_count(self) -> typing.Optional[jsii.Number]:
        """The maximum number of images to retain.

        Specify exactly one of maxImageCount and maxImageAgeDays.
        """
        return self._values.get('max_image_count')

    @property
    def rule_priority(self) -> typing.Optional[jsii.Number]:
        """Controls the order in which rules are evaluated (low to high).

        All rules must have a unique priority, where lower numbers have
        higher precedence. The first rule that matches is applied to an image.

        There can only be one rule with a tagStatus of Any, and it must have
        the highest rulePriority.

        All rules without a specified priority will have incrementing priorities
        automatically assigned to them, higher than any rules that DO have priorities.

        default
        :default: Automatically assigned
        """
        return self._values.get('rule_priority')

    @property
    def tag_prefix_list(self) -> typing.Optional[typing.List[str]]:
        """Select images that have ALL the given prefixes in their tag.

        Only if tagStatus == TagStatus.Tagged
        """
        return self._values.get('tag_prefix_list')

    @property
    def tag_status(self) -> typing.Optional["TagStatus"]:
        """Select images based on tags.

        Only one rule is allowed to select untagged images, and it must
        have the highest rulePriority.

        default
        :default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        """
        return self._values.get('tag_status')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LifecycleRule(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.OnCloudTrailImagePushedOptions", jsii_struct_bases=[aws_cdk.aws_events.OnEventOptions], name_mapping={'description': 'description', 'event_pattern': 'eventPattern', 'rule_name': 'ruleName', 'target': 'target', 'image_tag': 'imageTag'})
class OnCloudTrailImagePushedOptions(aws_cdk.aws_events.OnEventOptions):
    def __init__(self, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, image_tag: typing.Optional[str]=None):
        """Options for the onCloudTrailImagePushed method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        """
        if isinstance(event_pattern, dict): event_pattern = aws_cdk.aws_events.EventPattern(**event_pattern)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if event_pattern is not None: self._values["event_pattern"] = event_pattern
        if rule_name is not None: self._values["rule_name"] = rule_name
        if target is not None: self._values["target"] = target
        if image_tag is not None: self._values["image_tag"] = image_tag

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the rule's purpose.

        default
        :default: - No description
        """
        return self._values.get('description')

    @property
    def event_pattern(self) -> typing.Optional[aws_cdk.aws_events.EventPattern]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        default
        :default: - No additional filtering based on an event pattern.

        see
        :see: http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CloudWatchEventsandEventPatterns.html
        """
        return self._values.get('event_pattern')

    @property
    def rule_name(self) -> typing.Optional[str]:
        """A name for the rule.

        default
        :default: AWS CloudFormation generates a unique physical ID.
        """
        return self._values.get('rule_name')

    @property
    def target(self) -> typing.Optional[aws_cdk.aws_events.IRuleTarget]:
        """The target to register for the event.

        default
        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        return self._values.get('target')

    @property
    def image_tag(self) -> typing.Optional[str]:
        """Only watch changes to this image tag.

        default
        :default: - Watch changes to all tags
        """
        return self._values.get('image_tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OnCloudTrailImagePushedOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.OnImageScanCompletedOptions", jsii_struct_bases=[aws_cdk.aws_events.OnEventOptions], name_mapping={'description': 'description', 'event_pattern': 'eventPattern', 'rule_name': 'ruleName', 'target': 'target', 'image_tags': 'imageTags'})
class OnImageScanCompletedOptions(aws_cdk.aws_events.OnEventOptions):
    def __init__(self, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, image_tags: typing.Optional[typing.List[str]]=None):
        """Options for the OnImageScanCompleted method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        """
        if isinstance(event_pattern, dict): event_pattern = aws_cdk.aws_events.EventPattern(**event_pattern)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if event_pattern is not None: self._values["event_pattern"] = event_pattern
        if rule_name is not None: self._values["rule_name"] = rule_name
        if target is not None: self._values["target"] = target
        if image_tags is not None: self._values["image_tags"] = image_tags

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the rule's purpose.

        default
        :default: - No description
        """
        return self._values.get('description')

    @property
    def event_pattern(self) -> typing.Optional[aws_cdk.aws_events.EventPattern]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        default
        :default: - No additional filtering based on an event pattern.

        see
        :see: http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CloudWatchEventsandEventPatterns.html
        """
        return self._values.get('event_pattern')

    @property
    def rule_name(self) -> typing.Optional[str]:
        """A name for the rule.

        default
        :default: AWS CloudFormation generates a unique physical ID.
        """
        return self._values.get('rule_name')

    @property
    def target(self) -> typing.Optional[aws_cdk.aws_events.IRuleTarget]:
        """The target to register for the event.

        default
        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        return self._values.get('target')

    @property
    def image_tags(self) -> typing.Optional[typing.List[str]]:
        """Only watch changes to the image tags spedified. Leave it undefined to watch the full repository.

        default
        :default: - Watch the changes to the repository with all image tags
        """
        return self._values.get('image_tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OnImageScanCompletedOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.RepositoryAttributes", jsii_struct_bases=[], name_mapping={'repository_arn': 'repositoryArn', 'repository_name': 'repositoryName'})
class RepositoryAttributes():
    def __init__(self, *, repository_arn: str, repository_name: str):
        """
        :param repository_arn: 
        :param repository_name: 
        """
        self._values = {
            'repository_arn': repository_arn,
            'repository_name': repository_name,
        }

    @property
    def repository_arn(self) -> str:
        return self._values.get('repository_arn')

    @property
    def repository_name(self) -> str:
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RepositoryAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IRepository)
class RepositoryBase(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecr.RepositoryBase"):
    """Base class for ECR repository.

    Reused between imported repositories and owned repositories.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _RepositoryBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = aws_cdk.core.ResourceProps(physical_name=physical_name)

        jsii.create(RepositoryBase, self, [scope, id, props])

    @jsii.member(jsii_name="addToResourcePolicy")
    @abc.abstractmethod
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: aws_cdk.aws_iam.IGrantable, *actions: str) -> aws_cdk.aws_iam.Grant:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to use the images in this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(self, id: str, *, image_tag: typing.Optional[str]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnCloudTrailImagePushedOptions(image_tag=image_tag, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCloudTrailImagePushed", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(self, id: str, *, image_tags: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an AWS CloudWatch event rule that can trigger a target when an image scan is completed.

        :param id: The id of the rule.
        :param options: Options for adding the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = OnImageScanCompletedOptions(image_tags=image_tags, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onImageScanCompleted", [id, options])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(self, tag: typing.Optional[str]=None) -> str:
        """Returns the URL of the repository. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Optional image tag.
        """
        return jsii.invoke(self, "repositoryUriForTag", [tag])

    @property
    @jsii.member(jsii_name="repositoryArn")
    @abc.abstractmethod
    def repository_arn(self) -> str:
        """The ARN of the repository."""
        ...

    @property
    @jsii.member(jsii_name="repositoryName")
    @abc.abstractmethod
    def repository_name(self) -> str:
        """The name of the repository."""
        ...

    @property
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> str:
        """The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY
        """
        return jsii.get(self, "repositoryUri")


class _RepositoryBaseProxy(RepositoryBase, jsii.proxy_for(aws_cdk.core.Resource)):
    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of the repository."""
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The name of the repository."""
        return jsii.get(self, "repositoryName")


class Repository(RepositoryBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecr.Repository"):
    """Define an ECR repository."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, lifecycle_registry_id: typing.Optional[str]=None, lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, repository_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param lifecycle_registry_id: The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: Name for this repository. Default: Automatically generated name.
        """
        props = RepositoryProps(lifecycle_registry_id=lifecycle_registry_id, lifecycle_rules=lifecycle_rules, removal_policy=removal_policy, repository_name=repository_name)

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLocalRepository")
    @classmethod
    def arn_for_local_repository(cls, repository_name: str, scope: aws_cdk.core.IConstruct) -> str:
        """Returns an ECR ARN for a repository that resides in the same account/region as the current stack.

        :param repository_name: -
        :param scope: -
        """
        return jsii.sinvoke(cls, "arnForLocalRepository", [repository_name, scope])

    @jsii.member(jsii_name="fromRepositoryArn")
    @classmethod
    def from_repository_arn(cls, scope: aws_cdk.core.Construct, id: str, repository_arn: str) -> "IRepository":
        """
        :param scope: -
        :param id: -
        :param repository_arn: -
        """
        return jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn])

    @jsii.member(jsii_name="fromRepositoryAttributes")
    @classmethod
    def from_repository_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, repository_arn: str, repository_name: str) -> "IRepository":
        """Import a repository.

        :param scope: -
        :param id: -
        :param attrs: -
        :param repository_arn: 
        :param repository_name: 
        """
        attrs = RepositoryAttributes(repository_arn=repository_arn, repository_name=repository_name)

        return jsii.sinvoke(cls, "fromRepositoryAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromRepositoryName")
    @classmethod
    def from_repository_name(cls, scope: aws_cdk.core.Construct, id: str, repository_name: str) -> "IRepository":
        """
        :param scope: -
        :param id: -
        :param repository_name: -
        """
        return jsii.sinvoke(cls, "fromRepositoryName", [scope, id, repository_name])

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(self, *, description: typing.Optional[str]=None, max_image_age: typing.Optional[aws_cdk.core.Duration]=None, max_image_count: typing.Optional[jsii.Number]=None, rule_priority: typing.Optional[jsii.Number]=None, tag_prefix_list: typing.Optional[typing.List[str]]=None, tag_status: typing.Optional["TagStatus"]=None) -> None:
        """Add a life cycle rule to the repository.

        Life cycle rules automatically expire images from the repository that match
        certain conditions.

        :param rule: -
        :param description: Describes the purpose of the rule. Default: No description
        :param max_image_age: The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAgeDays.
        :param rule_priority: Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        """
        rule = LifecycleRule(description=description, max_image_age=max_image_age, max_image_count=max_image_count, rule_priority=rule_priority, tag_prefix_list=tag_prefix_list, tag_status=tag_status)

        return jsii.invoke(self, "addLifecycleRule", [rule])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a policy statement to the repository's resource policy.

        :param statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of the repository."""
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The name of the repository."""
        return jsii.get(self, "repositoryName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr.RepositoryProps", jsii_struct_bases=[], name_mapping={'lifecycle_registry_id': 'lifecycleRegistryId', 'lifecycle_rules': 'lifecycleRules', 'removal_policy': 'removalPolicy', 'repository_name': 'repositoryName'})
class RepositoryProps():
    def __init__(self, *, lifecycle_registry_id: typing.Optional[str]=None, lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, repository_name: typing.Optional[str]=None):
        """
        :param lifecycle_registry_id: The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: Name for this repository. Default: Automatically generated name.
        """
        self._values = {
        }
        if lifecycle_registry_id is not None: self._values["lifecycle_registry_id"] = lifecycle_registry_id
        if lifecycle_rules is not None: self._values["lifecycle_rules"] = lifecycle_rules
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if repository_name is not None: self._values["repository_name"] = repository_name

    @property
    def lifecycle_registry_id(self) -> typing.Optional[str]:
        """The AWS account ID associated with the registry that contains the repository.

        default
        :default: The default registry is assumed.

        see
        :see: https://docs.aws.amazon.com/AmazonECR/latest/APIReference/API_PutLifecyclePolicy.html
        """
        return self._values.get('lifecycle_registry_id')

    @property
    def lifecycle_rules(self) -> typing.Optional[typing.List["LifecycleRule"]]:
        """Life cycle rules to apply to this registry.

        default
        :default: No life cycle rules
        """
        return self._values.get('lifecycle_rules')

    @property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """Determine what happens to the repository when the resource/stack is deleted.

        default
        :default: RemovalPolicy.Retain
        """
        return self._values.get('removal_policy')

    @property
    def repository_name(self) -> typing.Optional[str]:
        """Name for this repository.

        default
        :default: Automatically generated name.
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RepositoryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecr.TagStatus")
class TagStatus(enum.Enum):
    """Select images based on tags."""
    ANY = "ANY"
    """Rule applies to all images."""
    TAGGED = "TAGGED"
    """Rule applies to tagged images."""
    UNTAGGED = "UNTAGGED"
    """Rule applies to untagged images."""

__all__ = ["CfnRepository", "CfnRepositoryProps", "IRepository", "LifecycleRule", "OnCloudTrailImagePushedOptions", "OnImageScanCompletedOptions", "Repository", "RepositoryAttributes", "RepositoryBase", "RepositoryProps", "TagStatus", "__jsii_assembly__"]

publication.publish()
