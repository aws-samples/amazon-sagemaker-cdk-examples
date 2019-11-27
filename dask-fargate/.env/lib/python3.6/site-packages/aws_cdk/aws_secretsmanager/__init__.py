"""
## AWS Secrets Manager Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
secretsmanager = require("@aws-cdk/aws-secretsmanager")
```

### Create a new Secret in a Stack

In order to have SecretsManager generate a new secret value automatically,
you can get started with the following:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Default secret
secret = secretsmanager.Secret(self, "Secret")
secret.grant_read(role)

iam.User(self, "User",
    password=secret.secret_value
)

# Templated secret
templated_secret = secretsmanager.Secret(self, "TemplatedSecret",
    generate_secret_string={
        "secret_string_template": JSON.stringify(username="user"),
        "generate_string_key": "password"
    }
)

iam.User(self, "OtherUser",
    user_name=templated_secret.secret_value_from_json("username").to_string(),
    password=templated_secret.secret_value_from_json("password")
)
```

The `Secret` construct does not allow specifying the `SecretString` property
of the `AWS::SecretsManager::Secret` resource (as this will almost always
lead to the secret being surfaced in plain text and possibly committed to
your source control).

If you need to use a pre-existing secret, the recommended way is to manually
provision the secret in *AWS SecretsManager* and use the `Secret.fromSecretArn`
or `Secret.fromSecretAttributes` method to make it available in your CDK Application:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
secret = secretsmanager.Secret.from_secret_attributes(scope, "ImportedSecret",
    secret_arn="arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name>-<random-6-characters>",
    # If the secret is encrypted using a KMS-hosted CMK, either import or reference that key:
    encryption_key=encryption_key
)
```

SecretsManager secret values can only be used in select set of properties. For the
list of properties, see [the CloudFormation Dynamic References documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.htm).

### Rotating a Secret

A rotation schedule can be added to a Secret:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
fn = lambda.Function(...)
secret = secretsmanager.Secret(self, "Secret")

secret.add_rotation_schedule("RotationSchedule",
    rotation_lambda=fn,
    automatically_after=Duration.days(15)
)
```

See [Overview of the Lambda Rotation Function](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-lambda-function-overview.html) on how to implement a Lambda Rotation Function.

For RDS credentials rotation, see [aws-rds](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-rds/README.md).
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
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-secretsmanager", "1.18.0", __name__, "aws-secretsmanager@1.18.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.AttachedSecretOptions", jsii_struct_bases=[], name_mapping={'target': 'target'})
class AttachedSecretOptions():
    def __init__(self, *, target: "ISecretAttachmentTarget"):
        """Options to add a secret attachment to a secret.

        :param target: The target to attach the secret to.
        """
        self._values = {
            'target': target,
        }

    @property
    def target(self) -> "ISecretAttachmentTarget":
        """The target to attach the secret to."""
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AttachedSecretOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-secretsmanager.AttachmentTargetType")
class AttachmentTargetType(enum.Enum):
    """The type of service or database that's being associated with the secret."""
    INSTANCE = "INSTANCE"
    """A database instance."""
    CLUSTER = "CLUSTER"
    """A database cluster."""

