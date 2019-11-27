"""
## AWS CodeBuild Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

AWS CodeBuild is a fully managed continuous integration service that compiles
source code, runs tests, and produces software packages that are ready to
deploy. With CodeBuild, you don’t need to provision, manage, and scale your own
build servers. CodeBuild scales continuously and processes multiple builds
concurrently, so your builds are not left waiting in a queue. You can get
started quickly by using prepackaged build environments, or you can create
custom build environments that use your own build tools. With CodeBuild, you are
charged by the minute for the compute resources you use.

## Installation

Install the module:

```console
$ npm i @aws-cdk/aws-codebuild
```

Import it into your code:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
```

The `codebuild.Project` construct represents a build project resource. See the
reference documentation for a comprehensive list of initialization properties,
methods and attributes.

## Source

Build projects are usually associated with a *source*, which is specified via
the `source` property which accepts a class that extends the `Source`
abstract base class.
The default is to have no source associated with the build project;
the `buildSpec` option is required in that case.

Here's a CodeBuild project with no source which simply prints `Hello, CodeBuild!`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
codebuild.Project(self, "MyProject",
    build_spec=codebuild.BuildSpec.from_object({
        "version": "0.2",
        "phases": {
            "build": {
                "commands": ["echo \"Hello, CodeBuild!\""
                ]
            }
        }
    })
)
```

### `CodeCommitSource`

Use an AWS CodeCommit repository as the source of this build:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codecommit as codecommit

repository = codecommit.Repository(self, "MyRepo", repository_name="foo")
codebuild.Project(self, "MyFirstCodeCommitProject",
    source=codebuild.Source.code_commit(repository=repository)
)
```

### `S3Source`

Create a CodeBuild project with an S3 bucket as the source:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_s3 as s3

bucket = s3.Bucket(self, "MyBucket")
codebuild.Project(self, "MyProject",
    source=codebuild.Source.s3(
        bucket=bucket,
        path="path/to/file.zip"
    )
)
```

### `GitHubSource` and `GitHubEnterpriseSource`

These source types can be used to build code from a GitHub repository.
Example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
git_hub_source = codebuild.Source.git_hub(
    owner="awslabs",
    repo="aws-cdk",
    webhook=True, # optional, default: true if `webhookFilteres` were provided, false otherwise
    webhook_filters=[
        codebuild.FilterGroup.in_event_of(codebuild.EventAction.PUSH).and_branch_is("master")
    ]
)
```

To provide GitHub credentials, please either go to AWS CodeBuild Console to connect
or call `ImportSourceCredentials` to persist your personal access token.
Example:

```
aws codebuild import-source-credentials --server-type GITHUB --auth-type PERSONAL_ACCESS_TOKEN --token <token_value>
```

### `BitBucketSource`

This source type can be used to build code from a BitBucket repository.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
bb_source = codebuild.Source.bit_bucket(
    owner="owner",
    repo="repo"
)
```

## CodePipeline

To add a CodeBuild Project as an Action to CodePipeline,
use the `PipelineProject` class instead of `Project`.
It's a simple class that doesn't allow you to specify `sources`,
`secondarySources`, `artifacts` or `secondaryArtifacts`,
as these are handled by setting input and output CodePipeline `Artifact` instances on the Action,
instead of setting them on the Project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
project = codebuild.PipelineProject(self, "Project")
```

For more details, see the readme of the `@aws-cdk/@aws-codepipeline` package.

## Caching

You can save time when your project builds by using a cache. A cache can store reusable pieces of your build environment and use them across multiple builds. Your build project can use one of two types of caching: Amazon S3 or local. In general, S3 caching is a good option for small and intermediate build artifacts that are more expensive to build than to download. Local caching is a good option for large intermediate build artifacts because the cache is immediately available on the build host.

### S3 Caching

With S3 caching, the cache is stored in an S3 bucket which is available from multiple hosts.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
codebuild.Project(self, "Project",
    source=codebuild.Source.bit_bucket(
        owner="awslabs",
        repo="aws-cdk"
    ),
    cache=codebuild.Cache.bucket(Bucket(self, "Bucket"))
)
```

### Local Caching

With local caching, the cache is stored on the codebuild instance itself. This is simple,
cheap and fast, but CodeBuild cannot guarantee a reuse of instance and hence cannot
guarantee cache hits. For example, when a build starts and caches files locally, if two subsequent builds start at the same time afterwards only one of those builds would get the cache. Three different cache modes are supported, which can be turned on individually.

* `LocalCacheMode.Source` caches Git metadata for primary and secondary sources.
* `LocalCacheMode.DockerLayer` caches existing Docker layers.
* `LocalCacheMode.Custom` caches directories you specify in the buildspec file.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
codebuild.Project(self, "Project",
    source=codebuild.Source.git_hub_enterprise(
        https_clone_url="https://my-github-enterprise.com/owner/repo"
    ),

    # Enable Docker AND custom caching
    cache=codebuild.Cache.local(LocalCacheMode.DockerLayer, LocalCacheMode.Custom)
)
```

## Environment

By default, projects use a small instance with an Ubuntu 18.04 image. You
can use the `environment` property to customize the build environment:

* `buildImage` defines the Docker image used. See [Images](#images) below for
  details on how to define build images.
* `computeType` defines the instance type used for the build.
* `privileged` can be set to `true` to allow privileged access.
* `environmentVariables` can be set at this level (and also at the project
  level).

## Images

The CodeBuild library supports both Linux and Windows images via the
`LinuxBuildImage` and `WindowsBuildImage` classes, respectively.

You can either specify one of the predefined Windows/Linux images by using one
of the constants such as `WindowsBuildImage.WIN_SERVER_CORE_2016_BASE` or
`LinuxBuildImage.UBUNTU_14_04_RUBY_2_5_1`.

Alternatively, you can specify a custom image using one of the static methods on
`XxxBuildImage`:

* Use `.fromDockerRegistry(image[, { secretsManagerCredentials }])` to reference an image in any public or private Docker registry.
* Use `.fromEcrRepository(repo[, tag])` to reference an image available in an
  ECR repository.
* Use `.fromAsset(directory)` to use an image created from a
  local asset.

The following example shows how to define an image from a Docker asset:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
environment={
    "build_image": codebuild.LinuxBuildImage.from_asset(self, "MyImage",
        directory=path.join(__dirname, "demo-image")
    )
}
```

The following example shows how to define an image from an ECR repository:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
environment={
    "build_image": codebuild.LinuxBuildImage.from_ecr_repository(ecr_repository, "v1.0")
}
```

The following example shows how to define an image from a private docker registry:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
environment={
    "build_image": codebuild.LinuxBuildImage.from_docker_registry("my-registry/my-repo",
        secrets_manager_credentials=secrets
    )
}
```

## Events

CodeBuild projects can be used either as a source for events or be triggered
by events via an event rule.

### Using Project as an event target

The `@aws-cdk/aws-events-targets.CodeBuildProject` allows using an AWS CodeBuild
project as a AWS CloudWatch event rule target:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# start build when a commit is pushed
targets = require("@aws-cdk/aws-events-targets")

code_commit_repository.on_commit("OnCommit", targets.CodeBuildProject(project))
```

### Using Project as an event source

To define Amazon CloudWatch event rules for build projects, use one of the `onXxx`
methods:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
rule = project.on_state_change("BuildStateChange",
    target=targets.LambdaFunction(fn)
)
```

## Secondary sources and artifacts

CodeBuild Projects can get their sources from multiple places, and produce
multiple outputs. For example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
project = codebuild.Project(self, "MyProject",
    secondary_sources=[
        codebuild.Source.code_commit(
            identifier="source2",
            repository=repo
        )
    ],
    secondary_artifacts=[
        codebuild.Artifacts.s3(
            identifier="artifact2",
            bucket=bucket,
            path="some/path",
            name="file.zip"
        )
    ]
)
```

Note that the `identifier` property is required for both secondary sources and
artifacts.

The contents of the secondary source is available to the build under the
directory specified by the `CODEBUILD_SRC_DIR_<identifier>` environment variable
(so, `CODEBUILD_SRC_DIR_source2` in the above case).

The secondary artifacts have their own section in the buildspec, under the
regular `artifacts` one. Each secondary artifact has its own section, beginning
with their identifier.

So, a buildspec for the above Project could look something like this:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
project = codebuild.Project(self, "MyProject",
    # secondary sources and artifacts as above...
    build_spec=codebuild.BuildSpec.from_object(
        version="0.2",
        phases={
            "build": {
                "commands": ["cd $CODEBUILD_SRC_DIR_source2", "touch output2.txt"
                ]
            }
        },
        artifacts={
            "secondary-artifacts": {
                "artifact2": {
                    "base-directory": "$CODEBUILD_SRC_DIR_source2",
                    "files": ["output2.txt"
                    ]
                }
            }
        }
    )
)
```

### Definition of VPC configuration in CodeBuild Project

Typically, resources in an VPC are not accessible by AWS CodeBuild. To enable
access, you must provide additional VPC-specific configuration information as
part of your CodeBuild project configuration. This includes the VPC ID, the
VPC subnet IDs, and the VPC security group IDs. VPC-enabled builds are then
able to access resources inside your VPC.

For further Information see https://docs.aws.amazon.com/codebuild/latest/userguide/vpc-support.html

**Use Cases**
VPC connectivity from AWS CodeBuild builds makes it possible to:

* Run integration tests from your build against data in an Amazon RDS database that's isolated on a private subnet.
* Query data in an Amazon ElastiCache cluster directly from tests.
* Interact with internal web services hosted on Amazon EC2, Amazon ECS, or services that use internal Elastic Load Balancing.
* Retrieve dependencies from self-hosted, internal artifact repositories, such as PyPI for Python, Maven for Java, and npm for Node.js.
* Access objects in an Amazon S3 bucket configured to allow access through an Amazon VPC endpoint only.
* Query external web services that require fixed IP addresses through the Elastic IP address of the NAT gateway or NAT instance associated with your subnet(s).

Your builds can access any resource that's hosted in your VPC.

**Enable Amazon VPC Access in your CodeBuild Projects**

Pass the VPC when defining your Project, then make sure to
give the CodeBuild's security group the right permissions
to access the resources that it needs by using the
`connections` object.

For example:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(self, "MyVPC")
project = codebuild.Project(self, "MyProject",
    vpc=vpc,
    build_spec=codebuild.BuildSpec.from_object()
)

project.connections.allow_to(load_balancer, ec2.Port.tcp(443))
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

import aws_cdk.assets
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_codecommit
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecr_assets
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.aws_s3_assets
import aws_cdk.aws_secretsmanager
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codebuild", "1.18.0", __name__, "aws-codebuild@1.18.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.ArtifactsConfig", jsii_struct_bases=[], name_mapping={'artifacts_property': 'artifactsProperty'})
class ArtifactsConfig():
    def __init__(self, *, artifacts_property: "CfnProject.ArtifactsProperty"):
        """The type returned from {@link IArtifacts#bind}.

        :param artifacts_property: The low-level CloudFormation artifacts property.
        """
        if isinstance(artifacts_property, dict): artifacts_property = CfnProject.ArtifactsProperty(**artifacts_property)
        self._values = {
            'artifacts_property': artifacts_property,
        }

    @property
    def artifacts_property(self) -> "CfnProject.ArtifactsProperty":
        """The low-level CloudFormation artifacts property."""
        return self._values.get('artifacts_property')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ArtifactsConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.ArtifactsProps", jsii_struct_bases=[], name_mapping={'identifier': 'identifier'})
class ArtifactsProps():
    def __init__(self, *, identifier: typing.Optional[str]=None):
        """Properties common to all Artifacts classes.

        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        """
        self._values = {
        }
        if identifier is not None: self._values["identifier"] = identifier

    @property
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier. This property is required on secondary artifacts."""
        return self._values.get('identifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ArtifactsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BindToCodePipelineOptions", jsii_struct_bases=[], name_mapping={'artifact_bucket': 'artifactBucket'})
class BindToCodePipelineOptions():
    def __init__(self, *, artifact_bucket: aws_cdk.aws_s3.IBucket):
        """The extra options passed to the {@link IProject.bindToCodePipeline} method.

        :param artifact_bucket: The artifact bucket that will be used by the action that invokes this project.
        """
        self._values = {
            'artifact_bucket': artifact_bucket,
        }

    @property
    def artifact_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The artifact bucket that will be used by the action that invokes this project."""
        return self._values.get('artifact_bucket')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BindToCodePipelineOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BucketCacheOptions", jsii_struct_bases=[], name_mapping={'prefix': 'prefix'})
class BucketCacheOptions():
    def __init__(self, *, prefix: typing.Optional[str]=None):
        """
        :param prefix: The prefix to use to store the cache in the bucket.
        """
        self._values = {
        }
        if prefix is not None: self._values["prefix"] = prefix

    @property
    def prefix(self) -> typing.Optional[str]:
        """The prefix to use to store the cache in the bucket."""
        return self._values.get('prefix')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketCacheOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BuildEnvironment", jsii_struct_bases=[], name_mapping={'build_image': 'buildImage', 'compute_type': 'computeType', 'environment_variables': 'environmentVariables', 'privileged': 'privileged'})
class BuildEnvironment():
    def __init__(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None):
        """
        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        self._values = {
        }
        if build_image is not None: self._values["build_image"] = build_image
        if compute_type is not None: self._values["compute_type"] = compute_type
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if privileged is not None: self._values["privileged"] = privileged

    @property
    def build_image(self) -> typing.Optional["IBuildImage"]:
        """The image used for the builds.

        default
        :default: LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get('build_image')

    @property
    def compute_type(self) -> typing.Optional["ComputeType"]:
        """The type of compute to use for this build. See the {@link ComputeType} enum for the possible values.

        default
        :default: taken from {@link #buildImage#defaultComputeType}
        """
        return self._values.get('compute_type')

    @property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]:
        """The environment variables that your builds can use."""
        return self._values.get('environment_variables')

    @property
    def privileged(self) -> typing.Optional[bool]:
        """Indicates how the project builds Docker images.

        Specify true to enable
        running the Docker daemon inside a Docker container. This value must be
        set to true only if this build project will be used to build Docker
        images, and the specified build environment image is not one provided by
        AWS CodeBuild with Docker support. Otherwise, all associated builds that
        attempt to interact with the Docker daemon will fail.

        default
        :default: false
        """
        return self._values.get('privileged')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildEnvironment(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BuildEnvironmentVariable", jsii_struct_bases=[], name_mapping={'value': 'value', 'type': 'type'})
class BuildEnvironmentVariable():
    def __init__(self, *, value: typing.Any, type: typing.Optional["BuildEnvironmentVariableType"]=None):
        """
        :param value: The value of the environment variable (or the name of the parameter in the SSM parameter store.).
        :param type: The type of environment variable. Default: PlainText
        """
        self._values = {
            'value': value,
        }
        if type is not None: self._values["type"] = type

    @property
    def value(self) -> typing.Any:
        """The value of the environment variable (or the name of the parameter in the SSM parameter store.)."""
        return self._values.get('value')

    @property
    def type(self) -> typing.Optional["BuildEnvironmentVariableType"]:
        """The type of environment variable.

        default
        :default: PlainText
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildEnvironmentVariable(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.BuildEnvironmentVariableType")
class BuildEnvironmentVariableType(enum.Enum):
    PLAINTEXT = "PLAINTEXT"
    """An environment variable in plaintext format."""
    PARAMETER_STORE = "PARAMETER_STORE"
    """An environment variable stored in Systems Manager Parameter Store."""

class BuildSpec(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.BuildSpec"):
    """BuildSpec for CodeBuild projects."""
    @staticmethod
    def __jsii_proxy_class__():
        return _BuildSpecProxy

    def __init__(self) -> None:
        jsii.create(BuildSpec, self, [])

    @jsii.member(jsii_name="fromObject")
    @classmethod
    def from_object(cls, value: typing.Mapping[str,typing.Any]) -> "BuildSpec":
        """
        :param value: -
        """
        return jsii.sinvoke(cls, "fromObject", [value])

    @jsii.member(jsii_name="fromSourceFilename")
    @classmethod
    def from_source_filename(cls, filename: str) -> "BuildSpec":
        """Use a file from the source as buildspec.

        Use this if you want to use a file different from 'buildspec.yml'`

        :param filename: -
        """
        return jsii.sinvoke(cls, "fromSourceFilename", [filename])

    @jsii.member(jsii_name="toBuildSpec")
    @abc.abstractmethod
    def to_build_spec(self) -> str:
        """Render the represented BuildSpec."""
        ...

    @property
    @jsii.member(jsii_name="isImmediate")
    @abc.abstractmethod
    def is_immediate(self) -> bool:
        """Whether the buildspec is directly available or deferred until build-time."""
        ...


class _BuildSpecProxy(BuildSpec):
    @jsii.member(jsii_name="toBuildSpec")
    def to_build_spec(self) -> str:
        """Render the represented BuildSpec."""
        return jsii.invoke(self, "toBuildSpec", [])

    @property
    @jsii.member(jsii_name="isImmediate")
    def is_immediate(self) -> bool:
        """Whether the buildspec is directly available or deferred until build-time."""
        return jsii.get(self, "isImmediate")


class Cache(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.Cache"):
    """Cache options for CodeBuild Project. A cache can store reusable pieces of your build environment and use them across multiple builds.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-caching.html
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _CacheProxy

    def __init__(self) -> None:
        jsii.create(Cache, self, [])

    @jsii.member(jsii_name="bucket")
    @classmethod
    def bucket(cls, bucket: aws_cdk.aws_s3.IBucket, *, prefix: typing.Optional[str]=None) -> "Cache":
        """Create an S3 caching strategy.

        :param bucket: the S3 bucket to use for caching.
        :param options: additional options to pass to the S3 caching.
        :param prefix: The prefix to use to store the cache in the bucket.
        """
        options = BucketCacheOptions(prefix=prefix)

        return jsii.sinvoke(cls, "bucket", [bucket, options])

    @jsii.member(jsii_name="local")
    @classmethod
    def local(cls, *modes: "LocalCacheMode") -> "Cache":
        """Create a local caching strategy.

        :param modes: the mode(s) to enable for local caching.
        """
        return jsii.sinvoke(cls, "local", [*modes])

    @jsii.member(jsii_name="none")
    @classmethod
    def none(cls) -> "Cache":
        return jsii.sinvoke(cls, "none", [])


class _CacheProxy(Cache):
    pass

@jsii.implements(aws_cdk.core.IInspectable)
class CfnProject(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.CfnProject"):
    """A CloudFormation ``AWS::CodeBuild::Project``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::Project
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, artifacts: typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable], environment: typing.Union[aws_cdk.core.IResolvable, "EnvironmentProperty"], service_role: str, source: typing.Union["SourceProperty", aws_cdk.core.IResolvable], badge_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProjectCacheProperty"]]]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[str]=None, logs_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LogsConfigProperty"]]]=None, name: typing.Optional[str]=None, queued_timeout_in_minutes: typing.Optional[jsii.Number]=None, secondary_artifacts: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]]]]]=None, secondary_sources: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["SourceProperty", aws_cdk.core.IResolvable]]]]]=None, secondary_source_versions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ProjectSourceVersionProperty"]]]]]=None, source_version: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, timeout_in_minutes: typing.Optional[jsii.Number]=None, triggers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProjectTriggersProperty"]]]=None, vpc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigProperty"]]]=None) -> None:
        """Create a new ``AWS::CodeBuild::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param artifacts: ``AWS::CodeBuild::Project.Artifacts``.
        :param environment: ``AWS::CodeBuild::Project.Environment``.
        :param service_role: ``AWS::CodeBuild::Project.ServiceRole``.
        :param source: ``AWS::CodeBuild::Project.Source``.
        :param badge_enabled: ``AWS::CodeBuild::Project.BadgeEnabled``.
        :param cache: ``AWS::CodeBuild::Project.Cache``.
        :param description: ``AWS::CodeBuild::Project.Description``.
        :param encryption_key: ``AWS::CodeBuild::Project.EncryptionKey``.
        :param logs_config: ``AWS::CodeBuild::Project.LogsConfig``.
        :param name: ``AWS::CodeBuild::Project.Name``.
        :param queued_timeout_in_minutes: ``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.
        :param secondary_artifacts: ``AWS::CodeBuild::Project.SecondaryArtifacts``.
        :param secondary_sources: ``AWS::CodeBuild::Project.SecondarySources``.
        :param secondary_source_versions: ``AWS::CodeBuild::Project.SecondarySourceVersions``.
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``.
        :param tags: ``AWS::CodeBuild::Project.Tags``.
        :param timeout_in_minutes: ``AWS::CodeBuild::Project.TimeoutInMinutes``.
        :param triggers: ``AWS::CodeBuild::Project.Triggers``.
        :param vpc_config: ``AWS::CodeBuild::Project.VpcConfig``.
        """
        props = CfnProjectProps(artifacts=artifacts, environment=environment, service_role=service_role, source=source, badge_enabled=badge_enabled, cache=cache, description=description, encryption_key=encryption_key, logs_config=logs_config, name=name, queued_timeout_in_minutes=queued_timeout_in_minutes, secondary_artifacts=secondary_artifacts, secondary_sources=secondary_sources, secondary_source_versions=secondary_source_versions, source_version=source_version, tags=tags, timeout_in_minutes=timeout_in_minutes, triggers=triggers, vpc_config=vpc_config)

        jsii.create(CfnProject, self, [scope, id, props])

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
        """``AWS::CodeBuild::Project.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Artifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-artifacts
        """
        return jsii.get(self, "artifacts")

    @artifacts.setter
    def artifacts(self, value: typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]):
        return jsii.set(self, "artifacts", value)

    @property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Union[aws_cdk.core.IResolvable, "EnvironmentProperty"]:
        """``AWS::CodeBuild::Project.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment
        """
        return jsii.get(self, "environment")

    @environment.setter
    def environment(self, value: typing.Union[aws_cdk.core.IResolvable, "EnvironmentProperty"]):
        return jsii.set(self, "environment", value)

    @property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> str:
        """``AWS::CodeBuild::Project.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-servicerole
        """
        return jsii.get(self, "serviceRole")

    @service_role.setter
    def service_role(self, value: str):
        return jsii.set(self, "serviceRole", value)

    @property
    @jsii.member(jsii_name="source")
    def source(self) -> typing.Union["SourceProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-source
        """
        return jsii.get(self, "source")

    @source.setter
    def source(self, value: typing.Union["SourceProperty", aws_cdk.core.IResolvable]):
        return jsii.set(self, "source", value)

    @property
    @jsii.member(jsii_name="badgeEnabled")
    def badge_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeBuild::Project.BadgeEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-badgeenabled
        """
        return jsii.get(self, "badgeEnabled")

    @badge_enabled.setter
    def badge_enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "badgeEnabled", value)

    @property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProjectCacheProperty"]]]:
        """``AWS::CodeBuild::Project.Cache``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-cache
        """
        return jsii.get(self, "cache")

    @cache.setter
    def cache(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProjectCacheProperty"]]]):
        return jsii.set(self, "cache", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.EncryptionKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-encryptionkey
        """
        return jsii.get(self, "encryptionKey")

    @encryption_key.setter
    def encryption_key(self, value: typing.Optional[str]):
        return jsii.set(self, "encryptionKey", value)

    @property
    @jsii.member(jsii_name="logsConfig")
    def logs_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LogsConfigProperty"]]]:
        """``AWS::CodeBuild::Project.LogsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-logsconfig
        """
        return jsii.get(self, "logsConfig")

    @logs_config.setter
    def logs_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LogsConfigProperty"]]]):
        return jsii.set(self, "logsConfig", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="queuedTimeoutInMinutes")
    def queued_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-queuedtimeoutinminutes
        """
        return jsii.get(self, "queuedTimeoutInMinutes")

    @queued_timeout_in_minutes.setter
    def queued_timeout_in_minutes(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "queuedTimeoutInMinutes", value)

    @property
    @jsii.member(jsii_name="secondaryArtifacts")
    def secondary_artifacts(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::CodeBuild::Project.SecondaryArtifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondaryartifacts
        """
        return jsii.get(self, "secondaryArtifacts")

    @secondary_artifacts.setter
    def secondary_artifacts(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ArtifactsProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "secondaryArtifacts", value)

    @property
    @jsii.member(jsii_name="secondarySources")
    def secondary_sources(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["SourceProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::CodeBuild::Project.SecondarySources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysources
        """
        return jsii.get(self, "secondarySources")

    @secondary_sources.setter
    def secondary_sources(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["SourceProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "secondarySources", value)

    @property
    @jsii.member(jsii_name="secondarySourceVersions")
    def secondary_source_versions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ProjectSourceVersionProperty"]]]]]:
        """``AWS::CodeBuild::Project.SecondarySourceVersions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysourceversions
        """
        return jsii.get(self, "secondarySourceVersions")

    @secondary_source_versions.setter
    def secondary_source_versions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ProjectSourceVersionProperty"]]]]]):
        return jsii.set(self, "secondarySourceVersions", value)

    @property
    @jsii.member(jsii_name="sourceVersion")
    def source_version(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        """
        return jsii.get(self, "sourceVersion")

    @source_version.setter
    def source_version(self, value: typing.Optional[str]):
        return jsii.set(self, "sourceVersion", value)

    @property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-timeoutinminutes
        """
        return jsii.get(self, "timeoutInMinutes")

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "timeoutInMinutes", value)

    @property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProjectTriggersProperty"]]]:
        """``AWS::CodeBuild::Project.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-triggers
        """
        return jsii.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProjectTriggersProperty"]]]):
        return jsii.set(self, "triggers", value)

    @property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigProperty"]]]:
        """``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter
    def vpc_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigProperty"]]]):
        return jsii.set(self, "vpcConfig", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.ArtifactsProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'artifact_identifier': 'artifactIdentifier', 'encryption_disabled': 'encryptionDisabled', 'location': 'location', 'name': 'name', 'namespace_type': 'namespaceType', 'override_artifact_name': 'overrideArtifactName', 'packaging': 'packaging', 'path': 'path'})
    class ArtifactsProperty():
        def __init__(self, *, type: str, artifact_identifier: typing.Optional[str]=None, encryption_disabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, location: typing.Optional[str]=None, name: typing.Optional[str]=None, namespace_type: typing.Optional[str]=None, override_artifact_name: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, packaging: typing.Optional[str]=None, path: typing.Optional[str]=None):
            """
            :param type: ``CfnProject.ArtifactsProperty.Type``.
            :param artifact_identifier: ``CfnProject.ArtifactsProperty.ArtifactIdentifier``.
            :param encryption_disabled: ``CfnProject.ArtifactsProperty.EncryptionDisabled``.
            :param location: ``CfnProject.ArtifactsProperty.Location``.
            :param name: ``CfnProject.ArtifactsProperty.Name``.
            :param namespace_type: ``CfnProject.ArtifactsProperty.NamespaceType``.
            :param override_artifact_name: ``CfnProject.ArtifactsProperty.OverrideArtifactName``.
            :param packaging: ``CfnProject.ArtifactsProperty.Packaging``.
            :param path: ``CfnProject.ArtifactsProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html
            """
            self._values = {
                'type': type,
            }
            if artifact_identifier is not None: self._values["artifact_identifier"] = artifact_identifier
            if encryption_disabled is not None: self._values["encryption_disabled"] = encryption_disabled
            if location is not None: self._values["location"] = location
            if name is not None: self._values["name"] = name
            if namespace_type is not None: self._values["namespace_type"] = namespace_type
            if override_artifact_name is not None: self._values["override_artifact_name"] = override_artifact_name
            if packaging is not None: self._values["packaging"] = packaging
            if path is not None: self._values["path"] = path

        @property
        def type(self) -> str:
            """``CfnProject.ArtifactsProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-type
            """
            return self._values.get('type')

        @property
        def artifact_identifier(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.ArtifactIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-artifactidentifier
            """
            return self._values.get('artifact_identifier')

        @property
        def encryption_disabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.ArtifactsProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-encryptiondisabled
            """
            return self._values.get('encryption_disabled')

        @property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-location
            """
            return self._values.get('location')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-name
            """
            return self._values.get('name')

        @property
        def namespace_type(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.NamespaceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-namespacetype
            """
            return self._values.get('namespace_type')

        @property
        def override_artifact_name(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.ArtifactsProperty.OverrideArtifactName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-overrideartifactname
            """
            return self._values.get('override_artifact_name')

        @property
        def packaging(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Packaging``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-packaging
            """
            return self._values.get('packaging')

        @property
        def path(self) -> typing.Optional[str]:
            """``CfnProject.ArtifactsProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-artifacts.html#cfn-codebuild-project-artifacts-path
            """
            return self._values.get('path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ArtifactsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.CloudWatchLogsConfigProperty", jsii_struct_bases=[], name_mapping={'status': 'status', 'group_name': 'groupName', 'stream_name': 'streamName'})
    class CloudWatchLogsConfigProperty():
        def __init__(self, *, status: str, group_name: typing.Optional[str]=None, stream_name: typing.Optional[str]=None):
            """
            :param status: ``CfnProject.CloudWatchLogsConfigProperty.Status``.
            :param group_name: ``CfnProject.CloudWatchLogsConfigProperty.GroupName``.
            :param stream_name: ``CfnProject.CloudWatchLogsConfigProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html
            """
            self._values = {
                'status': status,
            }
            if group_name is not None: self._values["group_name"] = group_name
            if stream_name is not None: self._values["stream_name"] = stream_name

        @property
        def status(self) -> str:
            """``CfnProject.CloudWatchLogsConfigProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-status
            """
            return self._values.get('status')

        @property
        def group_name(self) -> typing.Optional[str]:
            """``CfnProject.CloudWatchLogsConfigProperty.GroupName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-groupname
            """
            return self._values.get('group_name')

        @property
        def stream_name(self) -> typing.Optional[str]:
            """``CfnProject.CloudWatchLogsConfigProperty.StreamName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-cloudwatchlogsconfig.html#cfn-codebuild-project-cloudwatchlogsconfig-streamname
            """
            return self._values.get('stream_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CloudWatchLogsConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.EnvironmentProperty", jsii_struct_bases=[], name_mapping={'compute_type': 'computeType', 'image': 'image', 'type': 'type', 'certificate': 'certificate', 'environment_variables': 'environmentVariables', 'image_pull_credentials_type': 'imagePullCredentialsType', 'privileged_mode': 'privilegedMode', 'registry_credential': 'registryCredential'})
    class EnvironmentProperty():
        def __init__(self, *, compute_type: str, image: str, type: str, certificate: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProject.EnvironmentVariableProperty"]]]]]=None, image_pull_credentials_type: typing.Optional[str]=None, privileged_mode: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, registry_credential: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.RegistryCredentialProperty"]]]=None):
            """
            :param compute_type: ``CfnProject.EnvironmentProperty.ComputeType``.
            :param image: ``CfnProject.EnvironmentProperty.Image``.
            :param type: ``CfnProject.EnvironmentProperty.Type``.
            :param certificate: ``CfnProject.EnvironmentProperty.Certificate``.
            :param environment_variables: ``CfnProject.EnvironmentProperty.EnvironmentVariables``.
            :param image_pull_credentials_type: ``CfnProject.EnvironmentProperty.ImagePullCredentialsType``.
            :param privileged_mode: ``CfnProject.EnvironmentProperty.PrivilegedMode``.
            :param registry_credential: ``CfnProject.EnvironmentProperty.RegistryCredential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html
            """
            self._values = {
                'compute_type': compute_type,
                'image': image,
                'type': type,
            }
            if certificate is not None: self._values["certificate"] = certificate
            if environment_variables is not None: self._values["environment_variables"] = environment_variables
            if image_pull_credentials_type is not None: self._values["image_pull_credentials_type"] = image_pull_credentials_type
            if privileged_mode is not None: self._values["privileged_mode"] = privileged_mode
            if registry_credential is not None: self._values["registry_credential"] = registry_credential

        @property
        def compute_type(self) -> str:
            """``CfnProject.EnvironmentProperty.ComputeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-computetype
            """
            return self._values.get('compute_type')

        @property
        def image(self) -> str:
            """``CfnProject.EnvironmentProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-image
            """
            return self._values.get('image')

        @property
        def type(self) -> str:
            """``CfnProject.EnvironmentProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-type
            """
            return self._values.get('type')

        @property
        def certificate(self) -> typing.Optional[str]:
            """``CfnProject.EnvironmentProperty.Certificate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-certificate
            """
            return self._values.get('certificate')

        @property
        def environment_variables(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProject.EnvironmentVariableProperty"]]]]]:
            """``CfnProject.EnvironmentProperty.EnvironmentVariables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-environmentvariables
            """
            return self._values.get('environment_variables')

        @property
        def image_pull_credentials_type(self) -> typing.Optional[str]:
            """``CfnProject.EnvironmentProperty.ImagePullCredentialsType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-imagepullcredentialstype
            """
            return self._values.get('image_pull_credentials_type')

        @property
        def privileged_mode(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.EnvironmentProperty.PrivilegedMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-privilegedmode
            """
            return self._values.get('privileged_mode')

        @property
        def registry_credential(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.RegistryCredentialProperty"]]]:
            """``CfnProject.EnvironmentProperty.RegistryCredential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environment.html#cfn-codebuild-project-environment-registrycredential
            """
            return self._values.get('registry_credential')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EnvironmentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.EnvironmentVariableProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value', 'type': 'type'})
    class EnvironmentVariableProperty():
        def __init__(self, *, name: str, value: str, type: typing.Optional[str]=None):
            """
            :param name: ``CfnProject.EnvironmentVariableProperty.Name``.
            :param value: ``CfnProject.EnvironmentVariableProperty.Value``.
            :param type: ``CfnProject.EnvironmentVariableProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html
            """
            self._values = {
                'name': name,
                'value': value,
            }
            if type is not None: self._values["type"] = type

        @property
        def name(self) -> str:
            """``CfnProject.EnvironmentVariableProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-name
            """
            return self._values.get('name')

        @property
        def value(self) -> str:
            """``CfnProject.EnvironmentVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-value
            """
            return self._values.get('value')

        @property
        def type(self) -> typing.Optional[str]:
            """``CfnProject.EnvironmentVariableProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-environmentvariable.html#cfn-codebuild-project-environmentvariable-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EnvironmentVariableProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.GitSubmodulesConfigProperty", jsii_struct_bases=[], name_mapping={'fetch_submodules': 'fetchSubmodules'})
    class GitSubmodulesConfigProperty():
        def __init__(self, *, fetch_submodules: typing.Union[bool, aws_cdk.core.IResolvable]):
            """
            :param fetch_submodules: ``CfnProject.GitSubmodulesConfigProperty.FetchSubmodules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html
            """
            self._values = {
                'fetch_submodules': fetch_submodules,
            }

        @property
        def fetch_submodules(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnProject.GitSubmodulesConfigProperty.FetchSubmodules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-gitsubmodulesconfig.html#cfn-codebuild-project-gitsubmodulesconfig-fetchsubmodules
            """
            return self._values.get('fetch_submodules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GitSubmodulesConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.LogsConfigProperty", jsii_struct_bases=[], name_mapping={'cloud_watch_logs': 'cloudWatchLogs', 's3_logs': 's3Logs'})
    class LogsConfigProperty():
        def __init__(self, *, cloud_watch_logs: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.CloudWatchLogsConfigProperty"]]]=None, s3_logs: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.S3LogsConfigProperty"]]]=None):
            """
            :param cloud_watch_logs: ``CfnProject.LogsConfigProperty.CloudWatchLogs``.
            :param s3_logs: ``CfnProject.LogsConfigProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html
            """
            self._values = {
            }
            if cloud_watch_logs is not None: self._values["cloud_watch_logs"] = cloud_watch_logs
            if s3_logs is not None: self._values["s3_logs"] = s3_logs

        @property
        def cloud_watch_logs(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.CloudWatchLogsConfigProperty"]]]:
            """``CfnProject.LogsConfigProperty.CloudWatchLogs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-cloudwatchlogs
            """
            return self._values.get('cloud_watch_logs')

        @property
        def s3_logs(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.S3LogsConfigProperty"]]]:
            """``CfnProject.LogsConfigProperty.S3Logs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-logsconfig.html#cfn-codebuild-project-logsconfig-s3logs
            """
            return self._values.get('s3_logs')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LogsConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectCacheProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'location': 'location', 'modes': 'modes'})
    class ProjectCacheProperty():
        def __init__(self, *, type: str, location: typing.Optional[str]=None, modes: typing.Optional[typing.List[str]]=None):
            """
            :param type: ``CfnProject.ProjectCacheProperty.Type``.
            :param location: ``CfnProject.ProjectCacheProperty.Location``.
            :param modes: ``CfnProject.ProjectCacheProperty.Modes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html
            """
            self._values = {
                'type': type,
            }
            if location is not None: self._values["location"] = location
            if modes is not None: self._values["modes"] = modes

        @property
        def type(self) -> str:
            """``CfnProject.ProjectCacheProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-type
            """
            return self._values.get('type')

        @property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.ProjectCacheProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-location
            """
            return self._values.get('location')

        @property
        def modes(self) -> typing.Optional[typing.List[str]]:
            """``CfnProject.ProjectCacheProperty.Modes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectcache.html#cfn-codebuild-project-projectcache-modes
            """
            return self._values.get('modes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProjectCacheProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectSourceVersionProperty", jsii_struct_bases=[], name_mapping={'source_identifier': 'sourceIdentifier', 'source_version': 'sourceVersion'})
    class ProjectSourceVersionProperty():
        def __init__(self, *, source_identifier: str, source_version: typing.Optional[str]=None):
            """
            :param source_identifier: ``CfnProject.ProjectSourceVersionProperty.SourceIdentifier``.
            :param source_version: ``CfnProject.ProjectSourceVersionProperty.SourceVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html
            """
            self._values = {
                'source_identifier': source_identifier,
            }
            if source_version is not None: self._values["source_version"] = source_version

        @property
        def source_identifier(self) -> str:
            """``CfnProject.ProjectSourceVersionProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceidentifier
            """
            return self._values.get('source_identifier')

        @property
        def source_version(self) -> typing.Optional[str]:
            """``CfnProject.ProjectSourceVersionProperty.SourceVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projectsourceversion.html#cfn-codebuild-project-projectsourceversion-sourceversion
            """
            return self._values.get('source_version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProjectSourceVersionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.ProjectTriggersProperty", jsii_struct_bases=[], name_mapping={'filter_groups': 'filterGroups', 'webhook': 'webhook'})
    class ProjectTriggersProperty():
        def __init__(self, *, filter_groups: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProject.WebhookFilterProperty"]]]]]]]=None, webhook: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param filter_groups: ``CfnProject.ProjectTriggersProperty.FilterGroups``.
            :param webhook: ``CfnProject.ProjectTriggersProperty.Webhook``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html
            """
            self._values = {
            }
            if filter_groups is not None: self._values["filter_groups"] = filter_groups
            if webhook is not None: self._values["webhook"] = webhook

        @property
        def filter_groups(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProject.WebhookFilterProperty"]]]]]]]:
            """``CfnProject.ProjectTriggersProperty.FilterGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-filtergroups
            """
            return self._values.get('filter_groups')

        @property
        def webhook(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.ProjectTriggersProperty.Webhook``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-projecttriggers.html#cfn-codebuild-project-projecttriggers-webhook
            """
            return self._values.get('webhook')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProjectTriggersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.RegistryCredentialProperty", jsii_struct_bases=[], name_mapping={'credential': 'credential', 'credential_provider': 'credentialProvider'})
    class RegistryCredentialProperty():
        def __init__(self, *, credential: str, credential_provider: str):
            """
            :param credential: ``CfnProject.RegistryCredentialProperty.Credential``.
            :param credential_provider: ``CfnProject.RegistryCredentialProperty.CredentialProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html
            """
            self._values = {
                'credential': credential,
                'credential_provider': credential_provider,
            }

        @property
        def credential(self) -> str:
            """``CfnProject.RegistryCredentialProperty.Credential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credential
            """
            return self._values.get('credential')

        @property
        def credential_provider(self) -> str:
            """``CfnProject.RegistryCredentialProperty.CredentialProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-registrycredential.html#cfn-codebuild-project-registrycredential-credentialprovider
            """
            return self._values.get('credential_provider')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RegistryCredentialProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.S3LogsConfigProperty", jsii_struct_bases=[], name_mapping={'status': 'status', 'encryption_disabled': 'encryptionDisabled', 'location': 'location'})
    class S3LogsConfigProperty():
        def __init__(self, *, status: str, encryption_disabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, location: typing.Optional[str]=None):
            """
            :param status: ``CfnProject.S3LogsConfigProperty.Status``.
            :param encryption_disabled: ``CfnProject.S3LogsConfigProperty.EncryptionDisabled``.
            :param location: ``CfnProject.S3LogsConfigProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html
            """
            self._values = {
                'status': status,
            }
            if encryption_disabled is not None: self._values["encryption_disabled"] = encryption_disabled
            if location is not None: self._values["location"] = location

        @property
        def status(self) -> str:
            """``CfnProject.S3LogsConfigProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-status
            """
            return self._values.get('status')

        @property
        def encryption_disabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.S3LogsConfigProperty.EncryptionDisabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-encryptiondisabled
            """
            return self._values.get('encryption_disabled')

        @property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.S3LogsConfigProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-s3logsconfig.html#cfn-codebuild-project-s3logsconfig-location
            """
            return self._values.get('location')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3LogsConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.SourceAuthProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'resource': 'resource'})
    class SourceAuthProperty():
        def __init__(self, *, type: str, resource: typing.Optional[str]=None):
            """
            :param type: ``CfnProject.SourceAuthProperty.Type``.
            :param resource: ``CfnProject.SourceAuthProperty.Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html
            """
            self._values = {
                'type': type,
            }
            if resource is not None: self._values["resource"] = resource

        @property
        def type(self) -> str:
            """``CfnProject.SourceAuthProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-type
            """
            return self._values.get('type')

        @property
        def resource(self) -> typing.Optional[str]:
            """``CfnProject.SourceAuthProperty.Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-sourceauth.html#cfn-codebuild-project-sourceauth-resource
            """
            return self._values.get('resource')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SourceAuthProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.SourceProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'auth': 'auth', 'build_spec': 'buildSpec', 'git_clone_depth': 'gitCloneDepth', 'git_submodules_config': 'gitSubmodulesConfig', 'insecure_ssl': 'insecureSsl', 'location': 'location', 'report_build_status': 'reportBuildStatus', 'source_identifier': 'sourceIdentifier'})
    class SourceProperty():
        def __init__(self, *, type: str, auth: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.SourceAuthProperty"]]]=None, build_spec: typing.Optional[str]=None, git_clone_depth: typing.Optional[jsii.Number]=None, git_submodules_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.GitSubmodulesConfigProperty"]]]=None, insecure_ssl: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, location: typing.Optional[str]=None, report_build_status: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, source_identifier: typing.Optional[str]=None):
            """
            :param type: ``CfnProject.SourceProperty.Type``.
            :param auth: ``CfnProject.SourceProperty.Auth``.
            :param build_spec: ``CfnProject.SourceProperty.BuildSpec``.
            :param git_clone_depth: ``CfnProject.SourceProperty.GitCloneDepth``.
            :param git_submodules_config: ``CfnProject.SourceProperty.GitSubmodulesConfig``.
            :param insecure_ssl: ``CfnProject.SourceProperty.InsecureSsl``.
            :param location: ``CfnProject.SourceProperty.Location``.
            :param report_build_status: ``CfnProject.SourceProperty.ReportBuildStatus``.
            :param source_identifier: ``CfnProject.SourceProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html
            """
            self._values = {
                'type': type,
            }
            if auth is not None: self._values["auth"] = auth
            if build_spec is not None: self._values["build_spec"] = build_spec
            if git_clone_depth is not None: self._values["git_clone_depth"] = git_clone_depth
            if git_submodules_config is not None: self._values["git_submodules_config"] = git_submodules_config
            if insecure_ssl is not None: self._values["insecure_ssl"] = insecure_ssl
            if location is not None: self._values["location"] = location
            if report_build_status is not None: self._values["report_build_status"] = report_build_status
            if source_identifier is not None: self._values["source_identifier"] = source_identifier

        @property
        def type(self) -> str:
            """``CfnProject.SourceProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-type
            """
            return self._values.get('type')

        @property
        def auth(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.SourceAuthProperty"]]]:
            """``CfnProject.SourceProperty.Auth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-auth
            """
            return self._values.get('auth')

        @property
        def build_spec(self) -> typing.Optional[str]:
            """``CfnProject.SourceProperty.BuildSpec``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildspec
            """
            return self._values.get('build_spec')

        @property
        def git_clone_depth(self) -> typing.Optional[jsii.Number]:
            """``CfnProject.SourceProperty.GitCloneDepth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitclonedepth
            """
            return self._values.get('git_clone_depth')

        @property
        def git_submodules_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.GitSubmodulesConfigProperty"]]]:
            """``CfnProject.SourceProperty.GitSubmodulesConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-gitsubmodulesconfig
            """
            return self._values.get('git_submodules_config')

        @property
        def insecure_ssl(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.SourceProperty.InsecureSsl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-insecuressl
            """
            return self._values.get('insecure_ssl')

        @property
        def location(self) -> typing.Optional[str]:
            """``CfnProject.SourceProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-location
            """
            return self._values.get('location')

        @property
        def report_build_status(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.SourceProperty.ReportBuildStatus``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-reportbuildstatus
            """
            return self._values.get('report_build_status')

        @property
        def source_identifier(self) -> typing.Optional[str]:
            """``CfnProject.SourceProperty.SourceIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-sourceidentifier
            """
            return self._values.get('source_identifier')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SourceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.VpcConfigProperty", jsii_struct_bases=[], name_mapping={'security_group_ids': 'securityGroupIds', 'subnets': 'subnets', 'vpc_id': 'vpcId'})
    class VpcConfigProperty():
        def __init__(self, *, security_group_ids: typing.Optional[typing.List[str]]=None, subnets: typing.Optional[typing.List[str]]=None, vpc_id: typing.Optional[str]=None):
            """
            :param security_group_ids: ``CfnProject.VpcConfigProperty.SecurityGroupIds``.
            :param subnets: ``CfnProject.VpcConfigProperty.Subnets``.
            :param vpc_id: ``CfnProject.VpcConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html
            """
            self._values = {
            }
            if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
            if subnets is not None: self._values["subnets"] = subnets
            if vpc_id is not None: self._values["vpc_id"] = vpc_id

        @property
        def security_group_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnProject.VpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-securitygroupids
            """
            return self._values.get('security_group_ids')

        @property
        def subnets(self) -> typing.Optional[typing.List[str]]:
            """``CfnProject.VpcConfigProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-subnets
            """
            return self._values.get('subnets')

        @property
        def vpc_id(self) -> typing.Optional[str]:
            """``CfnProject.VpcConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-vpcconfig.html#cfn-codebuild-project-vpcconfig-vpcid
            """
            return self._values.get('vpc_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VpcConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProject.WebhookFilterProperty", jsii_struct_bases=[], name_mapping={'pattern': 'pattern', 'type': 'type', 'exclude_matched_pattern': 'excludeMatchedPattern'})
    class WebhookFilterProperty():
        def __init__(self, *, pattern: str, type: str, exclude_matched_pattern: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param pattern: ``CfnProject.WebhookFilterProperty.Pattern``.
            :param type: ``CfnProject.WebhookFilterProperty.Type``.
            :param exclude_matched_pattern: ``CfnProject.WebhookFilterProperty.ExcludeMatchedPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html
            """
            self._values = {
                'pattern': pattern,
                'type': type,
            }
            if exclude_matched_pattern is not None: self._values["exclude_matched_pattern"] = exclude_matched_pattern

        @property
        def pattern(self) -> str:
            """``CfnProject.WebhookFilterProperty.Pattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-pattern
            """
            return self._values.get('pattern')

        @property
        def type(self) -> str:
            """``CfnProject.WebhookFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-type
            """
            return self._values.get('type')

        @property
        def exclude_matched_pattern(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnProject.WebhookFilterProperty.ExcludeMatchedPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-webhookfilter.html#cfn-codebuild-project-webhookfilter-excludematchedpattern
            """
            return self._values.get('exclude_matched_pattern')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WebhookFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnProjectProps", jsii_struct_bases=[], name_mapping={'artifacts': 'artifacts', 'environment': 'environment', 'service_role': 'serviceRole', 'source': 'source', 'badge_enabled': 'badgeEnabled', 'cache': 'cache', 'description': 'description', 'encryption_key': 'encryptionKey', 'logs_config': 'logsConfig', 'name': 'name', 'queued_timeout_in_minutes': 'queuedTimeoutInMinutes', 'secondary_artifacts': 'secondaryArtifacts', 'secondary_sources': 'secondarySources', 'secondary_source_versions': 'secondarySourceVersions', 'source_version': 'sourceVersion', 'tags': 'tags', 'timeout_in_minutes': 'timeoutInMinutes', 'triggers': 'triggers', 'vpc_config': 'vpcConfig'})
class CfnProjectProps():
    def __init__(self, *, artifacts: typing.Union["CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable], environment: typing.Union[aws_cdk.core.IResolvable, "CfnProject.EnvironmentProperty"], service_role: str, source: typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable], badge_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, cache: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.ProjectCacheProperty"]]]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[str]=None, logs_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.LogsConfigProperty"]]]=None, name: typing.Optional[str]=None, queued_timeout_in_minutes: typing.Optional[jsii.Number]=None, secondary_artifacts: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable]]]]]=None, secondary_sources: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable]]]]]=None, secondary_source_versions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProject.ProjectSourceVersionProperty"]]]]]=None, source_version: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, timeout_in_minutes: typing.Optional[jsii.Number]=None, triggers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.ProjectTriggersProperty"]]]=None, vpc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.VpcConfigProperty"]]]=None):
        """Properties for defining a ``AWS::CodeBuild::Project``.

        :param artifacts: ``AWS::CodeBuild::Project.Artifacts``.
        :param environment: ``AWS::CodeBuild::Project.Environment``.
        :param service_role: ``AWS::CodeBuild::Project.ServiceRole``.
        :param source: ``AWS::CodeBuild::Project.Source``.
        :param badge_enabled: ``AWS::CodeBuild::Project.BadgeEnabled``.
        :param cache: ``AWS::CodeBuild::Project.Cache``.
        :param description: ``AWS::CodeBuild::Project.Description``.
        :param encryption_key: ``AWS::CodeBuild::Project.EncryptionKey``.
        :param logs_config: ``AWS::CodeBuild::Project.LogsConfig``.
        :param name: ``AWS::CodeBuild::Project.Name``.
        :param queued_timeout_in_minutes: ``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.
        :param secondary_artifacts: ``AWS::CodeBuild::Project.SecondaryArtifacts``.
        :param secondary_sources: ``AWS::CodeBuild::Project.SecondarySources``.
        :param secondary_source_versions: ``AWS::CodeBuild::Project.SecondarySourceVersions``.
        :param source_version: ``AWS::CodeBuild::Project.SourceVersion``.
        :param tags: ``AWS::CodeBuild::Project.Tags``.
        :param timeout_in_minutes: ``AWS::CodeBuild::Project.TimeoutInMinutes``.
        :param triggers: ``AWS::CodeBuild::Project.Triggers``.
        :param vpc_config: ``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html
        """
        self._values = {
            'artifacts': artifacts,
            'environment': environment,
            'service_role': service_role,
            'source': source,
        }
        if badge_enabled is not None: self._values["badge_enabled"] = badge_enabled
        if cache is not None: self._values["cache"] = cache
        if description is not None: self._values["description"] = description
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if logs_config is not None: self._values["logs_config"] = logs_config
        if name is not None: self._values["name"] = name
        if queued_timeout_in_minutes is not None: self._values["queued_timeout_in_minutes"] = queued_timeout_in_minutes
        if secondary_artifacts is not None: self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None: self._values["secondary_sources"] = secondary_sources
        if secondary_source_versions is not None: self._values["secondary_source_versions"] = secondary_source_versions
        if source_version is not None: self._values["source_version"] = source_version
        if tags is not None: self._values["tags"] = tags
        if timeout_in_minutes is not None: self._values["timeout_in_minutes"] = timeout_in_minutes
        if triggers is not None: self._values["triggers"] = triggers
        if vpc_config is not None: self._values["vpc_config"] = vpc_config

    @property
    def artifacts(self) -> typing.Union["CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Artifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-artifacts
        """
        return self._values.get('artifacts')

    @property
    def environment(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnProject.EnvironmentProperty"]:
        """``AWS::CodeBuild::Project.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-environment
        """
        return self._values.get('environment')

    @property
    def service_role(self) -> str:
        """``AWS::CodeBuild::Project.ServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-servicerole
        """
        return self._values.get('service_role')

    @property
    def source(self) -> typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable]:
        """``AWS::CodeBuild::Project.Source``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-source
        """
        return self._values.get('source')

    @property
    def badge_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeBuild::Project.BadgeEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-badgeenabled
        """
        return self._values.get('badge_enabled')

    @property
    def cache(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.ProjectCacheProperty"]]]:
        """``AWS::CodeBuild::Project.Cache``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-cache
        """
        return self._values.get('cache')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-description
        """
        return self._values.get('description')

    @property
    def encryption_key(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.EncryptionKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-encryptionkey
        """
        return self._values.get('encryption_key')

    @property
    def logs_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.LogsConfigProperty"]]]:
        """``AWS::CodeBuild::Project.LogsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-logsconfig
        """
        return self._values.get('logs_config')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-name
        """
        return self._values.get('name')

    @property
    def queued_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.QueuedTimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-queuedtimeoutinminutes
        """
        return self._values.get('queued_timeout_in_minutes')

    @property
    def secondary_artifacts(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnProject.ArtifactsProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::CodeBuild::Project.SecondaryArtifacts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondaryartifacts
        """
        return self._values.get('secondary_artifacts')

    @property
    def secondary_sources(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["CfnProject.SourceProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::CodeBuild::Project.SecondarySources``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysources
        """
        return self._values.get('secondary_sources')

    @property
    def secondary_source_versions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnProject.ProjectSourceVersionProperty"]]]]]:
        """``AWS::CodeBuild::Project.SecondarySourceVersions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-secondarysourceversions
        """
        return self._values.get('secondary_source_versions')

    @property
    def source_version(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::Project.SourceVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-sourceversion
        """
        return self._values.get('source_version')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodeBuild::Project.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-tags
        """
        return self._values.get('tags')

    @property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::CodeBuild::Project.TimeoutInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-timeoutinminutes
        """
        return self._values.get('timeout_in_minutes')

    @property
    def triggers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.ProjectTriggersProperty"]]]:
        """``AWS::CodeBuild::Project.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-triggers
        """
        return self._values.get('triggers')

    @property
    def vpc_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnProject.VpcConfigProperty"]]]:
        """``AWS::CodeBuild::Project.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html#cfn-codebuild-project-vpcconfig
        """
        return self._values.get('vpc_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnProjectProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSourceCredential(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.CfnSourceCredential"):
    """A CloudFormation ``AWS::CodeBuild::SourceCredential``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeBuild::SourceCredential
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auth_type: str, server_type: str, token: str, username: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CodeBuild::SourceCredential``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param auth_type: ``AWS::CodeBuild::SourceCredential.AuthType``.
        :param server_type: ``AWS::CodeBuild::SourceCredential.ServerType``.
        :param token: ``AWS::CodeBuild::SourceCredential.Token``.
        :param username: ``AWS::CodeBuild::SourceCredential.Username``.
        """
        props = CfnSourceCredentialProps(auth_type=auth_type, server_type=server_type, token=token, username=username)

        jsii.create(CfnSourceCredential, self, [scope, id, props])

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
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-authtype
        """
        return jsii.get(self, "authType")

    @auth_type.setter
    def auth_type(self, value: str):
        return jsii.set(self, "authType", value)

    @property
    @jsii.member(jsii_name="serverType")
    def server_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.ServerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-servertype
        """
        return jsii.get(self, "serverType")

    @server_type.setter
    def server_type(self, value: str):
        return jsii.set(self, "serverType", value)

    @property
    @jsii.member(jsii_name="token")
    def token(self) -> str:
        """``AWS::CodeBuild::SourceCredential.Token``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-token
        """
        return jsii.get(self, "token")

    @token.setter
    def token(self, value: str):
        return jsii.set(self, "token", value)

    @property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-username
        """
        return jsii.get(self, "username")

    @username.setter
    def username(self, value: typing.Optional[str]):
        return jsii.set(self, "username", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CfnSourceCredentialProps", jsii_struct_bases=[], name_mapping={'auth_type': 'authType', 'server_type': 'serverType', 'token': 'token', 'username': 'username'})
class CfnSourceCredentialProps():
    def __init__(self, *, auth_type: str, server_type: str, token: str, username: typing.Optional[str]=None):
        """Properties for defining a ``AWS::CodeBuild::SourceCredential``.

        :param auth_type: ``AWS::CodeBuild::SourceCredential.AuthType``.
        :param server_type: ``AWS::CodeBuild::SourceCredential.ServerType``.
        :param token: ``AWS::CodeBuild::SourceCredential.Token``.
        :param username: ``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html
        """
        self._values = {
            'auth_type': auth_type,
            'server_type': server_type,
            'token': token,
        }
        if username is not None: self._values["username"] = username

    @property
    def auth_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.AuthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-authtype
        """
        return self._values.get('auth_type')

    @property
    def server_type(self) -> str:
        """``AWS::CodeBuild::SourceCredential.ServerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-servertype
        """
        return self._values.get('server_type')

    @property
    def token(self) -> str:
        """``AWS::CodeBuild::SourceCredential.Token``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-token
        """
        return self._values.get('token')

    @property
    def username(self) -> typing.Optional[str]:
        """``AWS::CodeBuild::SourceCredential.Username``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-sourcecredential.html#cfn-codebuild-sourcecredential-username
        """
        return self._values.get('username')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSourceCredentialProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CommonProjectProps", jsii_struct_bases=[], name_mapping={'allow_all_outbound': 'allowAllOutbound', 'badge': 'badge', 'build_spec': 'buildSpec', 'cache': 'cache', 'description': 'description', 'encryption_key': 'encryptionKey', 'environment': 'environment', 'environment_variables': 'environmentVariables', 'project_name': 'projectName', 'role': 'role', 'security_groups': 'securityGroups', 'subnet_selection': 'subnetSelection', 'timeout': 'timeout', 'vpc': 'vpc'})
class CommonProjectProps():
    def __init__(self, *, allow_all_outbound: typing.Optional[bool]=None, badge: typing.Optional[bool]=None, build_spec: typing.Optional["BuildSpec"]=None, cache: typing.Optional["Cache"]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, environment: typing.Optional["BuildEnvironment"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, project_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        if isinstance(environment, dict): environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict): subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {
        }
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None: self._values["badge"] = badge
        if build_spec is not None: self._values["build_spec"] = build_spec
        if cache is not None: self._values["cache"] = cache
        if description is not None: self._values["description"] = description
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if environment is not None: self._values["environment"] = environment
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if project_name is not None: self._values["project_name"] = project_name
        if role is not None: self._values["role"] = role
        if security_groups is not None: self._values["security_groups"] = security_groups
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if timeout is not None: self._values["timeout"] = timeout
        if vpc is not None: self._values["vpc"] = vpc

    @property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @property
    def badge(self) -> typing.Optional[bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false
        """
        return self._values.get('badge')

    @property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        """
        return self._values.get('build_spec')

    @property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none
        """
        return self._values.get('cache')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        """
        return self._values.get('encryption_key')

    @property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get('environment')

    @property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.
        """
        return self._values.get('environment_variables')

    @property
    def project_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.
        """
        return self._values.get('project_name')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.
        """
        return self._values.get('role')

    @property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.
        """
        return self._values.get('security_groups')

    @property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.
        """
        return self._values.get('subnet_selection')

    @property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)
        """
        return self._values.get('timeout')

    @property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonProjectProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.ComputeType")
class ComputeType(enum.Enum):
    """Build machine compute type."""
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.DockerImageOptions", jsii_struct_bases=[], name_mapping={'secrets_manager_credentials': 'secretsManagerCredentials'})
class DockerImageOptions():
    def __init__(self, *, secrets_manager_credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None):
        """The options when creating a CodeBuild Docker build image using {@link LinuxBuildImage.fromDockerRegistry} or {@link WindowsBuildImage.fromDockerRegistry}.

        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)
        """
        self._values = {
        }
        if secrets_manager_credentials is not None: self._values["secrets_manager_credentials"] = secrets_manager_credentials

    @property
    def secrets_manager_credentials(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private.

        default
        :default: no credentials will be used (we assume the repository is public)
        """
        return self._values.get('secrets_manager_credentials')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.EventAction")
class EventAction(enum.Enum):
    """The types of webhook event actions."""
    PUSH = "PUSH"
    """A push (of a branch, or a tag) to the repository."""
    PULL_REQUEST_CREATED = "PULL_REQUEST_CREATED"
    """Creating a Pull Request."""
    PULL_REQUEST_UPDATED = "PULL_REQUEST_UPDATED"
    """Updating a Pull Request."""
    PULL_REQUEST_MERGED = "PULL_REQUEST_MERGED"
    """Merging a Pull Request."""
    PULL_REQUEST_REOPENED = "PULL_REQUEST_REOPENED"
    """Re-opening a previously closed Pull Request. Note that this event is only supported for GitHub and GitHubEnterprise sources."""

class FilterGroup(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.FilterGroup"):
    """An object that represents a group of filter conditions for a webhook. Every condition in a given FilterGroup must be true in order for the whole group to be true. You construct instances of it by calling the {@link #inEventOf} static factory method, and then calling various ``andXyz`` instance methods to create modified instances of it (this class is immutable).

    You pass instances of this class to the ``webhookFilters`` property when constructing a source.
    """
    @jsii.member(jsii_name="inEventOf")
    @classmethod
    def in_event_of(cls, *actions: "EventAction") -> "FilterGroup":
        """Creates a new event FilterGroup that triggers on any of the provided actions.

        :param actions: the actions to trigger the webhook on.
        """
        return jsii.sinvoke(cls, "inEventOf", [*actions])

    @jsii.member(jsii_name="andActorAccountIs")
    def and_actor_account_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the account ID of the actor initiating the event must match the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andActorAccountIs", [pattern])

    @jsii.member(jsii_name="andActorAccountIsNot")
    def and_actor_account_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the account ID of the actor initiating the event must not match the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andActorAccountIsNot", [pattern])

    @jsii.member(jsii_name="andBaseBranchIs")
    def and_base_branch_is(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must target the given base branch. Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBaseBranchIs", [branch_name])

    @jsii.member(jsii_name="andBaseBranchIsNot")
    def and_base_branch_is_not(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must not target the given base branch. Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBaseBranchIsNot", [branch_name])

    @jsii.member(jsii_name="andBaseRefIs")
    def and_base_ref_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must target the given Git reference. Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andBaseRefIs", [pattern])

    @jsii.member(jsii_name="andBaseRefIsNot")
    def and_base_ref_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the Pull Request that is the source of the event must not target the given Git reference. Note that you cannot use this method if this Group contains the ``PUSH`` event action.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andBaseRefIsNot", [pattern])

    @jsii.member(jsii_name="andBranchIs")
    def and_branch_is(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect the given branch.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBranchIs", [branch_name])

    @jsii.member(jsii_name="andBranchIsNot")
    def and_branch_is_not(self, branch_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect the given branch.

        :param branch_name: the name of the branch (can be a regular expression).
        """
        return jsii.invoke(self, "andBranchIsNot", [branch_name])

    @jsii.member(jsii_name="andFilePathIs")
    def and_file_path_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the push that is the source of the event must affect a file that matches the given pattern. Note that you can only use this method if this Group contains only the ``PUSH`` event action, and only for GitHub and GitHubEnterprise sources.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andFilePathIs", [pattern])

    @jsii.member(jsii_name="andFilePathIsNot")
    def and_file_path_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the push that is the source of the event must not affect a file that matches the given pattern. Note that you can only use this method if this Group contains only the ``PUSH`` event action, and only for GitHub and GitHubEnterprise sources.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andFilePathIsNot", [pattern])

    @jsii.member(jsii_name="andHeadRefIs")
    def and_head_ref_is(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect a Git reference (ie., a branch or a tag) that matches the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andHeadRefIs", [pattern])

    @jsii.member(jsii_name="andHeadRefIsNot")
    def and_head_ref_is_not(self, pattern: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect a Git reference (ie., a branch or a tag) that matches the given pattern.

        :param pattern: a regular expression.
        """
        return jsii.invoke(self, "andHeadRefIsNot", [pattern])

    @jsii.member(jsii_name="andTagIs")
    def and_tag_is(self, tag_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must affect the given tag.

        :param tag_name: the name of the tag (can be a regular expression).
        """
        return jsii.invoke(self, "andTagIs", [tag_name])

    @jsii.member(jsii_name="andTagIsNot")
    def and_tag_is_not(self, tag_name: str) -> "FilterGroup":
        """Create a new FilterGroup with an added condition: the event must not affect the given tag.

        :param tag_name: the name of the tag (can be a regular expression).
        """
        return jsii.invoke(self, "andTagIsNot", [tag_name])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IArtifacts")
class IArtifacts(jsii.compat.Protocol):
    """The abstract interface of a CodeBuild build output. Implemented by {@link Artifacts}."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IArtifactsProxy

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        ...

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier. This property is required on secondary artifacts."""
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, project: "IProject") -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param scope: a root Construct that allows creating new Constructs.
        :param project: the Project this Artifacts is used in.
        """
        ...


class _IArtifactsProxy():
    """The abstract interface of a CodeBuild build output. Implemented by {@link Artifacts}."""
    __jsii_type__ = "@aws-cdk/aws-codebuild.IArtifacts"
    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        return jsii.get(self, "type")

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier. This property is required on secondary artifacts."""
        return jsii.get(self, "identifier")

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, project: "IProject") -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param scope: a root Construct that allows creating new Constructs.
        :param project: the Project this Artifacts is used in.
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.implements(IArtifacts)
class Artifacts(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.Artifacts"):
    """Artifacts definition for a CodeBuild Project."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ArtifactsProxy

    def __init__(self, *, identifier: typing.Optional[str]=None) -> None:
        """
        :param props: -
        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        """
        props = ArtifactsProps(identifier=identifier)

        jsii.create(Artifacts, self, [props])

    @jsii.member(jsii_name="s3")
    @classmethod
    def s3(cls, *, bucket: aws_cdk.aws_s3.IBucket, name: str, encryption: typing.Optional[bool]=None, include_build_id: typing.Optional[bool]=None, package_zip: typing.Optional[bool]=None, path: typing.Optional[str]=None, identifier: typing.Optional[str]=None) -> "IArtifacts":
        """
        :param props: -
        :param bucket: The name of the output bucket.
        :param name: The name of the build output ZIP file or folder inside the bucket. The full S3 object key will be "//" or "/" depending on whether ``includeBuildId`` is set to true.
        :param encryption: If this is false, build output will not be encrypted. This is useful if the artifact to publish a static website or sharing content with others. Default: true - output will be encrypted
        :param include_build_id: Indicates if the build ID should be included in the path. If this is set to true, then the build artifact will be stored in "//". Default: true
        :param package_zip: If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /. Default: true - files will be archived
        :param path: The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the directory if ``includeBuildId`` is set to true).
        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        """
        props = S3ArtifactsProps(bucket=bucket, name=name, encryption=encryption, include_build_id=include_build_id, package_zip=package_zip, path=path, identifier=identifier)

        return jsii.sinvoke(cls, "s3", [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _project: "IProject") -> "ArtifactsConfig":
        """Callback when an Artifacts class is used in a CodeBuild Project.

        :param _scope: -
        :param _project: -
        """
        return jsii.invoke(self, "bind", [_scope, _project])

    @property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        ...

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier. This property is required on secondary artifacts."""
        return jsii.get(self, "identifier")


class _ArtifactsProxy(Artifacts):
    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The CodeBuild type of this artifact."""
        return jsii.get(self, "type")


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IBuildImage")
class IBuildImage(jsii.compat.Protocol):
    """Represents a Docker image used for the CodeBuild Project builds. Use the concrete subclasses, either: {@link LinuxBuildImage} or {@link WindowsBuildImage}."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IBuildImageProxy

    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        ...

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
        """
        ...

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        ...

    @property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        default
        :default: ImagePullPrincipalType.SERVICE_ROLE
        """
        ...

    @property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in.

        default
        :default: no repository
        """
        ...

    @property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry.

        default
        :default: no credentials will be used
        """
        ...

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        ...

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_environment: the current build environment.
        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        ...


class _IBuildImageProxy():
    """Represents a Docker image used for the CodeBuild Project builds. Use the concrete subclasses, either: {@link LinuxBuildImage} or {@link WindowsBuildImage}."""
    __jsii_type__ = "@aws-cdk/aws-codebuild.IBuildImage"
    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        return jsii.get(self, "defaultComputeType")

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
        """
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        return jsii.get(self, "type")

    @property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image.

        default
        :default: ImagePullPrincipalType.SERVICE_ROLE
        """
        return jsii.get(self, "imagePullPrincipalType")

    @property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in.

        default
        :default: no repository
        """
        return jsii.get(self, "repository")

    @property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry.

        default
        :default: no credentials will be used
        """
        return jsii.get(self, "secretsManagerCredentials")

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_environment: the current build environment.
        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        build_environment = BuildEnvironment(build_image=build_image, compute_type=compute_type, environment_variables=environment_variables, privileged=privileged)

        return jsii.invoke(self, "validate", [build_environment])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.IProject")
class IProject(aws_cdk.core.IResource, aws_cdk.aws_iam.IGrantable, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IProjectProxy

    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        """The ARN of this Project.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        """The human-visible name of this Project.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM service Role of this Project.

        Undefined for imported Projects.
        """
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, policy_statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """
        :param policy_statement: -
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """
        :param metric_name: The name of the metric.
        :param props: Customization properties.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        return
        :return: a CloudWatch metric associated with this build project.
        """
        ...

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        ...

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

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
        ...

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        ...

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        ...

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build fails.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build starts.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build completes successfully.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        ...

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        ...


class _IProjectProxy(jsii.proxy_for(aws_cdk.core.IResource), jsii.proxy_for(aws_cdk.aws_iam.IGrantable), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    __jsii_type__ = "@aws-cdk/aws-codebuild.IProject"
    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        """The ARN of this Project.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "projectArn")

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        """The human-visible name of this Project.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "projectName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM service Role of this Project.

        Undefined for imported Projects.
        """
        return jsii.get(self, "role")

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, policy_statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """
        :param policy_statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [policy_statement])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """
        :param metric_name: The name of the metric.
        :param props: Customization properties.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        return
        :return: a CloudWatch metric associated with this build project.
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

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

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build fails.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onBuildFailed", [id, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build starts.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onBuildStarted", [id, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build completes successfully.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onBuildSucceeded", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onPhaseChange", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onStateChange", [id, options])


@jsii.interface(jsii_type="@aws-cdk/aws-codebuild.ISource")
class ISource(jsii.compat.Protocol):
    """The abstract interface of a CodeBuild source. Implemented by {@link Source}."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @property
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> bool:
        ...

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, project: "IProject") -> "SourceConfig":
        """
        :param scope: -
        :param project: -
        """
        ...


class _ISourceProxy():
    """The abstract interface of a CodeBuild source. Implemented by {@link Source}."""
    __jsii_type__ = "@aws-cdk/aws-codebuild.ISource"
    @property
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> bool:
        return jsii.get(self, "badgeSupported")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        return jsii.get(self, "identifier")

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, project: "IProject") -> "SourceConfig":
        """
        :param scope: -
        :param project: -
        """
        return jsii.invoke(self, "bind", [scope, project])


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.ImagePullPrincipalType")
class ImagePullPrincipalType(enum.Enum):
    """The type of principal CodeBuild will use to pull your build Docker image."""
    CODEBUILD = "CODEBUILD"
    """CODEBUILD specifies that CodeBuild uses its own identity when pulling the image. This means the resource policy of the ECR repository that hosts the image will be modified to trust CodeBuild's service principal. This is the required principal type when using CodeBuild's pre-defined images."""
    SERVICE_ROLE = "SERVICE_ROLE"
    """SERVICE_ROLE specifies that AWS CodeBuild uses the project's role when pulling the image. The role will be granted pull permissions on the ECR repository hosting the image."""

@jsii.implements(IBuildImage)
class LinuxBuildImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.LinuxBuildImage"):
    """A CodeBuild image running Linux.

    This class has a bunch of public constants that represent the most popular images.

    You can also specify a custom image using one of the static methods:

    - LinuxBuildImage.fromDockerRegistry(image[, { secretsManagerCredentials }])
    - LinuxBuildImage.fromEcrRepository(repo[, tag])
    - LinuxBuildImage.fromAsset(parent, id, props)

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
    """
    @jsii.member(jsii_name="fromAsset")
    @classmethod
    def from_asset(cls, scope: aws_cdk.core.Construct, id: str, *, directory: str, build_args: typing.Optional[typing.Mapping[str,str]]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None) -> "IBuildImage":
        """Uses an Docker image asset as a Linux build image.

        :param scope: -
        :param id: -
        :param props: -
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.
        :param target: Docker target to build to. Default: - no target
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        """
        props = aws_cdk.aws_ecr_assets.DockerImageAssetProps(directory=directory, build_args=build_args, repository_name=repository_name, target=target, exclude=exclude, follow=follow)

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromDockerRegistry")
    @classmethod
    def from_docker_registry(cls, name: str, *, secrets_manager_credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> "IBuildImage":
        """
        :param name: -
        :param options: -
        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)

        return
        :return: a Linux build image from a Docker Hub image.
        """
        options = DockerImageOptions(secrets_manager_credentials=secrets_manager_credentials)

        return jsii.sinvoke(cls, "fromDockerRegistry", [name, options])

    @jsii.member(jsii_name="fromEcrRepository")
    @classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "IBuildImage":
        """
        :param repository: The ECR repository.
        :param tag: Image tag (default "latest").

        return
        :return:

        A Linux build image from an ECR repository.

        NOTE: if the repository is external (i.e. imported), then we won't be able to add
        a resource policy statement for it so CodeBuild can pull the image.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-ecr.html
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param _: -
        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        _ = BuildEnvironment(build_image=build_image, compute_type=compute_type, environment_variables=environment_variables, privileged=privileged)

        return jsii.invoke(self, "validate", [_])

    @classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2")
    def AMAZON_LINUX_2(cls) -> "IBuildImage":
        return jsii.sget(cls, "AMAZON_LINUX_2")

    @classproperty
    @jsii.member(jsii_name="STANDARD_1_0")
    def STANDARD_1_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "STANDARD_1_0")

    @classproperty
    @jsii.member(jsii_name="STANDARD_2_0")
    def STANDARD_2_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "STANDARD_2_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_24_4_1")
    def UBUNTU_14_04_ANDROID_JAV_A8_24_4_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_24_4_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_ANDROID_JAVA8_26_1_1")
    def UBUNTU_14_04_ANDROID_JAV_A8_26_1_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_ANDROID_JAVA8_26_1_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_BASE")
    def UBUNTU_14_04_BASE(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_BASE")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOCKER_17_09_0")
    def UBUNTU_14_04_DOCKER_17_09_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOCKER_17_09_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOCKER_18_09_0")
    def UBUNTU_14_04_DOCKER_18_09_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOCKER_18_09_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_1_1")
    def UBUNTU_14_04_DOTNET_CORE_1_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_1_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_0")
    def UBUNTU_14_04_DOTNET_CORE_2_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_DOTNET_CORE_2_1")
    def UBUNTU_14_04_DOTNET_CORE_2_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_DOTNET_CORE_2_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_GOLANG_1_10")
    def UBUNTU_14_04_GOLANG_1_10(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_GOLANG_1_10")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_GOLANG_1_11")
    def UBUNTU_14_04_GOLANG_1_11(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_GOLANG_1_11")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_10_1_0")
    def UBUNTU_14_04_NODEJS_10_1_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_10_1_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_10_14_1")
    def UBUNTU_14_04_NODEJS_10_14_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_10_14_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_6_3_1")
    def UBUNTU_14_04_NODEJS_6_3_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_6_3_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_NODEJS_8_11_0")
    def UBUNTU_14_04_NODEJS_8_11_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_NODEJS_8_11_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_11")
    def UBUNTU_14_04_OPEN_JDK_11(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_11")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_8")
    def UBUNTU_14_04_OPEN_JDK_8(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_8")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_OPEN_JDK_9")
    def UBUNTU_14_04_OPEN_JDK_9(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_OPEN_JDK_9")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_5_6")
    def UBUNTU_14_04_PHP_5_6(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PHP_5_6")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_7_0")
    def UBUNTU_14_04_PHP_7_0(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PHP_7_0")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PHP_7_1")
    def UBUNTU_14_04_PHP_7_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PHP_7_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_2_7_12")
    def UBUNTU_14_04_PYTHON_2_7_12(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_2_7_12")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_3_6")
    def UBUNTU_14_04_PYTHON_3_3_6(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_3_6")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_4_5")
    def UBUNTU_14_04_PYTHON_3_4_5(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_4_5")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_5_2")
    def UBUNTU_14_04_PYTHON_3_5_2(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_5_2")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_6_5")
    def UBUNTU_14_04_PYTHON_3_6_5(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_6_5")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_PYTHON_3_7_1")
    def UBUNTU_14_04_PYTHON_3_7_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_PYTHON_3_7_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_2_5")
    def UBUNTU_14_04_RUBY_2_2_5(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_2_5")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_3_1")
    def UBUNTU_14_04_RUBY_2_3_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_3_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_5_1")
    def UBUNTU_14_04_RUBY_2_5_1(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_5_1")

    @classproperty
    @jsii.member(jsii_name="UBUNTU_14_04_RUBY_2_5_3")
    def UBUNTU_14_04_RUBY_2_5_3(cls) -> "IBuildImage":
        return jsii.sget(cls, "UBUNTU_14_04_RUBY_2_5_3")

    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        return jsii.get(self, "defaultComputeType")

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses."""
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        return jsii.get(self, "type")

    @property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image."""
        return jsii.get(self, "imagePullPrincipalType")

    @property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in."""
        return jsii.get(self, "repository")

    @property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry."""
        return jsii.get(self, "secretsManagerCredentials")


@jsii.enum(jsii_type="@aws-cdk/aws-codebuild.LocalCacheMode")
class LocalCacheMode(enum.Enum):
    """Local cache modes to enable for the CodeBuild Project."""
    SOURCE = "SOURCE"
    """Caches Git metadata for primary and secondary sources."""
    DOCKER_LAYER = "DOCKER_LAYER"
    """Caches existing Docker layers."""
    CUSTOM = "CUSTOM"
    """Caches directories you specify in the buildspec file."""

class PhaseChangeEvent(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.PhaseChangeEvent"):
    """Event fields for the CodeBuild "phase change" event.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html#sample-build-notifications-ref
    """
    @classproperty
    @jsii.member(jsii_name="buildComplete")
    def build_complete(cls) -> str:
        """Whether the build is complete."""
        return jsii.sget(cls, "buildComplete")

    @classproperty
    @jsii.member(jsii_name="buildId")
    def build_id(cls) -> str:
        """The triggering build's id."""
        return jsii.sget(cls, "buildId")

    @classproperty
    @jsii.member(jsii_name="completedPhase")
    def completed_phase(cls) -> str:
        """The phase that was just completed."""
        return jsii.sget(cls, "completedPhase")

    @classproperty
    @jsii.member(jsii_name="completedPhaseDurationSeconds")
    def completed_phase_duration_seconds(cls) -> str:
        """The duration of the completed phase."""
        return jsii.sget(cls, "completedPhaseDurationSeconds")

    @classproperty
    @jsii.member(jsii_name="completedPhaseStatus")
    def completed_phase_status(cls) -> str:
        """The status of the completed phase."""
        return jsii.sget(cls, "completedPhaseStatus")

    @classproperty
    @jsii.member(jsii_name="projectName")
    def project_name(cls) -> str:
        """The triggering build's project name."""
        return jsii.sget(cls, "projectName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.PipelineProjectProps", jsii_struct_bases=[CommonProjectProps], name_mapping={'allow_all_outbound': 'allowAllOutbound', 'badge': 'badge', 'build_spec': 'buildSpec', 'cache': 'cache', 'description': 'description', 'encryption_key': 'encryptionKey', 'environment': 'environment', 'environment_variables': 'environmentVariables', 'project_name': 'projectName', 'role': 'role', 'security_groups': 'securityGroups', 'subnet_selection': 'subnetSelection', 'timeout': 'timeout', 'vpc': 'vpc'})
class PipelineProjectProps(CommonProjectProps):
    def __init__(self, *, allow_all_outbound: typing.Optional[bool]=None, badge: typing.Optional[bool]=None, build_spec: typing.Optional["BuildSpec"]=None, cache: typing.Optional["Cache"]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, environment: typing.Optional["BuildEnvironment"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, project_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        if isinstance(environment, dict): environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict): subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {
        }
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None: self._values["badge"] = badge
        if build_spec is not None: self._values["build_spec"] = build_spec
        if cache is not None: self._values["cache"] = cache
        if description is not None: self._values["description"] = description
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if environment is not None: self._values["environment"] = environment
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if project_name is not None: self._values["project_name"] = project_name
        if role is not None: self._values["role"] = role
        if security_groups is not None: self._values["security_groups"] = security_groups
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if timeout is not None: self._values["timeout"] = timeout
        if vpc is not None: self._values["vpc"] = vpc

    @property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @property
    def badge(self) -> typing.Optional[bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false
        """
        return self._values.get('badge')

    @property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        """
        return self._values.get('build_spec')

    @property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none
        """
        return self._values.get('cache')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        """
        return self._values.get('encryption_key')

    @property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get('environment')

    @property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.
        """
        return self._values.get('environment_variables')

    @property
    def project_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.
        """
        return self._values.get('project_name')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.
        """
        return self._values.get('role')

    @property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.
        """
        return self._values.get('security_groups')

    @property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.
        """
        return self._values.get('subnet_selection')

    @property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)
        """
        return self._values.get('timeout')

    @property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PipelineProjectProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IProject)
class Project(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.Project"):
    """A representation of a CodeBuild Project."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, artifacts: typing.Optional["IArtifacts"]=None, secondary_artifacts: typing.Optional[typing.List["IArtifacts"]]=None, secondary_sources: typing.Optional[typing.List["ISource"]]=None, source: typing.Optional["ISource"]=None, allow_all_outbound: typing.Optional[bool]=None, badge: typing.Optional[bool]=None, build_spec: typing.Optional["BuildSpec"]=None, cache: typing.Optional["Cache"]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, environment: typing.Optional["BuildEnvironment"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, project_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        props = ProjectProps(artifacts=artifacts, secondary_artifacts=secondary_artifacts, secondary_sources=secondary_sources, source=source, allow_all_outbound=allow_all_outbound, badge=badge, build_spec=build_spec, cache=cache, description=description, encryption_key=encryption_key, environment=environment, environment_variables=environment_variables, project_name=project_name, role=role, security_groups=security_groups, subnet_selection=subnet_selection, timeout=timeout, vpc=vpc)

        jsii.create(Project, self, [scope, id, props])

    @jsii.member(jsii_name="fromProjectArn")
    @classmethod
    def from_project_arn(cls, scope: aws_cdk.core.Construct, id: str, project_arn: str) -> "IProject":
        """
        :param scope: -
        :param id: -
        :param project_arn: -
        """
        return jsii.sinvoke(cls, "fromProjectArn", [scope, id, project_arn])

    @jsii.member(jsii_name="fromProjectName")
    @classmethod
    def from_project_name(cls, scope: aws_cdk.core.Construct, id: str, project_name: str) -> "IProject":
        """Import a Project defined either outside the CDK, or in a different CDK Stack (and exported using the {@link export} method).

        :param scope: the parent Construct for this Construct.
        :param id: the logical name of this Construct.
        :param project_name: the name of the project to import.

        return
        :return: a reference to the existing Project

        note:
        :note::

        if you're importing a CodeBuild Project for use
        in a CodePipeline, make sure the existing Project
        has permissions to access the S3 Bucket of that Pipeline -
        otherwise, builds in that Pipeline will always fail.
        """
        return jsii.sinvoke(cls, "fromProjectName", [scope, id, project_name])

    @jsii.member(jsii_name="serializeEnvVariables")
    @classmethod
    def serialize_env_variables(cls, environment_variables: typing.Mapping[str,"BuildEnvironmentVariable"]) -> typing.List["CfnProject.EnvironmentVariableProperty"]:
        """Convert the environment variables map of string to {@link BuildEnvironmentVariable}, which is the customer-facing type, to a list of {@link CfnProject.EnvironmentVariableProperty}, which is the representation of environment variables in CloudFormation.

        :param environment_variables: the map of string to environment variables.

        return
        :return: an array of {@link CfnProject.EnvironmentVariableProperty} instances
        """
        return jsii.sinvoke(cls, "serializeEnvVariables", [environment_variables])

    @jsii.member(jsii_name="addSecondaryArtifact")
    def add_secondary_artifact(self, secondary_artifact: "IArtifacts") -> None:
        """Adds a secondary artifact to the Project.

        :param secondary_artifact: the artifact to add as a secondary artifact.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return jsii.invoke(self, "addSecondaryArtifact", [secondary_artifact])

    @jsii.member(jsii_name="addSecondarySource")
    def add_secondary_source(self, secondary_source: "ISource") -> None:
        """Adds a secondary source to the Project.

        :param secondary_source: the source to add as a secondary source.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return jsii.invoke(self, "addSecondarySource", [secondary_source])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a permission only if there's a policy attached.

        :param statement: The permissions statement to add.
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="bindToCodePipeline")
    def bind_to_code_pipeline(self, _scope: aws_cdk.core.Construct, *, artifact_bucket: aws_cdk.aws_s3.IBucket) -> None:
        """A callback invoked when the given project is added to a CodePipeline.

        :param _scope: the construct the binding is taking place in.
        :param options: additional options for the binding.
        :param artifact_bucket: The artifact bucket that will be used by the action that invokes this project.
        """
        options = BindToCodePipelineOptions(artifact_bucket=artifact_bucket)

        return jsii.invoke(self, "bindToCodePipeline", [_scope, options])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """
        :param metric_name: The name of the metric.
        :param props: Customization properties.
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        return
        :return: a CloudWatch metric associated with this build project.
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricBuilds")
    def metric_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds triggered.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricBuilds", [props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the duration of all builds over time.

        Units: Seconds

        Valid CloudWatch statistics: Average (recommended), Maximum, Minimum

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

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricFailedBuilds")
    def metric_failed_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of builds that failed because of client error or because of a timeout.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricFailedBuilds", [props])

    @jsii.member(jsii_name="metricSucceededBuilds")
    def metric_succeeded_builds(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Measures the number of successful builds.

        Units: Count

        Valid CloudWatch statistics: Sum

        :param props: -
        :param color: Color for this metric when added to a Graph in a Dashboard.
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard.
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit for the metric that is associated with the alarm.

        default
        :default: sum over 5 minutes
        """
        props = aws_cdk.aws_cloudwatch.MetricOptions(color=color, dimensions=dimensions, label=label, period=period, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricSucceededBuilds", [props])

    @jsii.member(jsii_name="onBuildFailed")
    def on_build_failed(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build fails.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onBuildFailed", [id, options])

    @jsii.member(jsii_name="onBuildStarted")
    def on_build_started(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build starts.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onBuildStarted", [id, options])

    @jsii.member(jsii_name="onBuildSucceeded")
    def on_build_succeeded(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines an event rule which triggers when a build completes successfully.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onBuildSucceeded", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when something happens with this project.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPhaseChange")
    def on_phase_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule that triggers upon phase change of this build project.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onPhaseChange", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None) -> aws_cdk.aws_events.Rule:
        """Defines a CloudWatch event rule triggered when the build project state changes.

        You can filter specific build status events using an event
        pattern filter on the ``build-status`` detail field::

           const rule = project.onStateChange('OnBuildStarted', { target });
           rule.addEventPattern({
             detail: {
               'build-status': [
                 "IN_PROGRESS",
                 "SUCCEEDED",
                 "FAILED",
                 "STOPPED"
               ]
             }
           });

        You can also use the methods ``onBuildFailed`` and ``onBuildSucceeded`` to define rules for
        these specific state changes.

        To access fields from the event in the event target input,
        use the static fields on the ``StateChangeEvent`` class.

        :param id: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html
        """
        options = aws_cdk.aws_events.OnEventOptions(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onStateChange", [id, options])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        override:
        :override:: true
        """
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Access the Connections object. Will fail if this Project does not have a VPC set."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @property
    @jsii.member(jsii_name="projectArn")
    def project_arn(self) -> str:
        """The ARN of the project."""
        return jsii.get(self, "projectArn")

    @property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> str:
        """The name of the project."""
        return jsii.get(self, "projectName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role for this project."""
        return jsii.get(self, "role")


class PipelineProject(Project, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.PipelineProject"):
    """A convenience class for CodeBuild Projects that are used in CodePipeline."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, allow_all_outbound: typing.Optional[bool]=None, badge: typing.Optional[bool]=None, build_spec: typing.Optional["BuildSpec"]=None, cache: typing.Optional["Cache"]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, environment: typing.Optional["BuildEnvironment"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, project_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        """
        props = PipelineProjectProps(allow_all_outbound=allow_all_outbound, badge=badge, build_spec=build_spec, cache=cache, description=description, encryption_key=encryption_key, environment=environment, environment_variables=environment_variables, project_name=project_name, role=role, security_groups=security_groups, subnet_selection=subnet_selection, timeout=timeout, vpc=vpc)

        jsii.create(PipelineProject, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.ProjectProps", jsii_struct_bases=[CommonProjectProps], name_mapping={'allow_all_outbound': 'allowAllOutbound', 'badge': 'badge', 'build_spec': 'buildSpec', 'cache': 'cache', 'description': 'description', 'encryption_key': 'encryptionKey', 'environment': 'environment', 'environment_variables': 'environmentVariables', 'project_name': 'projectName', 'role': 'role', 'security_groups': 'securityGroups', 'subnet_selection': 'subnetSelection', 'timeout': 'timeout', 'vpc': 'vpc', 'artifacts': 'artifacts', 'secondary_artifacts': 'secondaryArtifacts', 'secondary_sources': 'secondarySources', 'source': 'source'})
class ProjectProps(CommonProjectProps):
    def __init__(self, *, allow_all_outbound: typing.Optional[bool]=None, badge: typing.Optional[bool]=None, build_spec: typing.Optional["BuildSpec"]=None, cache: typing.Optional["Cache"]=None, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, environment: typing.Optional["BuildEnvironment"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, project_name: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, artifacts: typing.Optional["IArtifacts"]=None, secondary_artifacts: typing.Optional[typing.List["IArtifacts"]]=None, secondary_sources: typing.Optional[typing.List["ISource"]]=None, source: typing.Optional["ISource"]=None):
        """
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        """
        if isinstance(environment, dict): environment = BuildEnvironment(**environment)
        if isinstance(subnet_selection, dict): subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {
        }
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if badge is not None: self._values["badge"] = badge
        if build_spec is not None: self._values["build_spec"] = build_spec
        if cache is not None: self._values["cache"] = cache
        if description is not None: self._values["description"] = description
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if environment is not None: self._values["environment"] = environment
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if project_name is not None: self._values["project_name"] = project_name
        if role is not None: self._values["role"] = role
        if security_groups is not None: self._values["security_groups"] = security_groups
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if timeout is not None: self._values["timeout"] = timeout
        if vpc is not None: self._values["vpc"] = vpc
        if artifacts is not None: self._values["artifacts"] = artifacts
        if secondary_artifacts is not None: self._values["secondary_artifacts"] = secondary_artifacts
        if secondary_sources is not None: self._values["secondary_sources"] = secondary_sources
        if source is not None: self._values["source"] = source

    @property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the CodeBuild to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        CodeBuild project to connect to network targets.

        Only used if 'vpc' is supplied.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @property
    def badge(self) -> typing.Optional[bool]:
        """Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge.

        For more information, see Build Badges Sample
        in the AWS CodeBuild User Guide.

        default
        :default: false
        """
        return self._values.get('badge')

    @property
    def build_spec(self) -> typing.Optional["BuildSpec"]:
        """Filename or contents of buildspec in JSON format.

        default
        :default: - Empty buildspec.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-example
        """
        return self._values.get('build_spec')

    @property
    def cache(self) -> typing.Optional["Cache"]:
        """Caching strategy to use.

        default
        :default: Cache.none
        """
        return self._values.get('cache')

    @property
    def description(self) -> typing.Optional[str]:
        """A description of the project.

        Use the description to identify the purpose
        of the project.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """Encryption key to use to read and write artifacts.

        default
        :default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        """
        return self._values.get('encryption_key')

    @property
    def environment(self) -> typing.Optional["BuildEnvironment"]:
        """Build environment to use for the build.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        """
        return self._values.get('environment')

    @property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]:
        """Additional environment variables to add to the build environment.

        default
        :default: - No additional environment variables are specified.
        """
        return self._values.get('environment_variables')

    @property
    def project_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeBuild Project.

        default
        :default: - Name is automatically generated.
        """
        return self._values.get('project_name')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Service Role to assume while running the build.

        default
        :default: - A role will be created.
        """
        return self._values.get('role')

    @property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        default
        :default: - Security group will be automatically created.
        """
        return self._values.get('security_groups')

    @property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied.

        default
        :default: - All private subnets.
        """
        return self._values.get('subnet_selection')

    @property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        default
        :default: Duration.hours(1)
        """
        return self._values.get('timeout')

    @property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place codebuild network interfaces.

        Specify this if the codebuild project needs to access resources in a VPC.

        default
        :default: - No VPC is specified.
        """
        return self._values.get('vpc')

    @property
    def artifacts(self) -> typing.Optional["IArtifacts"]:
        """Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts.

        default
        :default: NoArtifacts
        """
        return self._values.get('artifacts')

    @property
    def secondary_artifacts(self) -> typing.Optional[typing.List["IArtifacts"]]:
        """The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method.

        default
        :default: - No secondary artifacts.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return self._values.get('secondary_artifacts')

    @property
    def secondary_sources(self) -> typing.Optional[typing.List["ISource"]]:
        """The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method.

        default
        :default: - No secondary sources.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        """
        return self._values.get('secondary_sources')

    @property
    def source(self) -> typing.Optional["ISource"]:
        """The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``.

        default
        :default: - NoSource
        """
        return self._values.get('source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ProjectProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.S3ArtifactsProps", jsii_struct_bases=[ArtifactsProps], name_mapping={'identifier': 'identifier', 'bucket': 'bucket', 'name': 'name', 'encryption': 'encryption', 'include_build_id': 'includeBuildId', 'package_zip': 'packageZip', 'path': 'path'})
class S3ArtifactsProps(ArtifactsProps):
    def __init__(self, *, identifier: typing.Optional[str]=None, bucket: aws_cdk.aws_s3.IBucket, name: str, encryption: typing.Optional[bool]=None, include_build_id: typing.Optional[bool]=None, package_zip: typing.Optional[bool]=None, path: typing.Optional[str]=None):
        """Construction properties for {@link S3Artifacts}.

        :param identifier: The artifact identifier. This property is required on secondary artifacts.
        :param bucket: The name of the output bucket.
        :param name: The name of the build output ZIP file or folder inside the bucket. The full S3 object key will be "//" or "/" depending on whether ``includeBuildId`` is set to true.
        :param encryption: If this is false, build output will not be encrypted. This is useful if the artifact to publish a static website or sharing content with others. Default: true - output will be encrypted
        :param include_build_id: Indicates if the build ID should be included in the path. If this is set to true, then the build artifact will be stored in "//". Default: true
        :param package_zip: If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /. Default: true - files will be archived
        :param path: The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the directory if ``includeBuildId`` is set to true).
        """
        self._values = {
            'bucket': bucket,
            'name': name,
        }
        if identifier is not None: self._values["identifier"] = identifier
        if encryption is not None: self._values["encryption"] = encryption
        if include_build_id is not None: self._values["include_build_id"] = include_build_id
        if package_zip is not None: self._values["package_zip"] = package_zip
        if path is not None: self._values["path"] = path

    @property
    def identifier(self) -> typing.Optional[str]:
        """The artifact identifier. This property is required on secondary artifacts."""
        return self._values.get('identifier')

    @property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The name of the output bucket."""
        return self._values.get('bucket')

    @property
    def name(self) -> str:
        """The name of the build output ZIP file or folder inside the bucket.

        The full S3 object key will be "//" or
        "/" depending on whether ``includeBuildId`` is set to true.
        """
        return self._values.get('name')

    @property
    def encryption(self) -> typing.Optional[bool]:
        """If this is false, build output will not be encrypted. This is useful if the artifact to publish a static website or sharing content with others.

        default
        :default: true - output will be encrypted
        """
        return self._values.get('encryption')

    @property
    def include_build_id(self) -> typing.Optional[bool]:
        """Indicates if the build ID should be included in the path.

        If this is set to true,
        then the build artifact will be stored in "//".

        default
        :default: true
        """
        return self._values.get('include_build_id')

    @property
    def package_zip(self) -> typing.Optional[bool]:
        """If this is true, all build output will be packaged into a single .zip file. Otherwise, all files will be uploaded to /.

        default
        :default: true - files will be archived
        """
        return self._values.get('package_zip')

    @property
    def path(self) -> typing.Optional[str]:
        """The path inside of the bucket for the build output .zip file or folder. If a value is not specified, then build output will be stored at the root of the bucket (or under the  directory if ``includeBuildId`` is set to true)."""
        return self._values.get('path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3ArtifactsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ISource)
class Source(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codebuild.Source"):
    """Source provider definition for a CodeBuild Project."""
    @staticmethod
    def __jsii_proxy_class__():
        return _SourceProxy

    def __init__(self, *, identifier: typing.Optional[str]=None) -> None:
        """
        :param props: -
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = SourceProps(identifier=identifier)

        jsii.create(Source, self, [props])

    @jsii.member(jsii_name="bitBucket")
    @classmethod
    def bit_bucket(cls, *, owner: str, repo: str, clone_depth: typing.Optional[jsii.Number]=None, report_build_status: typing.Optional[bool]=None, webhook: typing.Optional[bool]=None, webhook_filters: typing.Optional[typing.List["FilterGroup"]]=None, identifier: typing.Optional[str]=None) -> "ISource":
        """
        :param props: -
        :param owner: The BitBucket account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = BitBucketSourceProps(owner=owner, repo=repo, clone_depth=clone_depth, report_build_status=report_build_status, webhook=webhook, webhook_filters=webhook_filters, identifier=identifier)

        return jsii.sinvoke(cls, "bitBucket", [props])

    @jsii.member(jsii_name="codeCommit")
    @classmethod
    def code_commit(cls, *, repository: aws_cdk.aws_codecommit.IRepository, clone_depth: typing.Optional[jsii.Number]=None, identifier: typing.Optional[str]=None) -> "ISource":
        """
        :param props: -
        :param repository: 
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = CodeCommitSourceProps(repository=repository, clone_depth=clone_depth, identifier=identifier)

        return jsii.sinvoke(cls, "codeCommit", [props])

    @jsii.member(jsii_name="gitHub")
    @classmethod
    def git_hub(cls, *, owner: str, repo: str, clone_depth: typing.Optional[jsii.Number]=None, report_build_status: typing.Optional[bool]=None, webhook: typing.Optional[bool]=None, webhook_filters: typing.Optional[typing.List["FilterGroup"]]=None, identifier: typing.Optional[str]=None) -> "ISource":
        """
        :param props: -
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = GitHubSourceProps(owner=owner, repo=repo, clone_depth=clone_depth, report_build_status=report_build_status, webhook=webhook, webhook_filters=webhook_filters, identifier=identifier)

        return jsii.sinvoke(cls, "gitHub", [props])

    @jsii.member(jsii_name="gitHubEnterprise")
    @classmethod
    def git_hub_enterprise(cls, *, https_clone_url: str, clone_depth: typing.Optional[jsii.Number]=None, ignore_ssl_errors: typing.Optional[bool]=None, report_build_status: typing.Optional[bool]=None, webhook: typing.Optional[bool]=None, webhook_filters: typing.Optional[typing.List["FilterGroup"]]=None, identifier: typing.Optional[str]=None) -> "ISource":
        """
        :param props: -
        :param https_clone_url: The HTTPS URL of the repository in your GitHub Enterprise installation.
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param ignore_ssl_errors: Whether to ignore SSL errors when connecting to the repository. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = GitHubEnterpriseSourceProps(https_clone_url=https_clone_url, clone_depth=clone_depth, ignore_ssl_errors=ignore_ssl_errors, report_build_status=report_build_status, webhook=webhook, webhook_filters=webhook_filters, identifier=identifier)

        return jsii.sinvoke(cls, "gitHubEnterprise", [props])

    @jsii.member(jsii_name="s3")
    @classmethod
    def s3(cls, *, bucket: aws_cdk.aws_s3.IBucket, path: str, identifier: typing.Optional[str]=None) -> "ISource":
        """
        :param props: -
        :param bucket: 
        :param path: 
        :param identifier: The source identifier. This property is required on secondary sources.
        """
        props = S3SourceProps(bucket=bucket, path=path, identifier=identifier)

        return jsii.sinvoke(cls, "s3", [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, _project: "IProject") -> "SourceConfig":
        """Called by the project when the source is added so that the source can perform binding operations on the source.

        For example, it can grant permissions to the
        code build project to read from the S3 bucket.

        :param _scope: -
        :param _project: -
        """
        return jsii.invoke(self, "bind", [_scope, _project])

    @property
    @jsii.member(jsii_name="badgeSupported")
    def badge_supported(self) -> bool:
        return jsii.get(self, "badgeSupported")

    @property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> typing.Optional[str]:
        return jsii.get(self, "identifier")


class _SourceProxy(Source):
    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        return jsii.get(self, "type")


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.SourceConfig", jsii_struct_bases=[], name_mapping={'source_property': 'sourceProperty', 'build_triggers': 'buildTriggers'})
class SourceConfig():
    def __init__(self, *, source_property: "CfnProject.SourceProperty", build_triggers: typing.Optional["CfnProject.ProjectTriggersProperty"]=None):
        """The type returned from {@link ISource#bind}.

        :param source_property: 
        :param build_triggers: 
        """
        if isinstance(source_property, dict): source_property = CfnProject.SourceProperty(**source_property)
        if isinstance(build_triggers, dict): build_triggers = CfnProject.ProjectTriggersProperty(**build_triggers)
        self._values = {
            'source_property': source_property,
        }
        if build_triggers is not None: self._values["build_triggers"] = build_triggers

    @property
    def source_property(self) -> "CfnProject.SourceProperty":
        return self._values.get('source_property')

    @property
    def build_triggers(self) -> typing.Optional["CfnProject.ProjectTriggersProperty"]:
        return self._values.get('build_triggers')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SourceConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.SourceProps", jsii_struct_bases=[], name_mapping={'identifier': 'identifier'})
class SourceProps():
    def __init__(self, *, identifier: typing.Optional[str]=None):
        """Properties common to all Source classes.

        :param identifier: The source identifier. This property is required on secondary sources.
        """
        self._values = {
        }
        if identifier is not None: self._values["identifier"] = identifier

    @property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier. This property is required on secondary sources."""
        return self._values.get('identifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.BitBucketSourceProps", jsii_struct_bases=[SourceProps], name_mapping={'identifier': 'identifier', 'owner': 'owner', 'repo': 'repo', 'clone_depth': 'cloneDepth', 'report_build_status': 'reportBuildStatus', 'webhook': 'webhook', 'webhook_filters': 'webhookFilters'})
class BitBucketSourceProps(SourceProps):
    def __init__(self, *, identifier: typing.Optional[str]=None, owner: str, repo: str, clone_depth: typing.Optional[jsii.Number]=None, report_build_status: typing.Optional[bool]=None, webhook: typing.Optional[bool]=None, webhook_filters: typing.Optional[typing.List["FilterGroup"]]=None):
        """Construction properties for {@link BitBucketSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param owner: The BitBucket account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        """
        self._values = {
            'owner': owner,
            'repo': repo,
        }
        if identifier is not None: self._values["identifier"] = identifier
        if clone_depth is not None: self._values["clone_depth"] = clone_depth
        if report_build_status is not None: self._values["report_build_status"] = report_build_status
        if webhook is not None: self._values["webhook"] = webhook
        if webhook_filters is not None: self._values["webhook_filters"] = webhook_filters

    @property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier. This property is required on secondary sources."""
        return self._values.get('identifier')

    @property
    def owner(self) -> str:
        """The BitBucket account/user that owns the repo.

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            "awslabs"
        """
        return self._values.get('owner')

    @property
    def repo(self) -> str:
        """The name of the repo (without the username).

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        """
        return self._values.get('repo')

    @property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get('clone_depth')

    @property
    def report_build_status(self) -> typing.Optional[bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true
        """
        return self._values.get('report_build_status')

    @property
    def webhook(self) -> typing.Optional[bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise
        """
        return self._values.get('webhook')

    @property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build
        """
        return self._values.get('webhook_filters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BitBucketSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.CodeCommitSourceProps", jsii_struct_bases=[SourceProps], name_mapping={'identifier': 'identifier', 'repository': 'repository', 'clone_depth': 'cloneDepth'})
class CodeCommitSourceProps(SourceProps):
    def __init__(self, *, identifier: typing.Optional[str]=None, repository: aws_cdk.aws_codecommit.IRepository, clone_depth: typing.Optional[jsii.Number]=None):
        """Construction properties for {@link CodeCommitSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param repository: 
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        """
        self._values = {
            'repository': repository,
        }
        if identifier is not None: self._values["identifier"] = identifier
        if clone_depth is not None: self._values["clone_depth"] = clone_depth

    @property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier. This property is required on secondary sources."""
        return self._values.get('identifier')

    @property
    def repository(self) -> aws_cdk.aws_codecommit.IRepository:
        return self._values.get('repository')

    @property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get('clone_depth')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeCommitSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.GitHubEnterpriseSourceProps", jsii_struct_bases=[SourceProps], name_mapping={'identifier': 'identifier', 'https_clone_url': 'httpsCloneUrl', 'clone_depth': 'cloneDepth', 'ignore_ssl_errors': 'ignoreSslErrors', 'report_build_status': 'reportBuildStatus', 'webhook': 'webhook', 'webhook_filters': 'webhookFilters'})
class GitHubEnterpriseSourceProps(SourceProps):
    def __init__(self, *, identifier: typing.Optional[str]=None, https_clone_url: str, clone_depth: typing.Optional[jsii.Number]=None, ignore_ssl_errors: typing.Optional[bool]=None, report_build_status: typing.Optional[bool]=None, webhook: typing.Optional[bool]=None, webhook_filters: typing.Optional[typing.List["FilterGroup"]]=None):
        """Construction properties for {@link GitHubEnterpriseSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param https_clone_url: The HTTPS URL of the repository in your GitHub Enterprise installation.
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param ignore_ssl_errors: Whether to ignore SSL errors when connecting to the repository. Default: false
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        """
        self._values = {
            'https_clone_url': https_clone_url,
        }
        if identifier is not None: self._values["identifier"] = identifier
        if clone_depth is not None: self._values["clone_depth"] = clone_depth
        if ignore_ssl_errors is not None: self._values["ignore_ssl_errors"] = ignore_ssl_errors
        if report_build_status is not None: self._values["report_build_status"] = report_build_status
        if webhook is not None: self._values["webhook"] = webhook
        if webhook_filters is not None: self._values["webhook_filters"] = webhook_filters

    @property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier. This property is required on secondary sources."""
        return self._values.get('identifier')

    @property
    def https_clone_url(self) -> str:
        """The HTTPS URL of the repository in your GitHub Enterprise installation."""
        return self._values.get('https_clone_url')

    @property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get('clone_depth')

    @property
    def ignore_ssl_errors(self) -> typing.Optional[bool]:
        """Whether to ignore SSL errors when connecting to the repository.

        default
        :default: false
        """
        return self._values.get('ignore_ssl_errors')

    @property
    def report_build_status(self) -> typing.Optional[bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true
        """
        return self._values.get('report_build_status')

    @property
    def webhook(self) -> typing.Optional[bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise
        """
        return self._values.get('webhook')

    @property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build
        """
        return self._values.get('webhook_filters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitHubEnterpriseSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.GitHubSourceProps", jsii_struct_bases=[SourceProps], name_mapping={'identifier': 'identifier', 'owner': 'owner', 'repo': 'repo', 'clone_depth': 'cloneDepth', 'report_build_status': 'reportBuildStatus', 'webhook': 'webhook', 'webhook_filters': 'webhookFilters'})
class GitHubSourceProps(SourceProps):
    def __init__(self, *, identifier: typing.Optional[str]=None, owner: str, repo: str, clone_depth: typing.Optional[jsii.Number]=None, report_build_status: typing.Optional[bool]=None, webhook: typing.Optional[bool]=None, webhook_filters: typing.Optional[typing.List["FilterGroup"]]=None):
        """Construction properties for {@link GitHubSource} and {@link GitHubEnterpriseSource}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo (without the username).
        :param clone_depth: The depth of history to download. Minimum value is 0. If this value is 0, greater than 25, or not provided, then the full history is downloaded with each build of the project.
        :param report_build_status: Whether to send notifications on your build's start and end. Default: true
        :param webhook: Whether to create a webhook that will trigger a build every time an event happens in the repository. Default: true if any ``webhookFilters`` were provided, false otherwise
        :param webhook_filters: A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false. Default: every push and every Pull Request (create or update) triggers a build
        """
        self._values = {
            'owner': owner,
            'repo': repo,
        }
        if identifier is not None: self._values["identifier"] = identifier
        if clone_depth is not None: self._values["clone_depth"] = clone_depth
        if report_build_status is not None: self._values["report_build_status"] = report_build_status
        if webhook is not None: self._values["webhook"] = webhook
        if webhook_filters is not None: self._values["webhook_filters"] = webhook_filters

    @property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier. This property is required on secondary sources."""
        return self._values.get('identifier')

    @property
    def owner(self) -> str:
        """The GitHub account/user that owns the repo.

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            "awslabs"
        """
        return self._values.get('owner')

    @property
    def repo(self) -> str:
        """The name of the repo (without the username).

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        """
        return self._values.get('repo')

    @property
    def clone_depth(self) -> typing.Optional[jsii.Number]:
        """The depth of history to download.

        Minimum value is 0.
        If this value is 0, greater than 25, or not provided,
        then the full history is downloaded with each build of the project.
        """
        return self._values.get('clone_depth')

    @property
    def report_build_status(self) -> typing.Optional[bool]:
        """Whether to send notifications on your build's start and end.

        default
        :default: true
        """
        return self._values.get('report_build_status')

    @property
    def webhook(self) -> typing.Optional[bool]:
        """Whether to create a webhook that will trigger a build every time an event happens in the repository.

        default
        :default: true if any ``webhookFilters`` were provided, false otherwise
        """
        return self._values.get('webhook')

    @property
    def webhook_filters(self) -> typing.Optional[typing.List["FilterGroup"]]:
        """A list of webhook filters that can constraint what events in the repository will trigger a build. A build is triggered if any of the provided filter groups match. Only valid if ``webhook`` was not provided as false.

        default
        :default: every push and every Pull Request (create or update) triggers a build
        """
        return self._values.get('webhook_filters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitHubSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codebuild.S3SourceProps", jsii_struct_bases=[SourceProps], name_mapping={'identifier': 'identifier', 'bucket': 'bucket', 'path': 'path'})
class S3SourceProps(SourceProps):
    def __init__(self, *, identifier: typing.Optional[str]=None, bucket: aws_cdk.aws_s3.IBucket, path: str):
        """Construction properties for {@link S3Source}.

        :param identifier: The source identifier. This property is required on secondary sources.
        :param bucket: 
        :param path: 
        """
        self._values = {
            'bucket': bucket,
            'path': path,
        }
        if identifier is not None: self._values["identifier"] = identifier

    @property
    def identifier(self) -> typing.Optional[str]:
        """The source identifier. This property is required on secondary sources."""
        return self._values.get('identifier')

    @property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        return self._values.get('bucket')

    @property
    def path(self) -> str:
        return self._values.get('path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3SourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class StateChangeEvent(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.StateChangeEvent"):
    """Event fields for the CodeBuild "state change" event.

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-notifications.html#sample-build-notifications-ref
    """
    @classproperty
    @jsii.member(jsii_name="buildId")
    def build_id(cls) -> str:
        """Return the build id."""
        return jsii.sget(cls, "buildId")

    @classproperty
    @jsii.member(jsii_name="buildStatus")
    def build_status(cls) -> str:
        """The triggering build's status."""
        return jsii.sget(cls, "buildStatus")

    @classproperty
    @jsii.member(jsii_name="currentPhase")
    def current_phase(cls) -> str:
        return jsii.sget(cls, "currentPhase")

    @classproperty
    @jsii.member(jsii_name="projectName")
    def project_name(cls) -> str:
        """The triggering build's project name."""
        return jsii.sget(cls, "projectName")


@jsii.implements(IBuildImage)
class WindowsBuildImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codebuild.WindowsBuildImage"):
    """A CodeBuild image running Windows.

    This class has a bunch of public constants that represent the most popular images.

    You can also specify a custom image using one of the static methods:

    - WindowsBuildImage.fromDockerRegistry(image[, { secretsManagerCredentials }])
    - WindowsBuildImage.fromEcrRepository(repo[, tag])
    - WindowsBuildImage.fromAsset(parent, id, props)

    see
    :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
    """
    @jsii.member(jsii_name="fromAsset")
    @classmethod
    def from_asset(cls, scope: aws_cdk.core.Construct, id: str, *, directory: str, build_args: typing.Optional[typing.Mapping[str,str]]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None) -> "IBuildImage":
        """Uses an Docker image asset as a Windows build image.

        :param scope: -
        :param id: -
        :param props: -
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.
        :param target: Docker target to build to. Default: - no target
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        """
        props = aws_cdk.aws_ecr_assets.DockerImageAssetProps(directory=directory, build_args=build_args, repository_name=repository_name, target=target, exclude=exclude, follow=follow)

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromDockerRegistry")
    @classmethod
    def from_docker_registry(cls, name: str, *, secrets_manager_credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> "IBuildImage":
        """
        :param name: -
        :param options: -
        :param secrets_manager_credentials: The credentials, stored in Secrets Manager, used for accessing the repository holding the image, if the repository is private. Default: no credentials will be used (we assume the repository is public)

        return
        :return: a Windows build image from a Docker Hub image.
        """
        options = DockerImageOptions(secrets_manager_credentials=secrets_manager_credentials)

        return jsii.sinvoke(cls, "fromDockerRegistry", [name, options])

    @jsii.member(jsii_name="fromEcrRepository")
    @classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "IBuildImage":
        """
        :param repository: The ECR repository.
        :param tag: Image tag (default "latest").

        return
        :return:

        A Linux build image from an ECR repository.

        NOTE: if the repository is external (i.e. imported), then we won't be able to add
        a resource policy statement for it so CodeBuild can pull the image.

        see
        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/sample-ecr.html
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="runScriptBuildspec")
    def run_script_buildspec(self, entrypoint: str) -> "BuildSpec":
        """Make a buildspec to run the indicated script.

        :param entrypoint: -
        """
        return jsii.invoke(self, "runScriptBuildspec", [entrypoint])

    @jsii.member(jsii_name="validate")
    def validate(self, *, build_image: typing.Optional["IBuildImage"]=None, compute_type: typing.Optional["ComputeType"]=None, environment_variables: typing.Optional[typing.Mapping[str,"BuildEnvironmentVariable"]]=None, privileged: typing.Optional[bool]=None) -> typing.List[str]:
        """Allows the image a chance to validate whether the passed configuration is correct.

        :param build_environment: -
        :param build_image: The image used for the builds. Default: LinuxBuildImage.STANDARD_1_0
        :param compute_type: The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: taken from {@link #buildImage#defaultComputeType}
        :param environment_variables: The environment variables that your builds can use.
        :param privileged: Indicates how the project builds Docker images. Specify true to enable running the Docker daemon inside a Docker container. This value must be set to true only if this build project will be used to build Docker images, and the specified build environment image is not one provided by AWS CodeBuild with Docker support. Otherwise, all associated builds that attempt to interact with the Docker daemon will fail. Default: false
        """
        build_environment = BuildEnvironment(build_image=build_image, compute_type=compute_type, environment_variables=environment_variables, privileged=privileged)

        return jsii.invoke(self, "validate", [build_environment])

    @classproperty
    @jsii.member(jsii_name="WIN_SERVER_CORE_2016_BASE")
    def WIN_SERVER_CORE_2016_BASE(cls) -> "IBuildImage":
        return jsii.sget(cls, "WIN_SERVER_CORE_2016_BASE")

    @property
    @jsii.member(jsii_name="defaultComputeType")
    def default_compute_type(self) -> "ComputeType":
        """The default {@link ComputeType} to use with this image, if one was not specified in {@link BuildEnvironment#computeType} explicitly."""
        return jsii.get(self, "defaultComputeType")

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        """The Docker image identifier that the build environment uses."""
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """The type of build environment."""
        return jsii.get(self, "type")

    @property
    @jsii.member(jsii_name="imagePullPrincipalType")
    def image_pull_principal_type(self) -> typing.Optional["ImagePullPrincipalType"]:
        """The type of principal that CodeBuild will use to pull this build Docker image."""
        return jsii.get(self, "imagePullPrincipalType")

    @property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[aws_cdk.aws_ecr.IRepository]:
        """An optional ECR repository that the image is hosted in."""
        return jsii.get(self, "repository")

    @property
    @jsii.member(jsii_name="secretsManagerCredentials")
    def secrets_manager_credentials(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secretsManagerCredentials for access to a private registry."""
        return jsii.get(self, "secretsManagerCredentials")


__all__ = ["Artifacts", "ArtifactsConfig", "ArtifactsProps", "BindToCodePipelineOptions", "BitBucketSourceProps", "BucketCacheOptions", "BuildEnvironment", "BuildEnvironmentVariable", "BuildEnvironmentVariableType", "BuildSpec", "Cache", "CfnProject", "CfnProjectProps", "CfnSourceCredential", "CfnSourceCredentialProps", "CodeCommitSourceProps", "CommonProjectProps", "ComputeType", "DockerImageOptions", "EventAction", "FilterGroup", "GitHubEnterpriseSourceProps", "GitHubSourceProps", "IArtifacts", "IBuildImage", "IProject", "ISource", "ImagePullPrincipalType", "LinuxBuildImage", "LocalCacheMode", "PhaseChangeEvent", "PipelineProject", "PipelineProjectProps", "Project", "ProjectProps", "S3ArtifactsProps", "S3SourceProps", "Source", "SourceConfig", "SourceProps", "StateChangeEvent", "WindowsBuildImage", "__jsii_assembly__"]

publication.publish()
