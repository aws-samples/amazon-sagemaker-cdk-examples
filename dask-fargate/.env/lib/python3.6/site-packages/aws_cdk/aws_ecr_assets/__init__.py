"""
# AWS CDK Docker Image Assets

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

This module allows bundling Docker images as assets.

Images are built from a local Docker context directory (with a `Dockerfile`),
uploaded to ECR by the CDK toolkit and/or your app's CI-CD pipeline, and can be
naturally referenced in your CDK app.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ecr_assets import DockerImageAsset

asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image")
)
```

The directory `my-image` must include a `Dockerfile`.

This will instruct the toolkit to build a Docker image from `my-image`, push it
to an AWS ECR repository and wire the name of the repository as CloudFormation
parameters to your stack.

Use `asset.imageUri` to reference the image (it includes both the ECR image URL
and tag.

You can optionally pass build args to the `docker build` command by specifying
the `buildArgs` property:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    build_args={
        "HTTP_PROXY": "http://10.20.30.2:1234"
    }
)
```

You can optionally pass a target to the `docker build` command by specifying
the `target` property:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
asset = DockerImageAsset(self, "MyBuildImage",
    directory=path.join(__dirname, "my-image"),
    target="a-target"
)
```

### Pull Permissions

Depending on the consumer of your image asset, you will need to make sure
the principal has permissions to pull the image.

In most cases, you should use the `asset.repository.grantPull(principal)`
method. This will modify the IAM policy of the principal to allow it to
pull images from this repository.

If the pulling principal is not in the same account or is an AWS service that
doesn't assume a role in your account (e.g. AWS CodeBuild), pull permissions
must be granted on the **resource policy** (and not on the principal's policy).
To do that, you can use `asset.repository.addToResourcePolicy(statement)` to
grant the desired principal the following permissions: "ecr:GetDownloadUrlForLayer",
"ecr:BatchGetImage" and "ecr:BatchCheckLayerAvailability".
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
import aws_cdk.aws_cloudformation
import aws_cdk.aws_ecr
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecr-assets", "1.18.0", __name__, "aws-ecr-assets@1.18.0.jsii.tgz")
@jsii.implements(aws_cdk.assets.IAsset)
class DockerImageAsset(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecr-assets.DockerImageAsset"):
    """An asset that represents a Docker image.

    The image will be created in build time and uploaded to an ECR repository.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, directory: str, build_args: typing.Optional[typing.Mapping[str,str]]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.
        :param target: Docker target to build to. Default: - no target
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        props = DockerImageAssetProps(directory=directory, build_args=build_args, repository_name=repository_name, target=target, exclude=exclude, follow=follow)

        jsii.create(DockerImageAsset, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "sourceHash")

    @property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> str:
        """The full URI of the image (including a tag).

        Use this reference to pull
        the asset.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imageUri")

    @image_uri.setter
    def image_uri(self, value: str):
        return jsii.set(self, "imageUri", value)

    @property
    @jsii.member(jsii_name="repository")
    def repository(self) -> aws_cdk.aws_ecr.IRepository:
        """Repository where the image is stored.

        stability
        :stability: experimental
        """
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: aws_cdk.aws_ecr.IRepository):
        return jsii.set(self, "repository", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-ecr-assets.DockerImageAssetProps", jsii_struct_bases=[aws_cdk.assets.CopyOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'directory': 'directory', 'build_args': 'buildArgs', 'repository_name': 'repositoryName', 'target': 'target'})
class DockerImageAssetProps(aws_cdk.assets.CopyOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[aws_cdk.assets.FollowMode]=None, directory: str, build_args: typing.Optional[typing.Mapping[str,str]]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None):
        """
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param directory: The directory where the Dockerfile is stored.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - automatically derived from the asset's ID.
        :param target: Docker target to build to. Default: - no target

        stability
        :stability: experimental
        """
        self._values = {
            'directory': directory,
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if build_args is not None: self._values["build_args"] = build_args
        if repository_name is not None: self._values["repository_name"] = repository_name
        if target is not None: self._values["target"] = target

    @property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: experimental
        """
        return self._values.get('exclude')

    @property
    def follow(self) -> typing.Optional[aws_cdk.assets.FollowMode]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: experimental
        """
        return self._values.get('follow')

    @property
    def directory(self) -> str:
        """The directory where the Dockerfile is stored.

        stability
        :stability: experimental
        """
        return self._values.get('directory')

    @property
    def build_args(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        default
        :default: - no build args are passed

        stability
        :stability: experimental
        """
        return self._values.get('build_args')

    @property
    def repository_name(self) -> typing.Optional[str]:
        """ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        default
        :default: - automatically derived from the asset's ID.

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    @property
    def target(self) -> typing.Optional[str]:
        """Docker target to build to.

        default
        :default: - no target

        stability
        :stability: experimental
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageAssetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["DockerImageAsset", "DockerImageAssetProps", "__jsii_assembly__"]

publication.publish()
