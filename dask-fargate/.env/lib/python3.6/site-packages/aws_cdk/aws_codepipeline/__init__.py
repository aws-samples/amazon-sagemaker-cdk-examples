"""
## AWS CodePipeline Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

### Pipeline

To construct an empty Pipeline:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codepipeline as codepipeline

pipeline = codepipeline.Pipeline(self, "MyFirstPipeline")
```

To give the Pipeline a nice, human-readable name:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
    pipeline_name="MyPipeline"
)
```

### Stages

You can provide Stages when creating the Pipeline:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
    stages=[{
        "stage_name": "Source",
        "actions": []
    }
    ]
)
```

Or append a Stage to an existing Pipeline:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
source_stage = pipeline.add_stage(
    stage_name="Source",
    actions=[]
)
```

You can insert the new Stage at an arbitrary point in the Pipeline:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
some_stage = pipeline.add_stage(
    stage_name="SomeStage",
    placement={
        # note: you can only specify one of the below properties
        "right_before": another_stage,
        "just_after": another_stage
    }
)
```

### Actions

Actions live in a separate package, `@aws-cdk/aws-codepipeline-actions`.

To add an Action to a Stage, you can provide it when creating the Stage,
in the `actions` property,
or you can use the `IStage.addAction()` method to mutate an existing Stage:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
source_stage.add_action(some_action)
```

### Cross-region CodePipelines

You can also use the cross-region feature to deploy resources
(currently, only CloudFormation Stacks are supported)
into a different region than your Pipeline is in.

It works like this:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
pipeline = codepipeline.Pipeline(self, "MyFirstPipeline",
    # ...
    cross_region_replication_buckets={
        # note that a physical name of the replication Bucket must be known at synthesis time
        "us-west-1": s3.Bucket.from_bucket_attributes(self, "UsWest1ReplicationBucket",
            bucket_name="my-us-west-1-replication-bucket",
            # optional KMS key
            encryption_key=kms.Key.from_key_arn(self, "UsWest1ReplicationKey", "arn:aws:kms:us-west-1:123456789012:key/1234-5678-9012")
        )
    }
)

# later in the code...
codepipeline_actions.CloudFormationCreateUpdateStackAction(
    action_name="CFN_US_West_1",
    # ...
    region="us-west-1"
)
```

This way, the `CFN_US_West_1` Action will operate in the `us-west-1` region,
regardless of which region your Pipeline is in.

If you don't provide a bucket for a region (other than the Pipeline's region)
that you're using for an Action,
there will be a new Stack, called `<nameOfYourPipelineStack>-support-<region>`,
defined for you, containing a replication Bucket.
This new Stack will depend on your Pipeline Stack,
so deploying the Pipeline Stack will deploy the support Stack(s) first.
Example:

```bash
$ cdk ls
MyMainStack
MyMainStack-support-us-west-1
$ cdk deploy MyMainStack
# output of cdk deploy here...
```

See [the AWS docs here](https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-create-cross-region.html)
for more information on cross-region CodePipelines.

#### Creating an encrypted replication bucket

If you're passing a replication bucket created in a different stack,
like this:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
replication_stack = Stack(app, "ReplicationStack",
    env={
        "region": "us-west-1"
    }
)
key = kms.Key(replication_stack, "ReplicationKey")
replication_bucket = s3.Bucket(replication_stack, "ReplicationBucket",
    # like was said above - replication buckets need a set physical name
    bucket_name=PhysicalName.GENERATE_IF_NEEDED,
    encryption_key=key
)

# later...
codepipeline.Pipeline(pipeline_stack, "Pipeline",
    cross_region_replication_buckets={
        "us-west-1": replication_bucket
    }
)
```

When trying to encrypt it
(and note that if any of the cross-region actions happen to be cross-account as well,
the bucket *has to* be encrypted - otherwise the pipeline will fail at runtime),
you cannot use a key directly - KMS keys don't have physical names,
and so you can't reference them across environments.

In this case, you need to use an alias in place of the key when creating the bucket:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
key = kms.Key(replication_stack, "ReplicationKey")
alias = kms.Alias(replication_stack, "ReplicationAlias",
    # aliasName is required
    alias_name=PhysicalName.GENERATE_IF_NEEDED,
    target_key=key
)
replication_bucket = s3.Bucket(replication_stack, "ReplicationBucket",
    bucket_name=PhysicalName.GENERATE_IF_NEEDED,
    encryption_key=alias
)
```

### Events

#### Using a pipeline as an event target

A pipeline can be used as a target for a CloudWatch event rule:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_events as events

# kick off the pipeline every day
rule = events.Rule(self, "Daily",
    schedule=events.Schedule.rate(Duration.days(1))
)

rule.add_target(targets.CodePipeline(pipeline))
```

When a pipeline is used as an event target, the
"codepipeline:StartPipelineExecution" permission is granted to the AWS
CloudWatch Events service.

#### Event sources

Pipelines emit CloudWatch events. To define event rules for events emitted by
the pipeline, stages or action, use the `onXxx` methods on the respective
construct:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
my_pipeline.on_state_change("MyPipelineStateChange", target)
my_stage.on_state_change("MyStageStateChange", target)
my_action.on_state_change("MyActionStateChange", target)
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
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codepipeline", "1.18.0", __name__, "aws-codepipeline@1.18.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ActionArtifactBounds", jsii_struct_bases=[], name_mapping={'max_inputs': 'maxInputs', 'max_outputs': 'maxOutputs', 'min_inputs': 'minInputs', 'min_outputs': 'minOutputs'})
class ActionArtifactBounds():
    def __init__(self, *, max_inputs: jsii.Number, max_outputs: jsii.Number, min_inputs: jsii.Number, min_outputs: jsii.Number):
        """Specifies the constraints on the number of input and output artifacts an action can have.

        The constraints for each action type are documented on the
        {@link https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html Pipeline Structure Reference} page.

        :param max_inputs: 
        :param max_outputs: 
        :param min_inputs: 
        :param min_outputs: 
        """
        self._values = {
            'max_inputs': max_inputs,
            'max_outputs': max_outputs,
            'min_inputs': min_inputs,
            'min_outputs': min_outputs,
        }

    @property
    def max_inputs(self) -> jsii.Number:
        return self._values.get('max_inputs')

    @property
    def max_outputs(self) -> jsii.Number:
        return self._values.get('max_outputs')

    @property
    def min_inputs(self) -> jsii.Number:
        return self._values.get('min_inputs')

    @property
    def min_outputs(self) -> jsii.Number:
        return self._values.get('min_outputs')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ActionArtifactBounds(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ActionBindOptions", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'role': 'role'})
class ActionBindOptions():
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole):
        """
        :param bucket: 
        :param role: 
        """
        self._values = {
            'bucket': bucket,
            'role': role,
        }

    @property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        return self._values.get('bucket')

    @property
    def role(self) -> aws_cdk.aws_iam.IRole:
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ActionBindOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline.ActionCategory")
class ActionCategory(enum.Enum):
    SOURCE = "SOURCE"
    BUILD = "BUILD"
    TEST = "TEST"
    APPROVAL = "APPROVAL"
    DEPLOY = "DEPLOY"
    INVOKE = "INVOKE"

@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ActionConfig", jsii_struct_bases=[], name_mapping={'configuration': 'configuration'})
class ActionConfig():
    def __init__(self, *, configuration: typing.Any=None):
        """
        :param configuration: 
        """
        self._values = {
        }
        if configuration is not None: self._values["configuration"] = configuration

    @property
    def configuration(self) -> typing.Any:
        return self._values.get('configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ActionConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.ActionProperties", jsii_struct_bases=[], name_mapping={'action_name': 'actionName', 'artifact_bounds': 'artifactBounds', 'category': 'category', 'provider': 'provider', 'account': 'account', 'inputs': 'inputs', 'outputs': 'outputs', 'owner': 'owner', 'region': 'region', 'resource': 'resource', 'role': 'role', 'run_order': 'runOrder', 'version': 'version'})
class ActionProperties():
    def __init__(self, *, action_name: str, artifact_bounds: "ActionArtifactBounds", category: "ActionCategory", provider: str, account: typing.Optional[str]=None, inputs: typing.Optional[typing.List["Artifact"]]=None, outputs: typing.Optional[typing.List["Artifact"]]=None, owner: typing.Optional[str]=None, region: typing.Optional[str]=None, resource: typing.Optional[aws_cdk.core.IResource]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, run_order: typing.Optional[jsii.Number]=None, version: typing.Optional[str]=None):
        """
        :param action_name: 
        :param artifact_bounds: 
        :param category: The category of the action. The category defines which action type the owner (the entity that performs the action) performs.
        :param provider: The service provider that the action calls.
        :param account: The account the Action is supposed to live in. For Actions backed by resources, this is inferred from the Stack {@link resource} is part of. However, some Actions, like the CloudFormation ones, are not backed by any resource, and they still might want to be cross-account. In general, a concrete Action class should specify either {@link resource}, or {@link account} - but not both.
        :param inputs: 
        :param outputs: 
        :param owner: 
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param resource: The optional resource that is backing this Action. This is used for automatically handling Actions backed by resources from a different account and/or region.
        :param role: 
        :param run_order: The order in which AWS CodePipeline runs this action. For more information, see the AWS CodePipeline User Guide. https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements
        :param version: 
        """
        if isinstance(artifact_bounds, dict): artifact_bounds = ActionArtifactBounds(**artifact_bounds)
        self._values = {
            'action_name': action_name,
            'artifact_bounds': artifact_bounds,
            'category': category,
            'provider': provider,
        }
        if account is not None: self._values["account"] = account
        if inputs is not None: self._values["inputs"] = inputs
        if outputs is not None: self._values["outputs"] = outputs
        if owner is not None: self._values["owner"] = owner
        if region is not None: self._values["region"] = region
        if resource is not None: self._values["resource"] = resource
        if role is not None: self._values["role"] = role
        if run_order is not None: self._values["run_order"] = run_order
        if version is not None: self._values["version"] = version

    @property
    def action_name(self) -> str:
        return self._values.get('action_name')

    @property
    def artifact_bounds(self) -> "ActionArtifactBounds":
        return self._values.get('artifact_bounds')

    @property
    def category(self) -> "ActionCategory":
        """The category of the action. The category defines which action type the owner (the entity that performs the action) performs."""
        return self._values.get('category')

    @property
    def provider(self) -> str:
        """The service provider that the action calls."""
        return self._values.get('provider')

    @property
    def account(self) -> typing.Optional[str]:
        """The account the Action is supposed to live in. For Actions backed by resources, this is inferred from the Stack {@link resource} is part of. However, some Actions, like the CloudFormation ones, are not backed by any resource, and they still might want to be cross-account. In general, a concrete Action class should specify either {@link resource}, or {@link account} - but not both."""
        return self._values.get('account')

    @property
    def inputs(self) -> typing.Optional[typing.List["Artifact"]]:
        return self._values.get('inputs')

    @property
    def outputs(self) -> typing.Optional[typing.List["Artifact"]]:
        return self._values.get('outputs')

    @property
    def owner(self) -> typing.Optional[str]:
        return self._values.get('owner')

    @property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline
        """
        return self._values.get('region')

    @property
    def resource(self) -> typing.Optional[aws_cdk.core.IResource]:
        """The optional resource that is backing this Action. This is used for automatically handling Actions backed by resources from a different account and/or region."""
        return self._values.get('resource')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return self._values.get('role')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The order in which AWS CodePipeline runs this action. For more information, see the AWS CodePipeline User Guide.

        https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements
        """
        return self._values.get('run_order')

    @property
    def version(self) -> typing.Optional[str]:
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ActionProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Artifact(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.Artifact"):
    """An output artifact of an action.

    Artifacts can be used as input by some actions.
    """
    def __init__(self, artifact_name: typing.Optional[str]=None) -> None:
        """
        :param artifact_name: -
        """
        jsii.create(Artifact, self, [artifact_name])

    @jsii.member(jsii_name="artifact")
    @classmethod
    def artifact(cls, name: str) -> "Artifact":
        """A static factory method used to create instances of the Artifact class. Mainly meant to be used from ``decdk``.

        :param name: the (required) name of the Artifact.
        """
        return jsii.sinvoke(cls, "artifact", [name])

    @jsii.member(jsii_name="atPath")
    def at_path(self, file_name: str) -> "ArtifactPath":
        """Returns an ArtifactPath for a file within this artifact. CfnOutput is in the form "::".

        :param file_name: The name of the file.
        """
        return jsii.invoke(self, "atPath", [file_name])

    @jsii.member(jsii_name="getParam")
    def get_param(self, json_file: str, key_name: str) -> str:
        """Returns a token for a value inside a JSON file within this artifact.

        :param json_file: The JSON file name.
        :param key_name: The hash key.
        """
        return jsii.invoke(self, "getParam", [json_file, key_name])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> typing.Optional[str]:
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> str:
        """The artifact attribute for the name of the S3 bucket where the artifact is stored."""
        return jsii.get(self, "bucketName")

    @property
    @jsii.member(jsii_name="objectKey")
    def object_key(self) -> str:
        """The artifact attribute for The name of the .zip file that contains the artifact that is generated by AWS CodePipeline, such as 1ABCyZZ.zip."""
        return jsii.get(self, "objectKey")

    @property
    @jsii.member(jsii_name="s3Location")
    def s3_location(self) -> aws_cdk.aws_s3.Location:
        """Returns the location of the .zip file in S3 that this Artifact represents. Used by Lambda's ``CfnParametersCode`` when being deployed in a CodePipeline."""
        return jsii.get(self, "s3Location")

    @property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        """The artifact attribute of the Amazon Simple Storage Service (Amazon S3) URL of the artifact, such as https://s3-us-west-2.amazonaws.com/artifactstorebucket-yivczw8jma0c/test/TemplateSo/1ABCyZZ.zip."""
        return jsii.get(self, "url")

    @property
    @jsii.member(jsii_name="artifactName")
    def artifact_name(self) -> typing.Optional[str]:
        return jsii.get(self, "artifactName")


