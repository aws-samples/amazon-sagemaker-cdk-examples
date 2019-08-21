import aws_cdk.cdk as cdk
import aws_cdk.core as core
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_lambda as serverless
import aws_cdk.aws_events as events
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3  as s3

from aws_cdk.aws_lambda_event_sources import *

import boto3 
import json

#USER VARIABLES
prefix = 'sagecdk'
my_region = boto3.session.Session().region_name
account_id = boto3.client('sts').get_caller_identity().get('Account')

class AutoModelDeploy(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)
        
        input_bucket = s3.Bucket(self, id='inputs')

        output_bucket = s3.Bucket(self, id='outputs')

        ## Permissions for SageMaker to access S3 buckets in account
        sagemaker_role = iam.Role(self, 'automodeldeploy-sagemaker-role', 
                assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'))
        sagemaker_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess'))
        sagemaker_role.add_to_policy(iam.PolicyStatement(
            resources=['arn:aws:s3:::*'],
            actions=['s3:GetObject', 
                    's3:PutObject', 
                    's3:DeleteObject', 
                    's3:ListBucket']))
        # Lambda Fn to create SageMaker endpoint when a new json file is uploaded
        # JSON specifies the details of the endpoint
        # TODO: consider using a zip package for this function if it grows > 4kB
        with open('lambda/deploy-model.py', encoding='utf8') as fp:
            lambda_code = fp.read()

        deploy_model_fn = serverless.Function(self,
                    id='deploy-model',
                    description='Creates SageMaker Endpoint based on S3 Object Trigger',
                    code=serverless.InlineCode(lambda_code),
                    handler='index.lambda_handler',
                    timeout=core.Duration.seconds(300),
                    runtime=serverless.Runtime.PYTHON_3_7,
                    environment={
                        'sagemaker_role': sagemaker_role.role_arn
                    })

        deploy_model_fn.add_to_role_policy(iam.PolicyStatement(
            actions=['sagemaker:CreateModel',
                    'sagemaker:DeleteModel',
                    'sagemaker:CreateEndpoint',
                    'sagemaker:DeleteEndpoint',
                    'sagemaker:DescribeEndpoint',
                    'sagemaker:CreateEndpointConfig',
                    'sagemaker:DeleteEndpointConfig'], 
            resources=['*']))

        # Allows Lambda function to pass role to SageMaker
        deploy_model_fn.add_to_role_policy(iam.PolicyStatement(
            actions=['iam:PassRole'], 
            resources=['*']))

        deploy_model_fn.add_event_source(S3EventSource(bucket=input_bucket, 
                    events=[s3.EventType.OBJECT_CREATED],
                    filters=[{
                        'suffix': 'json'
                    }]))

        input_bucket.grant_read_write(deploy_model_fn,'*')

        # Lambda that is triggered when Sagemaker endpoint status changes
        with open('lambda/check-status.py', encoding='utf8') as fp:
            lambda_code = fp.read()

        check_status_fn = serverless.Function(self,
                    id='check-status',
                    description='Checks on SageMaker Endpoint Status based on Cloudwatch Trigger',
                    code=serverless.InlineCode(lambda_code),
                    handler='index.lambda_handler',
                    timeout=core.Duration.seconds(300),
                    runtime=serverless.Runtime.PYTHON_3_7)
        

        # CloudWatch rule to trigger check status fn
        event_pattern = events.EventPattern(source=['aws.sagemaker'],
            detail_type=['SageMaker Endpoint State Change'])

        rule = events.Rule(self, 'sagemaker-endpoint-state',
                description='Detects when SageMaker Endpoint State Changes', 
                enabled=True, 
                event_pattern=event_pattern)
        
        rule.add_target(targets.LambdaFunction(check_status_fn))

app = core.App()
AutoModelDeploy(app, 'AutoModelDeploy')
app.synth()