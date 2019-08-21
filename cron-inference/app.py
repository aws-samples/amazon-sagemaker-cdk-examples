from aws_cdk import aws_events as events, aws_lambda as lambda_, cdk, aws_events_targets as targets, core
from aws_cdk import aws_iam
import boto3 
my_region = boto3.session.Session().region_name
endpoint_name = "DEMO-videogames-xgboost-2019-06-18-18-58-35-771"
my_acc_id = boto3.client('sts').get_caller_identity().get('Account')
input_data = "s3://sagemaker-us-east-1-497456752804/in/test.libsvm"
bucket = 'sagemaker-us-east-1-497456752804'
key = 'in/test.libsvm'
class LambdaCronSagemakerInference(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFn = lambda_.Function(
            self,
            "Singleton",
            code=lambda_.InlineCode(handler_code),
            handler="index.lambda_handler",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment={"endpoint_name":endpoint_name, # CHANGE TO YOUR ENDPOINT NAME!!
                        "content_type":"text/csv",
                        "input_data":input_data,
                        "bucket":bucket,
                        "key":key}
        )

        # Add sagemaker role
        lambdaFn.add_to_role_policy(aws_iam.PolicyStatement(
            actions = ['sagemaker:InvokeEndpoint',],
            resources = ['arn:aws:sagemaker:{}:{}:endpoint/{}'.format(my_region,my_acc_id,endpoint_name),]))

        #Add s3 role
        lambdaFn.add_to_role_policy(aws_iam.PolicyStatement(
            actions = ['s3:GetObject',],
            resources =['arn:aws:s3:::{}'.format(bucket),]))


        # Run every day at 6PM UTC
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))




app = core.App()
LambdaCronSagemakerInference(app, "LambdaCronSagemakerInference")
app.synth()