class ArtifactPath(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.ArtifactPath"):
    """A specific file within an output artifact.

    The most common use case for this is specifying the template file
    for a CloudFormation action.
    """
    def __init__(self, artifact: "Artifact", file_name: str) -> None:
        """
        :param artifact: -
        :param file_name: -
        """
        jsii.create(ArtifactPath, self, [artifact, file_name])

    @jsii.member(jsii_name="artifactPath")
    @classmethod
    def artifact_path(cls, artifact_name: str, file_name: str) -> "ArtifactPath":
        """
        :param artifact_name: -
        :param file_name: -
        """
        return jsii.sinvoke(cls, "artifactPath", [artifact_name, file_name])

    @property
    @jsii.member(jsii_name="artifact")
    def artifact(self) -> "Artifact":
        return jsii.get(self, "artifact")

    @property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> str:
        return jsii.get(self, "fileName")

    @property
    @jsii.member(jsii_name="location")
    def location(self) -> str:
        return jsii.get(self, "location")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCustomActionType(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType"):
    """A CloudFormation ``AWS::CodePipeline::CustomActionType``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodePipeline::CustomActionType
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, category: str, input_artifact_details: typing.Union["ArtifactDetailsProperty", aws_cdk.core.IResolvable], output_artifact_details: typing.Union["ArtifactDetailsProperty", aws_cdk.core.IResolvable], provider: str, version: str, configuration_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ConfigurationPropertiesProperty"]]]]]=None, settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SettingsProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::CodePipeline::CustomActionType``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param category: ``AWS::CodePipeline::CustomActionType.Category``.
        :param input_artifact_details: ``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.
        :param output_artifact_details: ``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.
        :param provider: ``AWS::CodePipeline::CustomActionType.Provider``.
        :param version: ``AWS::CodePipeline::CustomActionType.Version``.
        :param configuration_properties: ``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.
        :param settings: ``AWS::CodePipeline::CustomActionType.Settings``.
        :param tags: ``AWS::CodePipeline::CustomActionType.Tags``.
        """
        props = CfnCustomActionTypeProps(category=category, input_artifact_details=input_artifact_details, output_artifact_details=output_artifact_details, provider=provider, version=version, configuration_properties=configuration_properties, settings=settings, tags=tags)

        jsii.create(CfnCustomActionType, self, [scope, id, props])

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
        """``AWS::CodePipeline::CustomActionType.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="category")
    def category(self) -> str:
        """``AWS::CodePipeline::CustomActionType.Category``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-category
        """
        return jsii.get(self, "category")

    @category.setter
    def category(self, value: str):
        return jsii.set(self, "category", value)

    @property
    @jsii.member(jsii_name="inputArtifactDetails")
    def input_artifact_details(self) -> typing.Union["ArtifactDetailsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-inputartifactdetails
        """
        return jsii.get(self, "inputArtifactDetails")

    @input_artifact_details.setter
    def input_artifact_details(self, value: typing.Union["ArtifactDetailsProperty", aws_cdk.core.IResolvable]):
        return jsii.set(self, "inputArtifactDetails", value)

    @property
    @jsii.member(jsii_name="outputArtifactDetails")
    def output_artifact_details(self) -> typing.Union["ArtifactDetailsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-outputartifactdetails
        """
        return jsii.get(self, "outputArtifactDetails")

    @output_artifact_details.setter
    def output_artifact_details(self, value: typing.Union["ArtifactDetailsProperty", aws_cdk.core.IResolvable]):
        return jsii.set(self, "outputArtifactDetails", value)

    @property
    @jsii.member(jsii_name="provider")
    def provider(self) -> str:
        """``AWS::CodePipeline::CustomActionType.Provider``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-provider
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: str):
        return jsii.set(self, "provider", value)

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """``AWS::CodePipeline::CustomActionType.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: str):
        return jsii.set(self, "version", value)

    @property
    @jsii.member(jsii_name="configurationProperties")
    def configuration_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ConfigurationPropertiesProperty"]]]]]:
        """``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-configurationproperties
        """
        return jsii.get(self, "configurationProperties")

    @configuration_properties.setter
    def configuration_properties(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ConfigurationPropertiesProperty"]]]]]):
        return jsii.set(self, "configurationProperties", value)

    @property
    @jsii.member(jsii_name="settings")
    def settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SettingsProperty"]]]:
        """``AWS::CodePipeline::CustomActionType.Settings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-settings
        """
        return jsii.get(self, "settings")

    @settings.setter
    def settings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SettingsProperty"]]]):
        return jsii.set(self, "settings", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.ArtifactDetailsProperty", jsii_struct_bases=[], name_mapping={'maximum_count': 'maximumCount', 'minimum_count': 'minimumCount'})
    class ArtifactDetailsProperty():
        def __init__(self, *, maximum_count: jsii.Number, minimum_count: jsii.Number):
            """
            :param maximum_count: ``CfnCustomActionType.ArtifactDetailsProperty.MaximumCount``.
            :param minimum_count: ``CfnCustomActionType.ArtifactDetailsProperty.MinimumCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html
            """
            self._values = {
                'maximum_count': maximum_count,
                'minimum_count': minimum_count,
            }

        @property
        def maximum_count(self) -> jsii.Number:
            """``CfnCustomActionType.ArtifactDetailsProperty.MaximumCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html#cfn-codepipeline-customactiontype-artifactdetails-maximumcount
            """
            return self._values.get('maximum_count')

        @property
        def minimum_count(self) -> jsii.Number:
            """``CfnCustomActionType.ArtifactDetailsProperty.MinimumCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-artifactdetails.html#cfn-codepipeline-customactiontype-artifactdetails-minimumcount
            """
            return self._values.get('minimum_count')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ArtifactDetailsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.ConfigurationPropertiesProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'name': 'name', 'required': 'required', 'secret': 'secret', 'description': 'description', 'queryable': 'queryable', 'type': 'type'})
    class ConfigurationPropertiesProperty():
        def __init__(self, *, key: typing.Union[bool, aws_cdk.core.IResolvable], name: str, required: typing.Union[bool, aws_cdk.core.IResolvable], secret: typing.Union[bool, aws_cdk.core.IResolvable], description: typing.Optional[str]=None, queryable: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, type: typing.Optional[str]=None):
            """
            :param key: ``CfnCustomActionType.ConfigurationPropertiesProperty.Key``.
            :param name: ``CfnCustomActionType.ConfigurationPropertiesProperty.Name``.
            :param required: ``CfnCustomActionType.ConfigurationPropertiesProperty.Required``.
            :param secret: ``CfnCustomActionType.ConfigurationPropertiesProperty.Secret``.
            :param description: ``CfnCustomActionType.ConfigurationPropertiesProperty.Description``.
            :param queryable: ``CfnCustomActionType.ConfigurationPropertiesProperty.Queryable``.
            :param type: ``CfnCustomActionType.ConfigurationPropertiesProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html
            """
            self._values = {
                'key': key,
                'name': name,
                'required': required,
                'secret': secret,
            }
            if description is not None: self._values["description"] = description
            if queryable is not None: self._values["queryable"] = queryable
            if type is not None: self._values["type"] = type

        @property
        def key(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-key
            """
            return self._values.get('key')

        @property
        def name(self) -> str:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-name
            """
            return self._values.get('name')

        @property
        def required(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-required
            """
            return self._values.get('required')

        @property
        def secret(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Secret``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-secret
            """
            return self._values.get('secret')

        @property
        def description(self) -> typing.Optional[str]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-description
            """
            return self._values.get('description')

        @property
        def queryable(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Queryable``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-queryable
            """
            return self._values.get('queryable')

        @property
        def type(self) -> typing.Optional[str]:
            """``CfnCustomActionType.ConfigurationPropertiesProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-configurationproperties.html#cfn-codepipeline-customactiontype-configurationproperties-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConfigurationPropertiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionType.SettingsProperty", jsii_struct_bases=[], name_mapping={'entity_url_template': 'entityUrlTemplate', 'execution_url_template': 'executionUrlTemplate', 'revision_url_template': 'revisionUrlTemplate', 'third_party_configuration_url': 'thirdPartyConfigurationUrl'})
    class SettingsProperty():
        def __init__(self, *, entity_url_template: typing.Optional[str]=None, execution_url_template: typing.Optional[str]=None, revision_url_template: typing.Optional[str]=None, third_party_configuration_url: typing.Optional[str]=None):
            """
            :param entity_url_template: ``CfnCustomActionType.SettingsProperty.EntityUrlTemplate``.
            :param execution_url_template: ``CfnCustomActionType.SettingsProperty.ExecutionUrlTemplate``.
            :param revision_url_template: ``CfnCustomActionType.SettingsProperty.RevisionUrlTemplate``.
            :param third_party_configuration_url: ``CfnCustomActionType.SettingsProperty.ThirdPartyConfigurationUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html
            """
            self._values = {
            }
            if entity_url_template is not None: self._values["entity_url_template"] = entity_url_template
            if execution_url_template is not None: self._values["execution_url_template"] = execution_url_template
            if revision_url_template is not None: self._values["revision_url_template"] = revision_url_template
            if third_party_configuration_url is not None: self._values["third_party_configuration_url"] = third_party_configuration_url

        @property
        def entity_url_template(self) -> typing.Optional[str]:
            """``CfnCustomActionType.SettingsProperty.EntityUrlTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-entityurltemplate
            """
            return self._values.get('entity_url_template')

        @property
        def execution_url_template(self) -> typing.Optional[str]:
            """``CfnCustomActionType.SettingsProperty.ExecutionUrlTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-executionurltemplate
            """
            return self._values.get('execution_url_template')

        @property
        def revision_url_template(self) -> typing.Optional[str]:
            """``CfnCustomActionType.SettingsProperty.RevisionUrlTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-revisionurltemplate
            """
            return self._values.get('revision_url_template')

        @property
        def third_party_configuration_url(self) -> typing.Optional[str]:
            """``CfnCustomActionType.SettingsProperty.ThirdPartyConfigurationUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-customactiontype-settings.html#cfn-codepipeline-customactiontype-settings-thirdpartyconfigurationurl
            """
            return self._values.get('third_party_configuration_url')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnCustomActionTypeProps", jsii_struct_bases=[], name_mapping={'category': 'category', 'input_artifact_details': 'inputArtifactDetails', 'output_artifact_details': 'outputArtifactDetails', 'provider': 'provider', 'version': 'version', 'configuration_properties': 'configurationProperties', 'settings': 'settings', 'tags': 'tags'})
class CfnCustomActionTypeProps():
    def __init__(self, *, category: str, input_artifact_details: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable], output_artifact_details: typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable], provider: str, version: str, configuration_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.ConfigurationPropertiesProperty"]]]]]=None, settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnCustomActionType.SettingsProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::CodePipeline::CustomActionType``.

        :param category: ``AWS::CodePipeline::CustomActionType.Category``.
        :param input_artifact_details: ``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.
        :param output_artifact_details: ``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.
        :param provider: ``AWS::CodePipeline::CustomActionType.Provider``.
        :param version: ``AWS::CodePipeline::CustomActionType.Version``.
        :param configuration_properties: ``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.
        :param settings: ``AWS::CodePipeline::CustomActionType.Settings``.
        :param tags: ``AWS::CodePipeline::CustomActionType.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html
        """
        self._values = {
            'category': category,
            'input_artifact_details': input_artifact_details,
            'output_artifact_details': output_artifact_details,
            'provider': provider,
            'version': version,
        }
        if configuration_properties is not None: self._values["configuration_properties"] = configuration_properties
        if settings is not None: self._values["settings"] = settings
        if tags is not None: self._values["tags"] = tags

    @property
    def category(self) -> str:
        """``AWS::CodePipeline::CustomActionType.Category``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-category
        """
        return self._values.get('category')

    @property
    def input_artifact_details(self) -> typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.InputArtifactDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-inputartifactdetails
        """
        return self._values.get('input_artifact_details')

    @property
    def output_artifact_details(self) -> typing.Union["CfnCustomActionType.ArtifactDetailsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodePipeline::CustomActionType.OutputArtifactDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-outputartifactdetails
        """
        return self._values.get('output_artifact_details')

    @property
    def provider(self) -> str:
        """``AWS::CodePipeline::CustomActionType.Provider``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-provider
        """
        return self._values.get('provider')

    @property
    def version(self) -> str:
        """``AWS::CodePipeline::CustomActionType.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-version
        """
        return self._values.get('version')

    @property
    def configuration_properties(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCustomActionType.ConfigurationPropertiesProperty"]]]]]:
        """``AWS::CodePipeline::CustomActionType.ConfigurationProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-configurationproperties
        """
        return self._values.get('configuration_properties')

    @property
    def settings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnCustomActionType.SettingsProperty"]]]:
        """``AWS::CodePipeline::CustomActionType.Settings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-settings
        """
        return self._values.get('settings')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodePipeline::CustomActionType.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-customactiontype.html#cfn-codepipeline-customactiontype-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCustomActionTypeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPipeline(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline"):
    """A CloudFormation ``AWS::CodePipeline::Pipeline``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodePipeline::Pipeline
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, role_arn: str, stages: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "StageDeclarationProperty"]]], artifact_store: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ArtifactStoreProperty"]]]=None, artifact_stores: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ArtifactStoreMapProperty"]]]]]=None, disable_inbound_stage_transitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StageTransitionProperty"]]]]]=None, name: typing.Optional[str]=None, restart_execution_on_update: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::CodePipeline::Pipeline``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param role_arn: ``AWS::CodePipeline::Pipeline.RoleArn``.
        :param stages: ``AWS::CodePipeline::Pipeline.Stages``.
        :param artifact_store: ``AWS::CodePipeline::Pipeline.ArtifactStore``.
        :param artifact_stores: ``AWS::CodePipeline::Pipeline.ArtifactStores``.
        :param disable_inbound_stage_transitions: ``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.
        :param name: ``AWS::CodePipeline::Pipeline.Name``.
        :param restart_execution_on_update: ``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.
        :param tags: ``AWS::CodePipeline::Pipeline.Tags``.
        """
        props = CfnPipelineProps(role_arn=role_arn, stages=stages, artifact_store=artifact_store, artifact_stores=artifact_stores, disable_inbound_stage_transitions=disable_inbound_stage_transitions, name=name, restart_execution_on_update=restart_execution_on_update, tags=tags)

        jsii.create(CfnPipeline, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Version
        """
        return jsii.get(self, "attrVersion")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CodePipeline::Pipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::CodePipeline::Pipeline.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str):
        return jsii.set(self, "roleArn", value)

    @property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "StageDeclarationProperty"]]]:
        """``AWS::CodePipeline::Pipeline.Stages``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-stages
        """
        return jsii.get(self, "stages")

    @stages.setter
    def stages(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "StageDeclarationProperty"]]]):
        return jsii.set(self, "stages", value)

    @property
    @jsii.member(jsii_name="artifactStore")
    def artifact_store(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ArtifactStoreProperty"]]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStore``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstore
        """
        return jsii.get(self, "artifactStore")

    @artifact_store.setter
    def artifact_store(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ArtifactStoreProperty"]]]):
        return jsii.set(self, "artifactStore", value)

    @property
    @jsii.member(jsii_name="artifactStores")
    def artifact_stores(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ArtifactStoreMapProperty"]]]]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStores``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstores
        """
        return jsii.get(self, "artifactStores")

    @artifact_stores.setter
    def artifact_stores(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ArtifactStoreMapProperty"]]]]]):
        return jsii.set(self, "artifactStores", value)

    @property
    @jsii.member(jsii_name="disableInboundStageTransitions")
    def disable_inbound_stage_transitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StageTransitionProperty"]]]]]:
        """``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-disableinboundstagetransitions
        """
        return jsii.get(self, "disableInboundStageTransitions")

    @disable_inbound_stage_transitions.setter
    def disable_inbound_stage_transitions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "StageTransitionProperty"]]]]]):
        return jsii.set(self, "disableInboundStageTransitions", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::CodePipeline::Pipeline.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="restartExecutionOnUpdate")
    def restart_execution_on_update(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-restartexecutiononupdate
        """
        return jsii.get(self, "restartExecutionOnUpdate")

    @restart_execution_on_update.setter
    def restart_execution_on_update(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "restartExecutionOnUpdate", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ActionDeclarationProperty", jsii_struct_bases=[], name_mapping={'action_type_id': 'actionTypeId', 'name': 'name', 'configuration': 'configuration', 'input_artifacts': 'inputArtifacts', 'output_artifacts': 'outputArtifacts', 'region': 'region', 'role_arn': 'roleArn', 'run_order': 'runOrder'})
    class ActionDeclarationProperty():
        def __init__(self, *, action_type_id: typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionTypeIdProperty"], name: str, configuration: typing.Any=None, input_artifacts: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.InputArtifactProperty"]]]]]=None, output_artifacts: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.OutputArtifactProperty"]]]]]=None, region: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, run_order: typing.Optional[jsii.Number]=None):
            """
            :param action_type_id: ``CfnPipeline.ActionDeclarationProperty.ActionTypeId``.
            :param name: ``CfnPipeline.ActionDeclarationProperty.Name``.
            :param configuration: ``CfnPipeline.ActionDeclarationProperty.Configuration``.
            :param input_artifacts: ``CfnPipeline.ActionDeclarationProperty.InputArtifacts``.
            :param output_artifacts: ``CfnPipeline.ActionDeclarationProperty.OutputArtifacts``.
            :param region: ``CfnPipeline.ActionDeclarationProperty.Region``.
            :param role_arn: ``CfnPipeline.ActionDeclarationProperty.RoleArn``.
            :param run_order: ``CfnPipeline.ActionDeclarationProperty.RunOrder``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html
            """
            self._values = {
                'action_type_id': action_type_id,
                'name': name,
            }
            if configuration is not None: self._values["configuration"] = configuration
            if input_artifacts is not None: self._values["input_artifacts"] = input_artifacts
            if output_artifacts is not None: self._values["output_artifacts"] = output_artifacts
            if region is not None: self._values["region"] = region
            if role_arn is not None: self._values["role_arn"] = role_arn
            if run_order is not None: self._values["run_order"] = run_order

        @property
        def action_type_id(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionTypeIdProperty"]:
            """``CfnPipeline.ActionDeclarationProperty.ActionTypeId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid
            """
            return self._values.get('action_type_id')

        @property
        def name(self) -> str:
            """``CfnPipeline.ActionDeclarationProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-name
            """
            return self._values.get('name')

        @property
        def configuration(self) -> typing.Any:
            """``CfnPipeline.ActionDeclarationProperty.Configuration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-configuration
            """
            return self._values.get('configuration')

        @property
        def input_artifacts(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.InputArtifactProperty"]]]]]:
            """``CfnPipeline.ActionDeclarationProperty.InputArtifacts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-inputartifacts
            """
            return self._values.get('input_artifacts')

        @property
        def output_artifacts(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.OutputArtifactProperty"]]]]]:
            """``CfnPipeline.ActionDeclarationProperty.OutputArtifacts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-outputartifacts
            """
            return self._values.get('output_artifacts')

        @property
        def region(self) -> typing.Optional[str]:
            """``CfnPipeline.ActionDeclarationProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-region
            """
            return self._values.get('region')

        @property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnPipeline.ActionDeclarationProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-rolearn
            """
            return self._values.get('role_arn')

        @property
        def run_order(self) -> typing.Optional[jsii.Number]:
            """``CfnPipeline.ActionDeclarationProperty.RunOrder``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions.html#cfn-codepipeline-pipeline-stages-actions-runorder
            """
            return self._values.get('run_order')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActionDeclarationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ActionTypeIdProperty", jsii_struct_bases=[], name_mapping={'category': 'category', 'owner': 'owner', 'provider': 'provider', 'version': 'version'})
    class ActionTypeIdProperty():
        def __init__(self, *, category: str, owner: str, provider: str, version: str):
            """
            :param category: ``CfnPipeline.ActionTypeIdProperty.Category``.
            :param owner: ``CfnPipeline.ActionTypeIdProperty.Owner``.
            :param provider: ``CfnPipeline.ActionTypeIdProperty.Provider``.
            :param version: ``CfnPipeline.ActionTypeIdProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html
            """
            self._values = {
                'category': category,
                'owner': owner,
                'provider': provider,
                'version': version,
            }

        @property
        def category(self) -> str:
            """``CfnPipeline.ActionTypeIdProperty.Category``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-category
            """
            return self._values.get('category')

        @property
        def owner(self) -> str:
            """``CfnPipeline.ActionTypeIdProperty.Owner``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-owner
            """
            return self._values.get('owner')

        @property
        def provider(self) -> str:
            """``CfnPipeline.ActionTypeIdProperty.Provider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-provider
            """
            return self._values.get('provider')

        @property
        def version(self) -> str:
            """``CfnPipeline.ActionTypeIdProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-actiontypeid.html#cfn-codepipeline-pipeline-stages-actions-actiontypeid-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActionTypeIdProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ArtifactStoreMapProperty", jsii_struct_bases=[], name_mapping={'artifact_store': 'artifactStore', 'region': 'region'})
    class ArtifactStoreMapProperty():
        def __init__(self, *, artifact_store: typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreProperty"], region: str):
            """
            :param artifact_store: ``CfnPipeline.ArtifactStoreMapProperty.ArtifactStore``.
            :param region: ``CfnPipeline.ArtifactStoreMapProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html
            """
            self._values = {
                'artifact_store': artifact_store,
                'region': region,
            }

        @property
        def artifact_store(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreProperty"]:
            """``CfnPipeline.ArtifactStoreMapProperty.ArtifactStore``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html#cfn-codepipeline-pipeline-artifactstoremap-artifactstore
            """
            return self._values.get('artifact_store')

        @property
        def region(self) -> str:
            """``CfnPipeline.ArtifactStoreMapProperty.Region``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstoremap.html#cfn-codepipeline-pipeline-artifactstoremap-region
            """
            return self._values.get('region')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ArtifactStoreMapProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.ArtifactStoreProperty", jsii_struct_bases=[], name_mapping={'location': 'location', 'type': 'type', 'encryption_key': 'encryptionKey'})
    class ArtifactStoreProperty():
        def __init__(self, *, location: str, type: str, encryption_key: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPipeline.EncryptionKeyProperty"]]]=None):
            """
            :param location: ``CfnPipeline.ArtifactStoreProperty.Location``.
            :param type: ``CfnPipeline.ArtifactStoreProperty.Type``.
            :param encryption_key: ``CfnPipeline.ArtifactStoreProperty.EncryptionKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html
            """
            self._values = {
                'location': location,
                'type': type,
            }
            if encryption_key is not None: self._values["encryption_key"] = encryption_key

        @property
        def location(self) -> str:
            """``CfnPipeline.ArtifactStoreProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-location
            """
            return self._values.get('location')

        @property
        def type(self) -> str:
            """``CfnPipeline.ArtifactStoreProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-type
            """
            return self._values.get('type')

        @property
        def encryption_key(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPipeline.EncryptionKeyProperty"]]]:
            """``CfnPipeline.ArtifactStoreProperty.EncryptionKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html#cfn-codepipeline-pipeline-artifactstore-encryptionkey
            """
            return self._values.get('encryption_key')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ArtifactStoreProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.BlockerDeclarationProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'type': 'type'})
    class BlockerDeclarationProperty():
        def __init__(self, *, name: str, type: str):
            """
            :param name: ``CfnPipeline.BlockerDeclarationProperty.Name``.
            :param type: ``CfnPipeline.BlockerDeclarationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-blockers.html
            """
            self._values = {
                'name': name,
                'type': type,
            }

        @property
        def name(self) -> str:
            """``CfnPipeline.BlockerDeclarationProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-blockers.html#cfn-codepipeline-pipeline-stages-blockers-name
            """
            return self._values.get('name')

        @property
        def type(self) -> str:
            """``CfnPipeline.BlockerDeclarationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-blockers.html#cfn-codepipeline-pipeline-stages-blockers-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BlockerDeclarationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.EncryptionKeyProperty", jsii_struct_bases=[], name_mapping={'id': 'id', 'type': 'type'})
    class EncryptionKeyProperty():
        def __init__(self, *, id: str, type: str):
            """
            :param id: ``CfnPipeline.EncryptionKeyProperty.Id``.
            :param type: ``CfnPipeline.EncryptionKeyProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore-encryptionkey.html
            """
            self._values = {
                'id': id,
                'type': type,
            }

        @property
        def id(self) -> str:
            """``CfnPipeline.EncryptionKeyProperty.Id``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore-encryptionkey.html#cfn-codepipeline-pipeline-artifactstore-encryptionkey-id
            """
            return self._values.get('id')

        @property
        def type(self) -> str:
            """``CfnPipeline.EncryptionKeyProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore-encryptionkey.html#cfn-codepipeline-pipeline-artifactstore-encryptionkey-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionKeyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.InputArtifactProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class InputArtifactProperty():
        def __init__(self, *, name: str):
            """
            :param name: ``CfnPipeline.InputArtifactProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-inputartifacts.html
            """
            self._values = {
                'name': name,
            }

        @property
        def name(self) -> str:
            """``CfnPipeline.InputArtifactProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-inputartifacts.html#cfn-codepipeline-pipeline-stages-actions-inputartifacts-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InputArtifactProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.OutputArtifactProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class OutputArtifactProperty():
        def __init__(self, *, name: str):
            """
            :param name: ``CfnPipeline.OutputArtifactProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-outputartifacts.html
            """
            self._values = {
                'name': name,
            }

        @property
        def name(self) -> str:
            """``CfnPipeline.OutputArtifactProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages-actions-outputartifacts.html#cfn-codepipeline-pipeline-stages-actions-outputartifacts-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OutputArtifactProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.StageDeclarationProperty", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'name': 'name', 'blockers': 'blockers'})
    class StageDeclarationProperty():
        def __init__(self, *, actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionDeclarationProperty"]]], name: str, blockers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.BlockerDeclarationProperty"]]]]]=None):
            """
            :param actions: ``CfnPipeline.StageDeclarationProperty.Actions``.
            :param name: ``CfnPipeline.StageDeclarationProperty.Name``.
            :param blockers: ``CfnPipeline.StageDeclarationProperty.Blockers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html
            """
            self._values = {
                'actions': actions,
                'name': name,
            }
            if blockers is not None: self._values["blockers"] = blockers

        @property
        def actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ActionDeclarationProperty"]]]:
            """``CfnPipeline.StageDeclarationProperty.Actions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html#cfn-codepipeline-pipeline-stages-actions
            """
            return self._values.get('actions')

        @property
        def name(self) -> str:
            """``CfnPipeline.StageDeclarationProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html#cfn-codepipeline-pipeline-stages-name
            """
            return self._values.get('name')

        @property
        def blockers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.BlockerDeclarationProperty"]]]]]:
            """``CfnPipeline.StageDeclarationProperty.Blockers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-stages.html#cfn-codepipeline-pipeline-stages-blockers
            """
            return self._values.get('blockers')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StageDeclarationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipeline.StageTransitionProperty", jsii_struct_bases=[], name_mapping={'reason': 'reason', 'stage_name': 'stageName'})
    class StageTransitionProperty():
        def __init__(self, *, reason: str, stage_name: str):
            """
            :param reason: ``CfnPipeline.StageTransitionProperty.Reason``.
            :param stage_name: ``CfnPipeline.StageTransitionProperty.StageName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-disableinboundstagetransitions.html
            """
            self._values = {
                'reason': reason,
                'stage_name': stage_name,
            }

        @property
        def reason(self) -> str:
            """``CfnPipeline.StageTransitionProperty.Reason``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-disableinboundstagetransitions.html#cfn-codepipeline-pipeline-disableinboundstagetransitions-reason
            """
            return self._values.get('reason')

        @property
        def stage_name(self) -> str:
            """``CfnPipeline.StageTransitionProperty.StageName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-disableinboundstagetransitions.html#cfn-codepipeline-pipeline-disableinboundstagetransitions-stagename
            """
            return self._values.get('stage_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StageTransitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnPipelineProps", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'stages': 'stages', 'artifact_store': 'artifactStore', 'artifact_stores': 'artifactStores', 'disable_inbound_stage_transitions': 'disableInboundStageTransitions', 'name': 'name', 'restart_execution_on_update': 'restartExecutionOnUpdate', 'tags': 'tags'})
class CfnPipelineProps():
    def __init__(self, *, role_arn: str, stages: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageDeclarationProperty"]]], artifact_store: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPipeline.ArtifactStoreProperty"]]]=None, artifact_stores: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreMapProperty"]]]]]=None, disable_inbound_stage_transitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageTransitionProperty"]]]]]=None, name: typing.Optional[str]=None, restart_execution_on_update: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::CodePipeline::Pipeline``.

        :param role_arn: ``AWS::CodePipeline::Pipeline.RoleArn``.
        :param stages: ``AWS::CodePipeline::Pipeline.Stages``.
        :param artifact_store: ``AWS::CodePipeline::Pipeline.ArtifactStore``.
        :param artifact_stores: ``AWS::CodePipeline::Pipeline.ArtifactStores``.
        :param disable_inbound_stage_transitions: ``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.
        :param name: ``AWS::CodePipeline::Pipeline.Name``.
        :param restart_execution_on_update: ``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.
        :param tags: ``AWS::CodePipeline::Pipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html
        """
        self._values = {
            'role_arn': role_arn,
            'stages': stages,
        }
        if artifact_store is not None: self._values["artifact_store"] = artifact_store
        if artifact_stores is not None: self._values["artifact_stores"] = artifact_stores
        if disable_inbound_stage_transitions is not None: self._values["disable_inbound_stage_transitions"] = disable_inbound_stage_transitions
        if name is not None: self._values["name"] = name
        if restart_execution_on_update is not None: self._values["restart_execution_on_update"] = restart_execution_on_update
        if tags is not None: self._values["tags"] = tags

    @property
    def role_arn(self) -> str:
        """``AWS::CodePipeline::Pipeline.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-rolearn
        """
        return self._values.get('role_arn')

    @property
    def stages(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageDeclarationProperty"]]]:
        """``AWS::CodePipeline::Pipeline.Stages``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-stages
        """
        return self._values.get('stages')

    @property
    def artifact_store(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPipeline.ArtifactStoreProperty"]]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStore``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstore
        """
        return self._values.get('artifact_store')

    @property
    def artifact_stores(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.ArtifactStoreMapProperty"]]]]]:
        """``AWS::CodePipeline::Pipeline.ArtifactStores``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-artifactstores
        """
        return self._values.get('artifact_stores')

    @property
    def disable_inbound_stage_transitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPipeline.StageTransitionProperty"]]]]]:
        """``AWS::CodePipeline::Pipeline.DisableInboundStageTransitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-disableinboundstagetransitions
        """
        return self._values.get('disable_inbound_stage_transitions')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::CodePipeline::Pipeline.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-name
        """
        return self._values.get('name')

    @property
    def restart_execution_on_update(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodePipeline::Pipeline.RestartExecutionOnUpdate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-restartexecutiononupdate
        """
        return self._values.get('restart_execution_on_update')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodePipeline::Pipeline.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html#cfn-codepipeline-pipeline-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPipelineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWebhook(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook"):
    """A CloudFormation ``AWS::CodePipeline::Webhook``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodePipeline::Webhook
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, authentication: str, authentication_configuration: typing.Union[aws_cdk.core.IResolvable, "WebhookAuthConfigurationProperty"], filters: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "WebhookFilterRuleProperty"]]], target_action: str, target_pipeline: str, target_pipeline_version: jsii.Number, name: typing.Optional[str]=None, register_with_third_party: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None) -> None:
        """Create a new ``AWS::CodePipeline::Webhook``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param authentication: ``AWS::CodePipeline::Webhook.Authentication``.
        :param authentication_configuration: ``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.
        :param filters: ``AWS::CodePipeline::Webhook.Filters``.
        :param target_action: ``AWS::CodePipeline::Webhook.TargetAction``.
        :param target_pipeline: ``AWS::CodePipeline::Webhook.TargetPipeline``.
        :param target_pipeline_version: ``AWS::CodePipeline::Webhook.TargetPipelineVersion``.
        :param name: ``AWS::CodePipeline::Webhook.Name``.
        :param register_with_third_party: ``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.
        """
        props = CfnWebhookProps(authentication=authentication, authentication_configuration=authentication_configuration, filters=filters, target_action=target_action, target_pipeline=target_pipeline, target_pipeline_version=target_pipeline_version, name=name, register_with_third_party=register_with_third_party)

        jsii.create(CfnWebhook, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrUrl")
    def attr_url(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Url
        """
        return jsii.get(self, "attrUrl")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> str:
        """``AWS::CodePipeline::Webhook.Authentication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authentication
        """
        return jsii.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: str):
        return jsii.set(self, "authentication", value)

    @property
    @jsii.member(jsii_name="authenticationConfiguration")
    def authentication_configuration(self) -> typing.Union[aws_cdk.core.IResolvable, "WebhookAuthConfigurationProperty"]:
        """``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authenticationconfiguration
        """
        return jsii.get(self, "authenticationConfiguration")

    @authentication_configuration.setter
    def authentication_configuration(self, value: typing.Union[aws_cdk.core.IResolvable, "WebhookAuthConfigurationProperty"]):
        return jsii.set(self, "authenticationConfiguration", value)

    @property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "WebhookFilterRuleProperty"]]]:
        """``AWS::CodePipeline::Webhook.Filters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-filters
        """
        return jsii.get(self, "filters")

    @filters.setter
    def filters(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "WebhookFilterRuleProperty"]]]):
        return jsii.set(self, "filters", value)

    @property
    @jsii.member(jsii_name="targetAction")
    def target_action(self) -> str:
        """``AWS::CodePipeline::Webhook.TargetAction``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetaction
        """
        return jsii.get(self, "targetAction")

    @target_action.setter
    def target_action(self, value: str):
        return jsii.set(self, "targetAction", value)

    @property
    @jsii.member(jsii_name="targetPipeline")
    def target_pipeline(self) -> str:
        """``AWS::CodePipeline::Webhook.TargetPipeline``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipeline
        """
        return jsii.get(self, "targetPipeline")

    @target_pipeline.setter
    def target_pipeline(self, value: str):
        return jsii.set(self, "targetPipeline", value)

    @property
    @jsii.member(jsii_name="targetPipelineVersion")
    def target_pipeline_version(self) -> jsii.Number:
        """``AWS::CodePipeline::Webhook.TargetPipelineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipelineversion
        """
        return jsii.get(self, "targetPipelineVersion")

    @target_pipeline_version.setter
    def target_pipeline_version(self, value: jsii.Number):
        return jsii.set(self, "targetPipelineVersion", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::CodePipeline::Webhook.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="registerWithThirdParty")
    def register_with_third_party(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-registerwiththirdparty
        """
        return jsii.get(self, "registerWithThirdParty")

    @register_with_third_party.setter
    def register_with_third_party(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "registerWithThirdParty", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook.WebhookAuthConfigurationProperty", jsii_struct_bases=[], name_mapping={'allowed_ip_range': 'allowedIpRange', 'secret_token': 'secretToken'})
    class WebhookAuthConfigurationProperty():
        def __init__(self, *, allowed_ip_range: typing.Optional[str]=None, secret_token: typing.Optional[str]=None):
            """
            :param allowed_ip_range: ``CfnWebhook.WebhookAuthConfigurationProperty.AllowedIPRange``.
            :param secret_token: ``CfnWebhook.WebhookAuthConfigurationProperty.SecretToken``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html
            """
            self._values = {
            }
            if allowed_ip_range is not None: self._values["allowed_ip_range"] = allowed_ip_range
            if secret_token is not None: self._values["secret_token"] = secret_token

        @property
        def allowed_ip_range(self) -> typing.Optional[str]:
            """``CfnWebhook.WebhookAuthConfigurationProperty.AllowedIPRange``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html#cfn-codepipeline-webhook-webhookauthconfiguration-allowediprange
            """
            return self._values.get('allowed_ip_range')

        @property
        def secret_token(self) -> typing.Optional[str]:
            """``CfnWebhook.WebhookAuthConfigurationProperty.SecretToken``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookauthconfiguration.html#cfn-codepipeline-webhook-webhookauthconfiguration-secrettoken
            """
            return self._values.get('secret_token')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WebhookAuthConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnWebhook.WebhookFilterRuleProperty", jsii_struct_bases=[], name_mapping={'json_path': 'jsonPath', 'match_equals': 'matchEquals'})
    class WebhookFilterRuleProperty():
        def __init__(self, *, json_path: str, match_equals: typing.Optional[str]=None):
            """
            :param json_path: ``CfnWebhook.WebhookFilterRuleProperty.JsonPath``.
            :param match_equals: ``CfnWebhook.WebhookFilterRuleProperty.MatchEquals``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html
            """
            self._values = {
                'json_path': json_path,
            }
            if match_equals is not None: self._values["match_equals"] = match_equals

        @property
        def json_path(self) -> str:
            """``CfnWebhook.WebhookFilterRuleProperty.JsonPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html#cfn-codepipeline-webhook-webhookfilterrule-jsonpath
            """
            return self._values.get('json_path')

        @property
        def match_equals(self) -> typing.Optional[str]:
            """``CfnWebhook.WebhookFilterRuleProperty.MatchEquals``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-webhook-webhookfilterrule.html#cfn-codepipeline-webhook-webhookfilterrule-matchequals
            """
            return self._values.get('match_equals')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WebhookFilterRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CfnWebhookProps", jsii_struct_bases=[], name_mapping={'authentication': 'authentication', 'authentication_configuration': 'authenticationConfiguration', 'filters': 'filters', 'target_action': 'targetAction', 'target_pipeline': 'targetPipeline', 'target_pipeline_version': 'targetPipelineVersion', 'name': 'name', 'register_with_third_party': 'registerWithThirdParty'})
class CfnWebhookProps():
    def __init__(self, *, authentication: str, authentication_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookAuthConfigurationProperty"], filters: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookFilterRuleProperty"]]], target_action: str, target_pipeline: str, target_pipeline_version: jsii.Number, name: typing.Optional[str]=None, register_with_third_party: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
        """Properties for defining a ``AWS::CodePipeline::Webhook``.

        :param authentication: ``AWS::CodePipeline::Webhook.Authentication``.
        :param authentication_configuration: ``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.
        :param filters: ``AWS::CodePipeline::Webhook.Filters``.
        :param target_action: ``AWS::CodePipeline::Webhook.TargetAction``.
        :param target_pipeline: ``AWS::CodePipeline::Webhook.TargetPipeline``.
        :param target_pipeline_version: ``AWS::CodePipeline::Webhook.TargetPipelineVersion``.
        :param name: ``AWS::CodePipeline::Webhook.Name``.
        :param register_with_third_party: ``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html
        """
        self._values = {
            'authentication': authentication,
            'authentication_configuration': authentication_configuration,
            'filters': filters,
            'target_action': target_action,
            'target_pipeline': target_pipeline,
            'target_pipeline_version': target_pipeline_version,
        }
        if name is not None: self._values["name"] = name
        if register_with_third_party is not None: self._values["register_with_third_party"] = register_with_third_party

    @property
    def authentication(self) -> str:
        """``AWS::CodePipeline::Webhook.Authentication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authentication
        """
        return self._values.get('authentication')

    @property
    def authentication_configuration(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookAuthConfigurationProperty"]:
        """``AWS::CodePipeline::Webhook.AuthenticationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-authenticationconfiguration
        """
        return self._values.get('authentication_configuration')

    @property
    def filters(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWebhook.WebhookFilterRuleProperty"]]]:
        """``AWS::CodePipeline::Webhook.Filters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-filters
        """
        return self._values.get('filters')

    @property
    def target_action(self) -> str:
        """``AWS::CodePipeline::Webhook.TargetAction``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetaction
        """
        return self._values.get('target_action')

    @property
    def target_pipeline(self) -> str:
        """``AWS::CodePipeline::Webhook.TargetPipeline``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipeline
        """
        return self._values.get('target_pipeline')

    @property
    def target_pipeline_version(self) -> jsii.Number:
        """``AWS::CodePipeline::Webhook.TargetPipelineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-targetpipelineversion
        """
        return self._values.get('target_pipeline_version')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::CodePipeline::Webhook.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-name
        """
        return self._values.get('name')

    @property
    def register_with_third_party(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodePipeline::Webhook.RegisterWithThirdParty``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-webhook.html#cfn-codepipeline-webhook-registerwiththirdparty
        """
        return self._values.get('register_with_third_party')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnWebhookProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CommonActionProps", jsii_struct_bases=[], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder'})
class CommonActionProps():
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None):
        """Common properties shared by all Actions.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        self._values = {
            'action_name': action_name,
        }
        if run_order is not None: self._values["run_order"] = run_order

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CommonAwsActionProps", jsii_struct_bases=[CommonActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role'})
class CommonAwsActionProps(CommonActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Common properties shared by all Actions whose {@link ActionProperties.owner} field is 'AWS' (or unset, as 'AWS' is the default).

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        """
        self._values = {
            'action_name': action_name,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonAwsActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.CrossRegionSupport", jsii_struct_bases=[], name_mapping={'replication_bucket': 'replicationBucket', 'stack': 'stack'})
class CrossRegionSupport():
    def __init__(self, *, replication_bucket: aws_cdk.aws_s3.IBucket, stack: aws_cdk.core.Stack):
        """An interface representing resources generated in order to support the cross-region capabilities of CodePipeline. You get instances of this interface from the {@link Pipeline#crossRegionSupport} property.

        :param replication_bucket: The replication Bucket used by CodePipeline to operate in this region. Belongs to {@link stack}.
        :param stack: The Stack that has been created to house the replication Bucket required for this region.

        stability
        :stability: experimental
        """
        self._values = {
            'replication_bucket': replication_bucket,
            'stack': stack,
        }

    @property
    def replication_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The replication Bucket used by CodePipeline to operate in this region. Belongs to {@link stack}.

        stability
        :stability: experimental
        """
        return self._values.get('replication_bucket')

    @property
    def stack(self) -> aws_cdk.core.Stack:
        """The Stack that has been created to house the replication Bucket required for this  region.

        stability
        :stability: experimental
        """
        return self._values.get('stack')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CrossRegionSupport(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IAction")
class IAction(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IActionProxy

    @property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> "ActionProperties":
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, stage: "IStage", *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> "ActionConfig":
        """
        :param scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_bus: typing.Optional[aws_cdk.aws_events.IEventBus]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional[aws_cdk.aws_events.Schedule]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]=None) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        ...


class _IActionProxy():
    __jsii_type__ = "@aws-cdk/aws-codepipeline.IAction"
    @property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> "ActionProperties":
        return jsii.get(self, "actionProperties")

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, stage: "IStage", *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> "ActionConfig":
        """
        :param scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_bus: typing.Optional[aws_cdk.aws_events.IEventBus]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional[aws_cdk.aws_events.Schedule]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]=None) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        options = aws_cdk.aws_events.RuleProps(description=description, enabled=enabled, event_bus=event_bus, event_pattern=event_pattern, rule_name=rule_name, schedule=schedule, targets=targets)

        return jsii.invoke(self, "onStateChange", [name, target, options])


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IPipeline")
class IPipeline(aws_cdk.core.IResource, jsii.compat.Protocol):
    """The abstract view of an AWS CodePipeline as required and used by Actions. It extends {@link events.IRuleTarget}, so this interface can be used as a Target for CloudWatch Events."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IPipelineProxy

    @property
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> str:
        """The ARN of the Pipeline.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        """The name of the Pipeline.

        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by this CodePipeline.

        :param id: Identifier for this event handler.
        :param options: Additional options to pass to the event rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by the "CodePipeline Pipeline Execution State Change" event emitted from this pipeline.

        :param id: Identifier for this event handler.
        :param options: Additional options to pass to the event rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...


class _IPipelineProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """The abstract view of an AWS CodePipeline as required and used by Actions. It extends {@link events.IRuleTarget}, so this interface can be used as a Target for CloudWatch Events."""
    __jsii_type__ = "@aws-cdk/aws-codepipeline.IPipeline"
    @property
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> str:
        """The ARN of the Pipeline.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "pipelineArn")

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        """The name of the Pipeline.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "pipelineName")

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by this CodePipeline.

        :param id: Identifier for this event handler.
        :param options: Additional options to pass to the event rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Define an event rule triggered by the "CodePipeline Pipeline Execution State Change" event emitted from this pipeline.

        :param id: Identifier for this event handler.
        :param options: Additional options to pass to the event rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onStateChange", [id, options])


