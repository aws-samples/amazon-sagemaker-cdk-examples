from aws_cdk import aws_events as events, aws_lambda as lambda_, cdk, aws_events_targets as targets
from aws_cdk import aws_iam, core
from aws_cdk import aws_kinesis as kinesis_
from aws_cdk import aws_lambda_event_sources
import boto3 
my_region = boto3.session.Session().region_name
endpoint_name = "DEMO-videogames-xgboost-2019-06-18-18-58-35-771"
my_acc_id = boto3.client('sts').get_caller_identity().get('Account')
input_data = "s3://sagemaker-us-east-1-497456752804/in/test.libsvm"
bucket = 'sagemaker-us-east-1-497456752804'
key = 'in/test.libsvm'

class KinesisSagemakerInference(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        Kstream = kinesis_.Stream(
            self,
            "KinesisSagemakerInference",
            encryption=None,
            encryption_key=None,
            retention_period_hours=24,
            shard_count=1)
        

        lambdaFn = lambda_.Function(
            self,
            "KinesisSMLambda",
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

        lambdaFn.add_to_role_policy(aws_iam.PolicyStatement(
            actions = ['sagemaker:InvokeEndpoint',],
            resources = ['arn:aws:sagemaker:{}:{}:endpoint/{}'.format(my_region,my_acc_id,endpoint_name),]))


        # Add the Kinesis stream as Lambda source
        lambdaFn.add_event_source(aws_lambda_event_sources.KinesisEventSource(Kstream, starting_position=lambda_.StartingPosition.LATEST))
        
        # Add stream read permissions
        Kstream.grant_read(lambdaFn.role)



app = core.App()
KinesisSagemakerInference(app, "KinesisSagemakerInference")
app.synth()