@jsii.implements(aws_cdk.core.IInspectable)
class CfnResourcePolicy(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicy"):
    """A CloudFormation ``AWS::SecretsManager::ResourcePolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::ResourcePolicy
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, resource_policy: typing.Any, secret_id: str) -> None:
        """Create a new ``AWS::SecretsManager::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param resource_policy: ``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.
        :param secret_id: ``AWS::SecretsManager::ResourcePolicy.SecretId``.
        """
        props = CfnResourcePolicyProps(resource_policy=resource_policy, secret_id=secret_id)

        jsii.create(CfnResourcePolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="resourcePolicy")
    def resource_policy(self) -> typing.Any:
        """``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        """
        return jsii.get(self, "resourcePolicy")

    @resource_policy.setter
    def resource_policy(self, value: typing.Any):
        return jsii.set(self, "resourcePolicy", value)

    @property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> str:
        """``AWS::SecretsManager::ResourcePolicy.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter
    def secret_id(self, value: str):
        return jsii.set(self, "secretId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnResourcePolicyProps", jsii_struct_bases=[], name_mapping={'resource_policy': 'resourcePolicy', 'secret_id': 'secretId'})
class CfnResourcePolicyProps():
    def __init__(self, *, resource_policy: typing.Any, secret_id: str):
        """Properties for defining a ``AWS::SecretsManager::ResourcePolicy``.

        :param resource_policy: ``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.
        :param secret_id: ``AWS::SecretsManager::ResourcePolicy.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
        """
        self._values = {
            'resource_policy': resource_policy,
            'secret_id': secret_id,
        }

    @property
    def resource_policy(self) -> typing.Any:
        """``AWS::SecretsManager::ResourcePolicy.ResourcePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        """
        return self._values.get('resource_policy')

    @property
    def secret_id(self) -> str:
        """``AWS::SecretsManager::ResourcePolicy.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        """
        return self._values.get('secret_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourcePolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRotationSchedule(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule"):
    """A CloudFormation ``AWS::SecretsManager::RotationSchedule``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::RotationSchedule
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, secret_id: str, rotation_lambda_arn: typing.Optional[str]=None, rotation_rules: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RotationRulesProperty"]]]=None) -> None:
        """Create a new ``AWS::SecretsManager::RotationSchedule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param secret_id: ``AWS::SecretsManager::RotationSchedule.SecretId``.
        :param rotation_lambda_arn: ``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.
        :param rotation_rules: ``AWS::SecretsManager::RotationSchedule.RotationRules``.
        """
        props = CfnRotationScheduleProps(secret_id=secret_id, rotation_lambda_arn=rotation_lambda_arn, rotation_rules=rotation_rules)

        jsii.create(CfnRotationSchedule, self, [scope, id, props])

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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> str:
        """``AWS::SecretsManager::RotationSchedule.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter
    def secret_id(self, value: str):
        return jsii.set(self, "secretId", value)

    @property
    @jsii.member(jsii_name="rotationLambdaArn")
    def rotation_lambda_arn(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        """
        return jsii.get(self, "rotationLambdaArn")

    @rotation_lambda_arn.setter
    def rotation_lambda_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "rotationLambdaArn", value)

    @property
    @jsii.member(jsii_name="rotationRules")
    def rotation_rules(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RotationRulesProperty"]]]:
        """``AWS::SecretsManager::RotationSchedule.RotationRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        """
        return jsii.get(self, "rotationRules")

    @rotation_rules.setter
    def rotation_rules(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RotationRulesProperty"]]]):
        return jsii.set(self, "rotationRules", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationSchedule.RotationRulesProperty", jsii_struct_bases=[], name_mapping={'automatically_after_days': 'automaticallyAfterDays'})
    class RotationRulesProperty():
        def __init__(self, *, automatically_after_days: typing.Optional[jsii.Number]=None):
            """
            :param automatically_after_days: ``CfnRotationSchedule.RotationRulesProperty.AutomaticallyAfterDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html
            """
            self._values = {
            }
            if automatically_after_days is not None: self._values["automatically_after_days"] = automatically_after_days

        @property
        def automatically_after_days(self) -> typing.Optional[jsii.Number]:
            """``CfnRotationSchedule.RotationRulesProperty.AutomaticallyAfterDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-automaticallyafterdays
            """
            return self._values.get('automatically_after_days')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RotationRulesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnRotationScheduleProps", jsii_struct_bases=[], name_mapping={'secret_id': 'secretId', 'rotation_lambda_arn': 'rotationLambdaArn', 'rotation_rules': 'rotationRules'})
class CfnRotationScheduleProps():
    def __init__(self, *, secret_id: str, rotation_lambda_arn: typing.Optional[str]=None, rotation_rules: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRotationSchedule.RotationRulesProperty"]]]=None):
        """Properties for defining a ``AWS::SecretsManager::RotationSchedule``.

        :param secret_id: ``AWS::SecretsManager::RotationSchedule.SecretId``.
        :param rotation_lambda_arn: ``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.
        :param rotation_rules: ``AWS::SecretsManager::RotationSchedule.RotationRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
        """
        self._values = {
            'secret_id': secret_id,
        }
        if rotation_lambda_arn is not None: self._values["rotation_lambda_arn"] = rotation_lambda_arn
        if rotation_rules is not None: self._values["rotation_rules"] = rotation_rules

    @property
    def secret_id(self) -> str:
        """``AWS::SecretsManager::RotationSchedule.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        """
        return self._values.get('secret_id')

    @property
    def rotation_lambda_arn(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::RotationSchedule.RotationLambdaARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        """
        return self._values.get('rotation_lambda_arn')

    @property
    def rotation_rules(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnRotationSchedule.RotationRulesProperty"]]]:
        """``AWS::SecretsManager::RotationSchedule.RotationRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        """
        return self._values.get('rotation_rules')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRotationScheduleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSecret(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret"):
    """A CloudFormation ``AWS::SecretsManager::Secret``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::Secret
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, generate_secret_string: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GenerateSecretStringProperty"]]]=None, kms_key_id: typing.Optional[str]=None, name: typing.Optional[str]=None, secret_string: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::SecretsManager::Secret``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param description: ``AWS::SecretsManager::Secret.Description``.
        :param generate_secret_string: ``AWS::SecretsManager::Secret.GenerateSecretString``.
        :param kms_key_id: ``AWS::SecretsManager::Secret.KmsKeyId``.
        :param name: ``AWS::SecretsManager::Secret.Name``.
        :param secret_string: ``AWS::SecretsManager::Secret.SecretString``.
        :param tags: ``AWS::SecretsManager::Secret.Tags``.
        """
        props = CfnSecretProps(description=description, generate_secret_string=generate_secret_string, kms_key_id=kms_key_id, name=name, secret_string=secret_string, tags=tags)

        jsii.create(CfnSecret, self, [scope, id, props])

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
        """``AWS::SecretsManager::Secret.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="generateSecretString")
    def generate_secret_string(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GenerateSecretStringProperty"]]]:
        """``AWS::SecretsManager::Secret.GenerateSecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        """
        return jsii.get(self, "generateSecretString")

    @generate_secret_string.setter
    def generate_secret_string(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GenerateSecretStringProperty"]]]):
        return jsii.set(self, "generateSecretString", value)

    @property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]):
        return jsii.set(self, "kmsKeyId", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="secretString")
    def secret_string(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.SecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        """
        return jsii.get(self, "secretString")

    @secret_string.setter
    def secret_string(self, value: typing.Optional[str]):
        return jsii.set(self, "secretString", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecret.GenerateSecretStringProperty", jsii_struct_bases=[], name_mapping={'exclude_characters': 'excludeCharacters', 'exclude_lowercase': 'excludeLowercase', 'exclude_numbers': 'excludeNumbers', 'exclude_punctuation': 'excludePunctuation', 'exclude_uppercase': 'excludeUppercase', 'generate_string_key': 'generateStringKey', 'include_space': 'includeSpace', 'password_length': 'passwordLength', 'require_each_included_type': 'requireEachIncludedType', 'secret_string_template': 'secretStringTemplate'})
    class GenerateSecretStringProperty():
        def __init__(self, *, exclude_characters: typing.Optional[str]=None, exclude_lowercase: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, exclude_numbers: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, exclude_punctuation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, exclude_uppercase: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, generate_string_key: typing.Optional[str]=None, include_space: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, password_length: typing.Optional[jsii.Number]=None, require_each_included_type: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, secret_string_template: typing.Optional[str]=None):
            """
            :param exclude_characters: ``CfnSecret.GenerateSecretStringProperty.ExcludeCharacters``.
            :param exclude_lowercase: ``CfnSecret.GenerateSecretStringProperty.ExcludeLowercase``.
            :param exclude_numbers: ``CfnSecret.GenerateSecretStringProperty.ExcludeNumbers``.
            :param exclude_punctuation: ``CfnSecret.GenerateSecretStringProperty.ExcludePunctuation``.
            :param exclude_uppercase: ``CfnSecret.GenerateSecretStringProperty.ExcludeUppercase``.
            :param generate_string_key: ``CfnSecret.GenerateSecretStringProperty.GenerateStringKey``.
            :param include_space: ``CfnSecret.GenerateSecretStringProperty.IncludeSpace``.
            :param password_length: ``CfnSecret.GenerateSecretStringProperty.PasswordLength``.
            :param require_each_included_type: ``CfnSecret.GenerateSecretStringProperty.RequireEachIncludedType``.
            :param secret_string_template: ``CfnSecret.GenerateSecretStringProperty.SecretStringTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html
            """
            self._values = {
            }
            if exclude_characters is not None: self._values["exclude_characters"] = exclude_characters
            if exclude_lowercase is not None: self._values["exclude_lowercase"] = exclude_lowercase
            if exclude_numbers is not None: self._values["exclude_numbers"] = exclude_numbers
            if exclude_punctuation is not None: self._values["exclude_punctuation"] = exclude_punctuation
            if exclude_uppercase is not None: self._values["exclude_uppercase"] = exclude_uppercase
            if generate_string_key is not None: self._values["generate_string_key"] = generate_string_key
            if include_space is not None: self._values["include_space"] = include_space
            if password_length is not None: self._values["password_length"] = password_length
            if require_each_included_type is not None: self._values["require_each_included_type"] = require_each_included_type
            if secret_string_template is not None: self._values["secret_string_template"] = secret_string_template

        @property
        def exclude_characters(self) -> typing.Optional[str]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeCharacters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludecharacters
            """
            return self._values.get('exclude_characters')

        @property
        def exclude_lowercase(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeLowercase``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludelowercase
            """
            return self._values.get('exclude_lowercase')

        @property
        def exclude_numbers(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeNumbers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludenumbers
            """
            return self._values.get('exclude_numbers')

        @property
        def exclude_punctuation(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludePunctuation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludepunctuation
            """
            return self._values.get('exclude_punctuation')

        @property
        def exclude_uppercase(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnSecret.GenerateSecretStringProperty.ExcludeUppercase``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludeuppercase
            """
            return self._values.get('exclude_uppercase')

        @property
        def generate_string_key(self) -> typing.Optional[str]:
            """``CfnSecret.GenerateSecretStringProperty.GenerateStringKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-generatestringkey
            """
            return self._values.get('generate_string_key')

        @property
        def include_space(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnSecret.GenerateSecretStringProperty.IncludeSpace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-includespace
            """
            return self._values.get('include_space')

        @property
        def password_length(self) -> typing.Optional[jsii.Number]:
            """``CfnSecret.GenerateSecretStringProperty.PasswordLength``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-passwordlength
            """
            return self._values.get('password_length')

        @property
        def require_each_included_type(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnSecret.GenerateSecretStringProperty.RequireEachIncludedType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-requireeachincludedtype
            """
            return self._values.get('require_each_included_type')

        @property
        def secret_string_template(self) -> typing.Optional[str]:
            """``CfnSecret.GenerateSecretStringProperty.SecretStringTemplate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-secretstringtemplate
            """
            return self._values.get('secret_string_template')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GenerateSecretStringProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'generate_secret_string': 'generateSecretString', 'kms_key_id': 'kmsKeyId', 'name': 'name', 'secret_string': 'secretString', 'tags': 'tags'})
class CfnSecretProps():
    def __init__(self, *, description: typing.Optional[str]=None, generate_secret_string: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnSecret.GenerateSecretStringProperty"]]]=None, kms_key_id: typing.Optional[str]=None, name: typing.Optional[str]=None, secret_string: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::SecretsManager::Secret``.

        :param description: ``AWS::SecretsManager::Secret.Description``.
        :param generate_secret_string: ``AWS::SecretsManager::Secret.GenerateSecretString``.
        :param kms_key_id: ``AWS::SecretsManager::Secret.KmsKeyId``.
        :param name: ``AWS::SecretsManager::Secret.Name``.
        :param secret_string: ``AWS::SecretsManager::Secret.SecretString``.
        :param tags: ``AWS::SecretsManager::Secret.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if generate_secret_string is not None: self._values["generate_secret_string"] = generate_secret_string
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if name is not None: self._values["name"] = name
        if secret_string is not None: self._values["secret_string"] = secret_string
        if tags is not None: self._values["tags"] = tags

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        """
        return self._values.get('description')

    @property
    def generate_secret_string(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnSecret.GenerateSecretStringProperty"]]]:
        """``AWS::SecretsManager::Secret.GenerateSecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        """
        return self._values.get('generate_secret_string')

    @property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        """
        return self._values.get('kms_key_id')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        """
        return self._values.get('name')

    @property
    def secret_string(self) -> typing.Optional[str]:
        """``AWS::SecretsManager::Secret.SecretString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        """
        return self._values.get('secret_string')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SecretsManager::Secret.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSecretProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSecretTargetAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachment"):
    """A CloudFormation ``AWS::SecretsManager::SecretTargetAttachment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    cloudformationResource:
    :cloudformationResource:: AWS::SecretsManager::SecretTargetAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, secret_id: str, target_id: str, target_type: str) -> None:
        """Create a new ``AWS::SecretsManager::SecretTargetAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param secret_id: ``AWS::SecretsManager::SecretTargetAttachment.SecretId``.
        :param target_id: ``AWS::SecretsManager::SecretTargetAttachment.TargetId``.
        :param target_type: ``AWS::SecretsManager::SecretTargetAttachment.TargetType``.
        """
        props = CfnSecretTargetAttachmentProps(secret_id=secret_id, target_id=target_id, target_type=target_type)

        jsii.create(CfnSecretTargetAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        """
        return jsii.get(self, "secretId")

    @secret_id.setter
    def secret_id(self, value: str):
        return jsii.set(self, "secretId", value)

    @property
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        """
        return jsii.get(self, "targetId")

    @target_id.setter
    def target_id(self, value: str):
        return jsii.set(self, "targetId", value)

    @property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        """
        return jsii.get(self, "targetType")

    @target_type.setter
    def target_type(self, value: str):
        return jsii.set(self, "targetType", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.CfnSecretTargetAttachmentProps", jsii_struct_bases=[], name_mapping={'secret_id': 'secretId', 'target_id': 'targetId', 'target_type': 'targetType'})
class CfnSecretTargetAttachmentProps():
    def __init__(self, *, secret_id: str, target_id: str, target_type: str):
        """Properties for defining a ``AWS::SecretsManager::SecretTargetAttachment``.

        :param secret_id: ``AWS::SecretsManager::SecretTargetAttachment.SecretId``.
        :param target_id: ``AWS::SecretsManager::SecretTargetAttachment.TargetId``.
        :param target_type: ``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        """
        self._values = {
            'secret_id': secret_id,
            'target_id': target_id,
            'target_type': target_type,
        }

    @property
    def secret_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.SecretId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        """
        return self._values.get('secret_id')

    @property
    def target_id(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        """
        return self._values.get('target_id')

    @property
    def target_type(self) -> str:
        """``AWS::SecretsManager::SecretTargetAttachment.TargetType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        """
        return self._values.get('target_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSecretTargetAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecret")
class ISecret(aws_cdk.core.IResource, jsii.compat.Protocol):
    """A secret in AWS Secrets Manager."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretProxy

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        ...

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param options: -
        :param rotation_lambda: THe Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.
        """
        ...

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: str) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -
        """
        ...


class _ISecretProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """A secret in AWS Secrets Manager."""
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecret"
    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param options: -
        :param rotation_lambda: THe Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        """
        options = RotationScheduleOptions(rotation_lambda=rotation_lambda, automatically_after=automatically_after)

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: the principal being granted permission.
        :param version_stages: the version stages the grant is limited to. If not specified, no restriction on the version stages is applied.
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, key: str) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param key: -
        """
        return jsii.invoke(self, "secretValueFromJson", [key])


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget")
class ISecretAttachmentTarget(jsii.compat.Protocol):
    """A secret attachment target."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretAttachmentTargetProxy

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications."""
        ...


class _ISecretAttachmentTargetProxy():
    """A secret attachment target."""
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecretAttachmentTarget"
    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> "SecretAttachmentTargetProps":
        """Renders the target specifications."""
        return jsii.invoke(self, "asSecretAttachmentTarget", [])


@jsii.interface(jsii_type="@aws-cdk/aws-secretsmanager.ISecretTargetAttachment")
class ISecretTargetAttachment(ISecret, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecretTargetAttachmentProxy

    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        attribute:
        :attribute:: true
        """
        ...


class _ISecretTargetAttachmentProxy(jsii.proxy_for(ISecret)):
    __jsii_type__ = "@aws-cdk/aws-secretsmanager.ISecretTargetAttachment"
    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")


class RotationSchedule(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.RotationSchedule"):
    """A rotation schedule."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, secret: "ISecret", rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param secret: The secret to rotate.
        :param rotation_lambda: THe Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        """
        props = RotationScheduleProps(secret=secret, rotation_lambda=rotation_lambda, automatically_after=automatically_after)

        jsii.create(RotationSchedule, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleOptions", jsii_struct_bases=[], name_mapping={'rotation_lambda': 'rotationLambda', 'automatically_after': 'automaticallyAfter'})
class RotationScheduleOptions():
    def __init__(self, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after: typing.Optional[aws_cdk.core.Duration]=None):
        """Options to add a rotation schedule to a secret.

        :param rotation_lambda: THe Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        """
        self._values = {
            'rotation_lambda': rotation_lambda,
        }
        if automatically_after is not None: self._values["automatically_after"] = automatically_after

    @property
    def rotation_lambda(self) -> aws_cdk.aws_lambda.IFunction:
        """THe Lambda function that can rotate the secret."""
        return self._values.get('rotation_lambda')

    @property
    def automatically_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        default
        :default: Duration.days(30)
        """
        return self._values.get('automatically_after')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RotationScheduleOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.RotationScheduleProps", jsii_struct_bases=[RotationScheduleOptions], name_mapping={'rotation_lambda': 'rotationLambda', 'automatically_after': 'automaticallyAfter', 'secret': 'secret'})
class RotationScheduleProps(RotationScheduleOptions):
    def __init__(self, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after: typing.Optional[aws_cdk.core.Duration]=None, secret: "ISecret"):
        """Construction properties for a RotationSchedule.

        :param rotation_lambda: THe Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        :param secret: The secret to rotate.
        """
        self._values = {
            'rotation_lambda': rotation_lambda,
            'secret': secret,
        }
        if automatically_after is not None: self._values["automatically_after"] = automatically_after

    @property
    def rotation_lambda(self) -> aws_cdk.aws_lambda.IFunction:
        """THe Lambda function that can rotate the secret."""
        return self._values.get('rotation_lambda')

    @property
    def automatically_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        default
        :default: Duration.days(30)
        """
        return self._values.get('automatically_after')

    @property
    def secret(self) -> "ISecret":
        """The secret to rotate."""
        return self._values.get('secret')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RotationScheduleProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ISecret)
class Secret(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.Secret"):
    """Creates a new secret in AWS SecretsManager."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, generate_secret_string: typing.Optional["SecretStringGenerator"]=None, secret_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        """
        props = SecretProps(description=description, encryption_key=encryption_key, generate_secret_string=generate_secret_string, secret_name=secret_name)

        jsii.create(Secret, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretArn")
    @classmethod
    def from_secret_arn(cls, scope: aws_cdk.core.Construct, id: str, secret_arn: str) -> "ISecret":
        """
        :param scope: -
        :param id: -
        :param secret_arn: -
        """
        return jsii.sinvoke(cls, "fromSecretArn", [scope, id, secret_arn])

    @jsii.member(jsii_name="fromSecretAttributes")
    @classmethod
    def from_secret_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, secret_arn: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> "ISecret":
        """Import an existing secret into the Stack.

        :param scope: the scope of the import.
        :param id: the ID of the imported Secret in the construct tree.
        :param attrs: the attributes of the imported secret.
        :param secret_arn: The ARN of the secret in SecretsManager.
        :param encryption_key: The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.
        """
        attrs = SecretAttributes(secret_arn=secret_arn, encryption_key=encryption_key)

        return jsii.sinvoke(cls, "fromSecretAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param options: -
        :param rotation_lambda: THe Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        """
        options = RotationScheduleOptions(rotation_lambda=rotation_lambda, automatically_after=automatically_after)

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="addTargetAttachment")
    def add_target_attachment(self, id: str, *, target: "ISecretAttachmentTarget") -> "SecretTargetAttachment":
        """Adds a target attachment to the secret.

        :param id: -
        :param options: -
        :param target: The target to attach the secret to.

        return
        :return: an AttachedSecret
        """
        options = AttachedSecretOptions(target=target)

        return jsii.invoke(self, "addTargetAttachment", [id, options])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, json_field: str) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -
        """
        return jsii.invoke(self, "secretValueFromJson", [json_field])

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager."""
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``."""
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretAttachmentTargetProps", jsii_struct_bases=[], name_mapping={'target_id': 'targetId', 'target_type': 'targetType'})
class SecretAttachmentTargetProps():
    def __init__(self, *, target_id: str, target_type: "AttachmentTargetType"):
        """Attachment target specifications.

        :param target_id: The id of the target to attach the secret to.
        :param target_type: The type of the target to attach the secret to.
        """
        self._values = {
            'target_id': target_id,
            'target_type': target_type,
        }

    @property
    def target_id(self) -> str:
        """The id of the target to attach the secret to."""
        return self._values.get('target_id')

    @property
    def target_type(self) -> "AttachmentTargetType":
        """The type of the target to attach the secret to."""
        return self._values.get('target_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SecretAttachmentTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretAttributes", jsii_struct_bases=[], name_mapping={'secret_arn': 'secretArn', 'encryption_key': 'encryptionKey'})
class SecretAttributes():
    def __init__(self, *, secret_arn: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None):
        """Attributes required to import an existing secret into the Stack.

        :param secret_arn: The ARN of the secret in SecretsManager.
        :param encryption_key: The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used.
        """
        self._values = {
            'secret_arn': secret_arn,
        }
        if encryption_key is not None: self._values["encryption_key"] = encryption_key

    @property
    def secret_arn(self) -> str:
        """The ARN of the secret in SecretsManager."""
        return self._values.get('secret_arn')

    @property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The encryption key that is used to encrypt the secret, unless the default SecretsManager key is used."""
        return self._values.get('encryption_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SecretAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'encryption_key': 'encryptionKey', 'generate_secret_string': 'generateSecretString', 'secret_name': 'secretName'})
class SecretProps():
    def __init__(self, *, description: typing.Optional[str]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, generate_secret_string: typing.Optional["SecretStringGenerator"]=None, secret_name: typing.Optional[str]=None):
        """The properties required to create a new secret in AWS Secrets Manager.

        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        """
        if isinstance(generate_secret_string, dict): generate_secret_string = SecretStringGenerator(**generate_secret_string)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if generate_secret_string is not None: self._values["generate_secret_string"] = generate_secret_string
        if secret_name is not None: self._values["secret_name"] = secret_name

    @property
    def description(self) -> typing.Optional[str]:
        """An optional, human-friendly description of the secret.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key to use for encrypting the secret value.

        default
        :default: - A default KMS key for the account and region is used.
        """
        return self._values.get('encryption_key')

    @property
    def generate_secret_string(self) -> typing.Optional["SecretStringGenerator"]:
        """Configuration for how to generate a secret value.

        default
        :default:

        - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each
          category), per the default values of ``SecretStringGenerator``.
        """
        return self._values.get('generate_secret_string')

    @property
    def secret_name(self) -> typing.Optional[str]:
        """A name for the secret.

        Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to
        30 days blackout period. During that period, it is not possible to create another secret that shares the same name.

        default
        :default: - A name is generated by CloudFormation.
        """
        return self._values.get('secret_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SecretProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretStringGenerator", jsii_struct_bases=[], name_mapping={'exclude_characters': 'excludeCharacters', 'exclude_lowercase': 'excludeLowercase', 'exclude_numbers': 'excludeNumbers', 'exclude_punctuation': 'excludePunctuation', 'exclude_uppercase': 'excludeUppercase', 'generate_string_key': 'generateStringKey', 'include_space': 'includeSpace', 'password_length': 'passwordLength', 'require_each_included_type': 'requireEachIncludedType', 'secret_string_template': 'secretStringTemplate'})
class SecretStringGenerator():
    def __init__(self, *, exclude_characters: typing.Optional[str]=None, exclude_lowercase: typing.Optional[bool]=None, exclude_numbers: typing.Optional[bool]=None, exclude_punctuation: typing.Optional[bool]=None, exclude_uppercase: typing.Optional[bool]=None, generate_string_key: typing.Optional[str]=None, include_space: typing.Optional[bool]=None, password_length: typing.Optional[jsii.Number]=None, require_each_included_type: typing.Optional[bool]=None, secret_string_template: typing.Optional[str]=None):
        """Configuration to generate secrets such as passwords automatically.

        :param exclude_characters: A string that includes characters that shouldn't be included in the generated password. The string can be a minimum of ``0`` and a maximum of ``4096`` characters long. Default: no exclusions
        :param exclude_lowercase: Specifies that the generated password shouldn't include lowercase letters. Default: false
        :param exclude_numbers: Specifies that the generated password shouldn't include digits. Default: false
        :param exclude_punctuation: Specifies that the generated password shouldn't include punctuation characters. Default: false
        :param exclude_uppercase: Specifies that the generated password shouldn't include uppercase letters. Default: false
        :param generate_string_key: The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter. If you specify ``generateStringKey`` then ``secretStringTemplate`` must be also be specified.
        :param include_space: Specifies that the generated password can include the space character. Default: false
        :param password_length: The desired length of the generated password. Default: 32
        :param require_each_included_type: Specifies whether the generated password must include at least one of every allowed character type. Default: true
        :param secret_string_template: A properly structured JSON string that the generated password can be added to. The ``generateStringKey`` is combined with the generated random string and inserted into the JSON structure that's specified by this parameter. The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate`` then ``generateStringKey`` must be also be specified.
        """
        self._values = {
        }
        if exclude_characters is not None: self._values["exclude_characters"] = exclude_characters
        if exclude_lowercase is not None: self._values["exclude_lowercase"] = exclude_lowercase
        if exclude_numbers is not None: self._values["exclude_numbers"] = exclude_numbers
        if exclude_punctuation is not None: self._values["exclude_punctuation"] = exclude_punctuation
        if exclude_uppercase is not None: self._values["exclude_uppercase"] = exclude_uppercase
        if generate_string_key is not None: self._values["generate_string_key"] = generate_string_key
        if include_space is not None: self._values["include_space"] = include_space
        if password_length is not None: self._values["password_length"] = password_length
        if require_each_included_type is not None: self._values["require_each_included_type"] = require_each_included_type
        if secret_string_template is not None: self._values["secret_string_template"] = secret_string_template

    @property
    def exclude_characters(self) -> typing.Optional[str]:
        """A string that includes characters that shouldn't be included in the generated password.

        The string can be a minimum
        of ``0`` and a maximum of ``4096`` characters long.

        default
        :default: no exclusions
        """
        return self._values.get('exclude_characters')

    @property
    def exclude_lowercase(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include lowercase letters.

        default
        :default: false
        """
        return self._values.get('exclude_lowercase')

    @property
    def exclude_numbers(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include digits.

        default
        :default: false
        """
        return self._values.get('exclude_numbers')

    @property
    def exclude_punctuation(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include punctuation characters.

        default
        :default: false
        """
        return self._values.get('exclude_punctuation')

    @property
    def exclude_uppercase(self) -> typing.Optional[bool]:
        """Specifies that the generated password shouldn't include uppercase letters.

        default
        :default: false
        """
        return self._values.get('exclude_uppercase')

    @property
    def generate_string_key(self) -> typing.Optional[str]:
        """The JSON key name that's used to add the generated password to the JSON structure specified by the ``secretStringTemplate`` parameter.

        If you specify ``generateStringKey`` then ``secretStringTemplate``
        must be also be specified.
        """
        return self._values.get('generate_string_key')

    @property
    def include_space(self) -> typing.Optional[bool]:
        """Specifies that the generated password can include the space character.

        default
        :default: false
        """
        return self._values.get('include_space')

    @property
    def password_length(self) -> typing.Optional[jsii.Number]:
        """The desired length of the generated password.

        default
        :default: 32
        """
        return self._values.get('password_length')

    @property
    def require_each_included_type(self) -> typing.Optional[bool]:
        """Specifies whether the generated password must include at least one of every allowed character type.

        default
        :default: true
        """
        return self._values.get('require_each_included_type')

    @property
    def secret_string_template(self) -> typing.Optional[str]:
        """A properly structured JSON string that the generated password can be added to.

        The ``generateStringKey`` is
        combined with the generated random string and inserted into the JSON structure that's specified by this parameter.
        The merged JSON string is returned as the completed SecretString of the secret. If you specify ``secretStringTemplate``
        then ``generateStringKey`` must be also be specified.
        """
        return self._values.get('secret_string_template')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SecretStringGenerator(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ISecretTargetAttachment, ISecret)
class SecretTargetAttachment(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-secretsmanager.SecretTargetAttachment"):
    """An attached secret."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, secret: "ISecret", target: "ISecretAttachmentTarget") -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param secret: The secret to attach to the target.
        :param target: The target to attach the secret to.
        """
        props = SecretTargetAttachmentProps(secret=secret, target=target)

        jsii.create(SecretTargetAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecretTargetAttachmentSecretArn")
    @classmethod
    def from_secret_target_attachment_secret_arn(cls, scope: aws_cdk.core.Construct, id: str, secret_target_attachment_secret_arn: str) -> "ISecretTargetAttachment":
        """
        :param scope: -
        :param id: -
        :param secret_target_attachment_secret_arn: -
        """
        return jsii.sinvoke(cls, "fromSecretTargetAttachmentSecretArn", [scope, id, secret_target_attachment_secret_arn])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(self, id: str, *, rotation_lambda: aws_cdk.aws_lambda.IFunction, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> "RotationSchedule":
        """Adds a rotation schedule to the secret.

        :param id: -
        :param options: -
        :param rotation_lambda: THe Lambda function that can rotate the secret.
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)
        """
        options = RotationScheduleOptions(rotation_lambda=rotation_lambda, automatically_after=automatically_after)

        return jsii.invoke(self, "addRotationSchedule", [id, options])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable, version_stages: typing.Optional[typing.List[str]]=None) -> aws_cdk.aws_iam.Grant:
        """Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -
        """
        return jsii.invoke(self, "grantRead", [grantee, version_stages])

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(self, json_field: str) -> aws_cdk.core.SecretValue:
        """Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -
        """
        return jsii.invoke(self, "secretValueFromJson", [json_field])

    @property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> str:
        """The ARN of the secret in AWS Secrets Manager."""
        return jsii.get(self, "secretArn")

    @property
    @jsii.member(jsii_name="secretTargetAttachmentSecretArn")
    def secret_target_attachment_secret_arn(self) -> str:
        """Same as ``secretArn``.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "secretTargetAttachmentSecretArn")

    @property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> aws_cdk.core.SecretValue:
        """Retrieve the value of the stored secret as a ``SecretValue``."""
        return jsii.get(self, "secretValue")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        """
        return jsii.get(self, "encryptionKey")


@jsii.data_type(jsii_type="@aws-cdk/aws-secretsmanager.SecretTargetAttachmentProps", jsii_struct_bases=[AttachedSecretOptions], name_mapping={'target': 'target', 'secret': 'secret'})
class SecretTargetAttachmentProps(AttachedSecretOptions):
    def __init__(self, *, target: "ISecretAttachmentTarget", secret: "ISecret"):
        """Construction properties for an AttachedSecret.

        :param target: The target to attach the secret to.
        :param secret: The secret to attach to the target.
        """
        self._values = {
            'target': target,
            'secret': secret,
        }

    @property
    def target(self) -> "ISecretAttachmentTarget":
        """The target to attach the secret to."""
        return self._values.get('target')

    @property
    def secret(self) -> "ISecret":
        """The secret to attach to the target."""
        return self._values.get('secret')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SecretTargetAttachmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["AttachedSecretOptions", "AttachmentTargetType", "CfnResourcePolicy", "CfnResourcePolicyProps", "CfnRotationSchedule", "CfnRotationScheduleProps", "CfnSecret", "CfnSecretProps", "CfnSecretTargetAttachment", "CfnSecretTargetAttachmentProps", "ISecret", "ISecretAttachmentTarget", "ISecretTargetAttachment", "RotationSchedule", "RotationScheduleOptions", "RotationScheduleProps", "Secret", "SecretAttachmentTargetProps", "SecretAttributes", "SecretProps", "SecretStringGenerator", "SecretTargetAttachment", "SecretTargetAttachmentProps", "__jsii_assembly__"]

publication.publish()
