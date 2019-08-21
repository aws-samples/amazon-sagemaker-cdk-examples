from aws_cdk import aws_events as events, aws_lambda as lambda_, cdk, aws_events_targets as targets
from aws_cdk import aws_iam, core
from aws_cdk import aws_apigateway as apig_
import boto3 

my_region = boto3.session.Session().region_name
endpoint_name = "vehicle-damage-inspection-endpoint"
my_acc_id = boto3.client('sts').get_caller_identity().get('Account')

class APILambdaSagemaker(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFn = lambda_.Function(
            self,
            "callsmlambda",
            code=lambda_.InlineCode(handler_code),
            handler="index.lambda_handler",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment={"endpoint_name":endpoint_name, # CHANGE TO YOUR ENDPOINT NAME!!
                        "content_type":"text/csv"}
        )

        lambdaFn.add_to_role_policy(aws_iam.PolicyStatement(actions=['sagemaker:InvokeEndpoint',],
            resources = ['arn:aws:sagemaker:{}:{}:endpoint/{}'.format(my_region,my_acc_id,endpoint_name),]))


        api = apig_.LambdaRestApi(self,"callsmapi",proxy=True,handler=lambdaFn)
        print(api)


app = core.App()
APILambdaSagemaker(app, "APILambdaSagemaker")
app.synth()
