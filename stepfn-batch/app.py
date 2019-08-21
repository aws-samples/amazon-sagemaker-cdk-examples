#!/usr/bin/env python3
from aws_cdk import (
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    cdk,
    aws_lambda as lambda_,
    aws_iam,
    core
)

import boto3 
my_region = boto3.session.Session().region_name

my_acc_id = boto3.client('sts').get_caller_identity().get('Account')

#USER VARIABLES
transform_job_name = 'xgboost-batch-transform'
model_name = 'xgboost-2019-06-18-19-03-13-823'
max_concurrent='10'
max_payload_size=str(int(100/int(max_concurrent))) #Maximum concurrent transforms * maximum payload can't exceed 100 MB
s3_uri_in='s3://sagemaker-us-east-1-497456752804/in/test.libsvm'
s3_uri_out='s3://sagemaker-us-east-1-497456752804/out/'
instance_type= 'ml.m4.xlarge'
instance_count='2'

#---------------


class SMbatchInference(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create both lambdas

        with open("lambda-submit.py", encoding="utf8") as fp:
            lambda_submit_code = fp.read()

        lambdaFn1 = lambda_.Function(
            self,
            "submitsmbatch",
            code=lambda_.InlineCode(lambda_submit_code),
            handler="index.lambda_handler",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment={
            "transform_job_name":transform_job_name,
            "model_name":model_name,
            "max_concurrent":max_concurrent,
            "max_payload_size":max_payload_size,
            "s3_uri_in":s3_uri_in,
            "s3_uri_out":s3_uri_out,
            "instance_type":instance_type,
            "instance_count":instance_count,
            }
        )

        # Add perms
        lambdaFn1.add_to_role_policy(aws_iam.PolicyStatement(
            actions = ['sagemaker:CreateTransformJob',],
            resources = ['arn:aws:sagemaker:{}:{}:transform-job/{}*'.format(my_region,my_acc_id,transform_job_name),]
            ))

       
        with open("lambda-check.py", encoding="utf8") as fp:
            lambda_check_code = fp.read()

        lambdaFn2 = lambda_.Function(
            self,
            "checksmbatch",
            code=lambda_.InlineCode(lambda_check_code),
            handler="index.lambda_handler",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment={"model_name":model_name, # CHANGE TO YOUR ENDPOINT NAME!!
                        "content_type":"text/csv"}
        )
        # Add perms
        lambdaFn2.add_to_role_policy(aws_iam.PolicyStatement(
            actions = ['sagemaker:DescribeTransformJob',],
            resources = ['arn:aws:sagemaker:{}:{}:transform-job/{}*'.format(my_region,my_acc_id,transform_job_name),]
            ))
        # Define state machine

        # submit_job_activity = sfn.Activity(
        #     self, "SubmitJob"
        # )
        # check_job_activity = sfn.Activity(
        #     self, "CheckJob"
        # )

        submit_job = sfn.Task(
            self, "Submit Job",
            task=sfn_tasks.InvokeFunction(lambdaFn1),
        )

        wait_x = sfn.Wait(
            self, "Wait 1 minute",
            time=sfn.WaitTime.duration(core.Duration.minutes(1)),
        )
        get_status = sfn.Task(
            self, "Get Job Status",
            task=sfn_tasks.InvokeFunction(lambdaFn2),
        )
        is_complete = sfn.Choice(
            self, "Job Complete?"
        )
        job_failed = sfn.Fail(
            self, "Job Failed",
            cause="AWS Batch Job Failed",
            error="DescribeJob returned FAILED"
        )
        final_status = sfn.Task(
            self, "Get Final Job Status",
            task=sfn_tasks.InvokeFunction(lambdaFn2),
        )

        definition = submit_job\
            .next(wait_x)\
            .next(get_status)\
            .next(is_complete
                  .when(sfn.Condition.string_equals(
                      "$.status", "Failed"), job_failed)
                  .when(sfn.Condition.string_equals(
                      "$.status", "Completed"), final_status)
                  .otherwise(wait_x))

        sfn.StateMachine(
            self, "SMbatchInference",
            definition=definition,
        )

app = core.App()
SMbatchInference(app, "SM-batch-Inference")
app.synth()
