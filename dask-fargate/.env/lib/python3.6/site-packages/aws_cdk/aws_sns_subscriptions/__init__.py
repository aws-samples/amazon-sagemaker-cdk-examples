"""
# CDK Construct Library for Amazon Simple Notification Service Subscriptions

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library provides constructs for adding subscriptions to an Amazon SNS topic.
Subscriptions can be added by calling the `.addSubscription(...)` method on the topic.

## Subscriptions

Subscriptions can be added to the following endpoints:

* HTTPS
* Amazon SQS
* AWS Lambda
* Email

Create an Amazon SNS Topic to add subscriptions.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns as sns

my_topic = sns.Topic(self, "MyTopic")
```

### HTTPS

Add an HTTPS Subscription to your topic:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns_subscriptions as subscriptions

my_topic.add_subscription(subsscriptions.UrlSubscription("https://foobar.com/"))
```

### Amazon SQS

Subscribe a queue to your topic:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_sns_subscriptions as subscriptions

my_queue = sqs.Queue(self, "MyQueue")

my_topic.add_subscription(subsscriptions.SqsSubscription(queue))
```

Note that subscriptions of queues in different accounts need to be manually confirmed by
reading the initial message from the queue and visiting the link found in it.

### AWS Lambda

Subscribe an AWS Lambda function to your topic:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda
import aws_cdk.aws_sns_subscriptions as subscriptions

my_function = lambda.Function(self, "Echo",
    handler="index.handler",
    runtime=lambda.Runtime.NODEJS_10_X,
    code=lambda.Code.from_inline(f"exports.handler = {handler.toString()}")
)

my_topic.add_subscription(subscriptions.LambdaSubscription(my_function))
```

### Email

Subscribe an email address to your topic:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns_subscriptions as subscriptions

my_topic.add_subscription(subscriptions.EmailSubscription("foo@bar.com"))
```

Note that email subscriptions require confirmation by visiting the link sent to the
email address.
"""
import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sns-subscriptions", "1.18.0", __name__, "aws-sns-subscriptions@1.18.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_sns.ITopicSubscription)
class EmailSubscription(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns-subscriptions.EmailSubscription"):
    """Use an email address as a subscription target.

    Email subscriptions require confirmation.
    """
    def __init__(self, email_address: str, *, json: typing.Optional[bool]=None, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None) -> None:
        """
        :param email_address: -
        :param props: -
        :param json: Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)
        :param filter_policy: The filter policy. Default: - all messages are delivered
        """
        props = EmailSubscriptionProps(json=json, filter_policy=filter_policy)

        jsii.create(EmailSubscription, self, [email_address, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: aws_cdk.aws_sns.ITopic) -> aws_cdk.aws_sns.TopicSubscriptionConfig:
        """
        :param _topic: -
        """
        return jsii.invoke(self, "bind", [_topic])


@jsii.implements(aws_cdk.aws_sns.ITopicSubscription)
class LambdaSubscription(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns-subscriptions.LambdaSubscription"):
    """Use a Lambda function as a subscription target."""
    def __init__(self, fn: aws_cdk.aws_lambda.IFunction, *, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None) -> None:
        """
        :param fn: -
        :param props: -
        :param filter_policy: The filter policy. Default: - all messages are delivered
        """
        props = LambdaSubscriptionProps(filter_policy=filter_policy)

        jsii.create(LambdaSubscription, self, [fn, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: aws_cdk.aws_sns.ITopic) -> aws_cdk.aws_sns.TopicSubscriptionConfig:
        """
        :param topic: -
        """
        return jsii.invoke(self, "bind", [topic])


@jsii.implements(aws_cdk.aws_sns.ITopicSubscription)
class SqsSubscription(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns-subscriptions.SqsSubscription"):
    """Use an SQS queue as a subscription target."""
    def __init__(self, queue: aws_cdk.aws_sqs.IQueue, *, raw_message_delivery: typing.Optional[bool]=None, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None) -> None:
        """
        :param queue: -
        :param props: -
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param filter_policy: The filter policy. Default: - all messages are delivered
        """
        props = SqsSubscriptionProps(raw_message_delivery=raw_message_delivery, filter_policy=filter_policy)

        jsii.create(SqsSubscription, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: aws_cdk.aws_sns.ITopic) -> aws_cdk.aws_sns.TopicSubscriptionConfig:
        """
        :param topic: -
        """
        return jsii.invoke(self, "bind", [topic])


@jsii.data_type(jsii_type="@aws-cdk/aws-sns-subscriptions.SubscriptionProps", jsii_struct_bases=[], name_mapping={'filter_policy': 'filterPolicy'})
class SubscriptionProps():
    def __init__(self, *, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None):
        """
        :param filter_policy: The filter policy. Default: - all messages are delivered
        """
        self._values = {
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy

    @property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns-subscriptions.EmailSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'filter_policy': 'filterPolicy', 'json': 'json'})
class EmailSubscriptionProps(SubscriptionProps):
    def __init__(self, *, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None, json: typing.Optional[bool]=None):
        """Options for email subscriptions.

        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param json: Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)
        """
        self._values = {
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if json is not None: self._values["json"] = json

    @property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    @property
    def json(self) -> typing.Optional[bool]:
        """Indicates if the full notification JSON should be sent to the email address or just the message text.

        default
        :default: false (Message text)
        """
        return self._values.get('json')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmailSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns-subscriptions.LambdaSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'filter_policy': 'filterPolicy'})
class LambdaSubscriptionProps(SubscriptionProps):
    def __init__(self, *, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None):
        """Properties for a Lambda subscription.

        :param filter_policy: The filter policy. Default: - all messages are delivered
        """
        self._values = {
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy

    @property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sns-subscriptions.SqsSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'filter_policy': 'filterPolicy', 'raw_message_delivery': 'rawMessageDelivery'})
class SqsSubscriptionProps(SubscriptionProps):
    def __init__(self, *, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None, raw_message_delivery: typing.Optional[bool]=None):
        """Properties for an SQS subscription.

        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        """
        self._values = {
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery

    @property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    @property
    def raw_message_delivery(self) -> typing.Optional[bool]:
        """The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        default
        :default: false
        """
        return self._values.get('raw_message_delivery')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_sns.ITopicSubscription)
class UrlSubscription(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns-subscriptions.UrlSubscription"):
    """Use a URL as a subscription target.

    The message will be POSTed to the given URL.

    see
    :see: https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html
    """
    def __init__(self, url: str, *, protocol: typing.Optional[aws_cdk.aws_sns.SubscriptionProtocol]=None, raw_message_delivery: typing.Optional[bool]=None, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None) -> None:
        """
        :param url: -
        :param props: -
        :param protocol: The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param filter_policy: The filter policy. Default: - all messages are delivered
        """
        props = UrlSubscriptionProps(protocol=protocol, raw_message_delivery=raw_message_delivery, filter_policy=filter_policy)

        jsii.create(UrlSubscription, self, [url, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: aws_cdk.aws_sns.ITopic) -> aws_cdk.aws_sns.TopicSubscriptionConfig:
        """
        :param _topic: -
        """
        return jsii.invoke(self, "bind", [_topic])


@jsii.data_type(jsii_type="@aws-cdk/aws-sns-subscriptions.UrlSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'filter_policy': 'filterPolicy', 'protocol': 'protocol', 'raw_message_delivery': 'rawMessageDelivery'})
class UrlSubscriptionProps(SubscriptionProps):
    def __init__(self, *, filter_policy: typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]=None, protocol: typing.Optional[aws_cdk.aws_sns.SubscriptionProtocol]=None, raw_message_delivery: typing.Optional[bool]=None):
        """Options for URL subscriptions.

        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param protocol: The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        """
        self._values = {
        }
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if protocol is not None: self._values["protocol"] = protocol
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery

    @property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_sns.SubscriptionFilter]]:
        """The filter policy.

        default
        :default: - all messages are delivered
        """
        return self._values.get('filter_policy')

    @property
    def protocol(self) -> typing.Optional[aws_cdk.aws_sns.SubscriptionProtocol]:
        """The subscription's protocol.

        default
        :default: - Protocol is derived from url
        """
        return self._values.get('protocol')

    @property
    def raw_message_delivery(self) -> typing.Optional[bool]:
        """The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        default
        :default: false
        """
        return self._values.get('raw_message_delivery')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UrlSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["EmailSubscription", "EmailSubscriptionProps", "LambdaSubscription", "LambdaSubscriptionProps", "SqsSubscription", "SqsSubscriptionProps", "SubscriptionProps", "UrlSubscription", "UrlSubscriptionProps", "__jsii_assembly__"]

publication.publish()