@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline.IStage")
class IStage(jsii.compat.Protocol):
    """The abstract interface of a Pipeline Stage that is used by Actions."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IStageProxy

    @property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> "IPipeline":
        ...

    @property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """The physical, human-readable name of this Pipeline Stage."""
        ...

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: "IAction") -> None:
        """
        :param action: -
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_bus: typing.Optional[aws_cdk.aws_events.IEventBus]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional[aws_cdk.aws_events.Schedule]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]=None) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        ...


class _IStageProxy():
    """The abstract interface of a Pipeline Stage that is used by Actions."""
    __jsii_type__ = "@aws-cdk/aws-codepipeline.IStage"
    @property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> "IPipeline":
        return jsii.get(self, "pipeline")

    @property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """The physical, human-readable name of this Pipeline Stage."""
        return jsii.get(self, "stageName")

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: "IAction") -> None:
        """
        :param action: -
        """
        return jsii.invoke(self, "addAction", [action])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_bus: typing.Optional[aws_cdk.aws_events.IEventBus]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional[aws_cdk.aws_events.Schedule]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]=None) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.
        """
        options = aws_cdk.aws_events.RuleProps(description=description, enabled=enabled, event_bus=event_bus, event_pattern=event_pattern, rule_name=rule_name, schedule=schedule, targets=targets)

        return jsii.invoke(self, "onStateChange", [name, target, options])


@jsii.implements(IPipeline)
class Pipeline(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline.Pipeline"):
    """An AWS CodePipeline pipeline with its associated IAM role and S3 bucket.

    Example::

        # Example automatically generated. See https://github.com/aws/jsii/issues/826
        # create a pipeline
        pipeline = Pipeline(self, "Pipeline")
        
        # add a stage
        source_stage = pipeline.add_stage(name="Source")
        
        # add a source action to the stage
        source_stage.add_action(codepipeline_actions.CodeCommitSourceAction(
            action_name="Source",
            output_artifact_name="SourceArtifact",
            repository=repo
        ))
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, artifact_bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, cross_region_replication_buckets: typing.Optional[typing.Mapping[str,aws_cdk.aws_s3.IBucket]]=None, pipeline_name: typing.Optional[str]=None, restart_execution_on_update: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, stages: typing.Optional[typing.List["StageProps"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param artifact_bucket: The S3 bucket used by this Pipeline to store artifacts. Default: - A new S3 bucket will be created.
        :param cross_region_replication_buckets: A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Default: - None.
        :param pipeline_name: Name of the pipeline. Default: - AWS CloudFormation generates an ID and uses that for the pipeline name.
        :param restart_execution_on_update: Indicates whether to rerun the AWS CodePipeline pipeline after you update it. Default: false
        :param role: The IAM role to be assumed by this Pipeline. Default: a new IAM role will be created.
        :param stages: The list of Stages, in order, to create this Pipeline with. You can always add more Stages later by calling {@link Pipeline#addStage}. Default: - None.
        """
        props = PipelineProps(artifact_bucket=artifact_bucket, cross_region_replication_buckets=cross_region_replication_buckets, pipeline_name=pipeline_name, restart_execution_on_update=restart_execution_on_update, role=role, stages=stages)

        jsii.create(Pipeline, self, [scope, id, props])

    @jsii.member(jsii_name="fromPipelineArn")
    @classmethod
    def from_pipeline_arn(cls, scope: aws_cdk.core.Construct, id: str, pipeline_arn: str) -> "IPipeline":
        """Import a pipeline into this app.

        :param scope: the scope into which to import this pipeline.
        :param id: the logical ID of the returned pipeline construct.
        :param pipeline_arn: The ARN of the pipeline (e.g. ``arn:aws:codepipeline:us-east-1:123456789012:MyDemoPipeline``).
        """
        return jsii.sinvoke(cls, "fromPipelineArn", [scope, id, pipeline_arn])

    @jsii.member(jsii_name="addStage")
    def add_stage(self, *, placement: typing.Optional["StagePlacement"]=None, stage_name: str, actions: typing.Optional[typing.List["IAction"]]=None) -> "IStage":
        """Creates a new Stage, and adds it to this Pipeline.

        :param props: the creation properties of the new Stage.
        :param placement: 
        :param stage_name: The physical, human-readable name to assign to this Pipeline Stage.
        :param actions: The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}.

        return
        :return: the newly created Stage
        """
        props = StageOptions(placement=placement, stage_name=stage_name, actions=actions)

        return jsii.invoke(self, "addStage", [props])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the pipeline role.

        :param statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule triggered by this CodePipeline.

        :param id: Identifier for this event handler.
        :param options: Additional options to pass to the event rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule triggered by the "CodePipeline Pipeline Execution State Change" event emitted from this pipeline.

        :param id: Identifier for this event handler.
        :param options: Additional options to pass to the event rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onStateChange", [id, options])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the pipeline structure.

        Validation happens according to the rules documented at

        https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#pipeline-requirements

        override:
        :override:: true
        """
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="artifactBucket")
    def artifact_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """Bucket used to store output artifacts."""
        return jsii.get(self, "artifactBucket")

    @property
    @jsii.member(jsii_name="crossRegionSupport")
    def cross_region_support(self) -> typing.Mapping[str,"CrossRegionSupport"]:
        """Returns all of the {@link CrossRegionSupportStack}s that were generated automatically when dealing with Actions that reside in a different region than the Pipeline itself.

        stability
        :stability: experimental
        """
        return jsii.get(self, "crossRegionSupport")

    @property
    @jsii.member(jsii_name="pipelineArn")
    def pipeline_arn(self) -> str:
        """ARN of this pipeline."""
        return jsii.get(self, "pipelineArn")

    @property
    @jsii.member(jsii_name="pipelineName")
    def pipeline_name(self) -> str:
        """The name of the pipeline."""
        return jsii.get(self, "pipelineName")

    @property
    @jsii.member(jsii_name="pipelineVersion")
    def pipeline_version(self) -> str:
        """The version of the pipeline.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "pipelineVersion")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The IAM role AWS CodePipeline will use to perform actions or assume roles for actions with a more specific IAM role."""
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="stageCount")
    def stage_count(self) -> jsii.Number:
        """Get the number of Stages in this Pipeline."""
        return jsii.get(self, "stageCount")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.PipelineProps", jsii_struct_bases=[], name_mapping={'artifact_bucket': 'artifactBucket', 'cross_region_replication_buckets': 'crossRegionReplicationBuckets', 'pipeline_name': 'pipelineName', 'restart_execution_on_update': 'restartExecutionOnUpdate', 'role': 'role', 'stages': 'stages'})
