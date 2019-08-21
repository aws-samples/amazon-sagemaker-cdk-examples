import json
import boto3
from botocore.vendored import requests
import os
import datetime

#USER VARIABLES
timenow = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
max_depth = os.environ['max_depth']
container = os.environ['container']
base_name = os.environ['base_name']
role_arn = os.environ['role_arn']
s3_input_train = os.environ['s3_input']
s3_input_validation = os.environ['s3_input_validation']
s3_output = os.environ['s3_output']

def run_training():
    response = client.create_training_job(
    TrainingJobName='videogames-xgboost-'+timenow,
    HyperParameters={
        'max_depth': max_depth
    },
    AlgorithmSpecification={
        'TrainingImage': container,
        'TrainingInputMode': 'File',
    },
    RoleArn=role_arn,
    InputDataConfig=[
        {
            'ChannelName': 'train',
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': s3_input_train,
                    'S3DataDistributionType': 'FullyReplicated',
                }
            },
            'ContentType': 'libsvm',
            'CompressionType': 'None',
            'InputMode': 'File',
        },
        {
            'ChannelName': 'validation',
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': s3_input_validation,
                    'S3DataDistributionType': 'FullyReplicated',
                }
            },
            'ContentType': 'libsvm',
            'CompressionType': 'None',
            'InputMode': 'File',
        },
    ],
    OutputDataConfig={
        'S3OutputPath': s3_output
    },
    StoppingCondition={
        'MaxRuntimeInSeconds': 3000
    },
    ResourceConfig={
        'InstanceType': 'ml.m4.xlarge',
        'InstanceCount': 1,
        'VolumeSizeInGB': 3,
    },
    Tags=[
        {
            'Key': 'Training Time',
            'Value': timenow
        },
        {
            'Key': 'Max depth used',
            'Value': max_depth
        },
    ])

    print(response)


def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('sagemaker-runtime')
    
    print("Calling Sagemaker endpoint")

    try:
        run_training()
    except Exception as e:
        print("something went wrong ...")
        print(e)
    
    return {
        'statusCode': 200,
        'body': json.loads(response['Body'].read())
    }
