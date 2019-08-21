from aws_cdk import aws_events as events, aws_lambda as lambda_, cdk, aws_events_targets as targets, core
from aws_cdk import aws_iam
import boto3 
from sagemaker.amazon.amazon_estimator import get_image_uri

#USER VARIABLES
my_region = boto3.session.Session().region_name
base_name = "video-game-xgboost"
my_acc_id = boto3.client('sts').get_caller_identity().get('Account')
role_arn = 'arn:aws:iam::497456752804:role/service-role/AmazonSageMaker-ExecutionRole-20180629T142561'
s3_input_train = 's3://sagemaker-us-east-1-497456752804/sagemaker/videogames-xgboost/train'
s3_input_validation = 's3://sagemaker-us-east-1-497456752804/sagemaker/videogames-xgboost/validation'
s3_output = 's3://sagemaker-us-east-1-497456752804/sagemaker/videogames-xgboost/output'
#Algo hyperparams
max_depth = '5'
container = get_image_uri('us-east-1', 'xgboost')

class LambdaCronSagemakerTrain(core.Stack):
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
            environment={"base_name":base_name, 
                        "max_depth":max_depth,
                        "container":container,
                        "role_arn":role_arn,
                        "s3_input_train":s3_input_train,
                        "s3_input_validation":s3_input_validation,
                        "s3_output":s3_output}
                        )

        lambdaFn.add_to_role_policy(aws_iam.PolicyStatement(actions = ['sagemaker:CreateTrainingJob',],
        	resources=[role_arn,]))


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
LambdaCronSagemakerTrain(app, "LambdaCronSagemakerTrain")
app.synth()