class PipelineProps():
    def __init__(self, *, artifact_bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, cross_region_replication_buckets: typing.Optional[typing.Mapping[str,aws_cdk.aws_s3.IBucket]]=None, pipeline_name: typing.Optional[str]=None, restart_execution_on_update: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, stages: typing.Optional[typing.List["StageProps"]]=None):
        """
        :param artifact_bucket: The S3 bucket used by this Pipeline to store artifacts. Default: - A new S3 bucket will be created.
        :param cross_region_replication_buckets: A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region. Default: - None.
        :param pipeline_name: Name of the pipeline. Default: - AWS CloudFormation generates an ID and uses that for the pipeline name.
        :param restart_execution_on_update: Indicates whether to rerun the AWS CodePipeline pipeline after you update it. Default: false
        :param role: The IAM role to be assumed by this Pipeline. Default: a new IAM role will be created.
        :param stages: The list of Stages, in order, to create this Pipeline with. You can always add more Stages later by calling {@link Pipeline#addStage}. Default: - None.
        """
        self._values = {
        }
        if artifact_bucket is not None: self._values["artifact_bucket"] = artifact_bucket
        if cross_region_replication_buckets is not None: self._values["cross_region_replication_buckets"] = cross_region_replication_buckets
        if pipeline_name is not None: self._values["pipeline_name"] = pipeline_name
        if restart_execution_on_update is not None: self._values["restart_execution_on_update"] = restart_execution_on_update
        if role is not None: self._values["role"] = role
        if stages is not None: self._values["stages"] = stages

    @property
    def artifact_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """The S3 bucket used by this Pipeline to store artifacts.

        default
        :default: - A new S3 bucket will be created.
        """
        return self._values.get('artifact_bucket')

    @property
    def cross_region_replication_buckets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_s3.IBucket]]:
        """A map of region to S3 bucket name used for cross-region CodePipeline. For every Action that you specify targeting a different region than the Pipeline itself, if you don't provide an explicit Bucket for that region using this property, the construct will automatically create a Stack containing an S3 Bucket in that region.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('cross_region_replication_buckets')

    @property
    def pipeline_name(self) -> typing.Optional[str]:
        """Name of the pipeline.

        default
        :default: - AWS CloudFormation generates an ID and uses that for the pipeline name.
        """
        return self._values.get('pipeline_name')

    @property
    def restart_execution_on_update(self) -> typing.Optional[bool]:
        """Indicates whether to rerun the AWS CodePipeline pipeline after you update it.

        default
        :default: false
        """
        return self._values.get('restart_execution_on_update')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role to be assumed by this Pipeline.

        default
        :default: a new IAM role will be created.
        """
        return self._values.get('role')

    @property
    def stages(self) -> typing.Optional[typing.List["StageProps"]]:
        """The list of Stages, in order, to create this Pipeline with. You can always add more Stages later by calling {@link Pipeline#addStage}.

        default
        :default: - None.
        """
        return self._values.get('stages')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PipelineProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StagePlacement", jsii_struct_bases=[], name_mapping={'just_after': 'justAfter', 'right_before': 'rightBefore'})
class StagePlacement():
    def __init__(self, *, just_after: typing.Optional["IStage"]=None, right_before: typing.Optional["IStage"]=None):
        """Allows you to control where to place a new Stage when it's added to the Pipeline. Note that you can provide only one of the below properties - specifying more than one will result in a validation error.

        :param just_after: Inserts the new Stage as a child of the given Stage (changing its current child Stage, if it had one).
        :param right_before: Inserts the new Stage as a parent of the given Stage (changing its current parent Stage, if it had one).

        see
        :see: #justAfter
        """
        self._values = {
        }
        if just_after is not None: self._values["just_after"] = just_after
        if right_before is not None: self._values["right_before"] = right_before

    @property
    def just_after(self) -> typing.Optional["IStage"]:
        """Inserts the new Stage as a child of the given Stage (changing its current child Stage, if it had one)."""
        return self._values.get('just_after')

    @property
    def right_before(self) -> typing.Optional["IStage"]:
        """Inserts the new Stage as a parent of the given Stage (changing its current parent Stage, if it had one)."""
        return self._values.get('right_before')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StagePlacement(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StageProps", jsii_struct_bases=[], name_mapping={'stage_name': 'stageName', 'actions': 'actions'})
class StageProps():
    def __init__(self, *, stage_name: str, actions: typing.Optional[typing.List["IAction"]]=None):
        """Construction properties of a Pipeline Stage.

        :param stage_name: The physical, human-readable name to assign to this Pipeline Stage.
        :param actions: The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}.
        """
        self._values = {
            'stage_name': stage_name,
        }
        if actions is not None: self._values["actions"] = actions

    @property
    def stage_name(self) -> str:
        """The physical, human-readable name to assign to this Pipeline Stage."""
        return self._values.get('stage_name')

    @property
    def actions(self) -> typing.Optional[typing.List["IAction"]]:
        """The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}."""
        return self._values.get('actions')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline.StageOptions", jsii_struct_bases=[StageProps], name_mapping={'stage_name': 'stageName', 'actions': 'actions', 'placement': 'placement'})
class StageOptions(StageProps):
    def __init__(self, *, stage_name: str, actions: typing.Optional[typing.List["IAction"]]=None, placement: typing.Optional["StagePlacement"]=None):
        """
        :param stage_name: The physical, human-readable name to assign to this Pipeline Stage.
        :param actions: The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}.
        :param placement: 
        """
        if isinstance(placement, dict): placement = StagePlacement(**placement)
        self._values = {
            'stage_name': stage_name,
        }
        if actions is not None: self._values["actions"] = actions
        if placement is not None: self._values["placement"] = placement

    @property
    def stage_name(self) -> str:
        """The physical, human-readable name to assign to this Pipeline Stage."""
        return self._values.get('stage_name')

    @property
    def actions(self) -> typing.Optional[typing.List["IAction"]]:
        """The list of Actions to create this Stage with. You can always add more Actions later by calling {@link IStage#addAction}."""
        return self._values.get('actions')

    @property
    def placement(self) -> typing.Optional["StagePlacement"]:
        return self._values.get('placement')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["ActionArtifactBounds", "ActionBindOptions", "ActionCategory", "ActionConfig", "ActionProperties", "Artifact", "ArtifactPath", "CfnCustomActionType", "CfnCustomActionTypeProps", "CfnPipeline", "CfnPipelineProps", "CfnWebhook", "CfnWebhookProps", "CommonActionProps", "CommonAwsActionProps", "CrossRegionSupport", "IAction", "IPipeline", "IStage", "Pipeline", "PipelineProps", "StageOptions", "StagePlacement", "StageProps", "__jsii_assembly__"]

publication.publish()
