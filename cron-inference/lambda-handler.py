import json
import boto3
from botocore.vendored import requests
import os

def lambda_handler(event, context):
    # TODO implement
    
    client_sm = boto3.client('sagemaker-runtime')
    client_s3 = boto3.client('s3')

    print("Getting test data")
    obj = client_s3.get_object(Bucket=os.environ['bucket'], Key=os.environ['key'])
    
    print("Calling Sagemaker endpoint")
    response = client.invoke_endpoint(
        EndpointName=os.environ['endpoint_name'],
        Body=os.environ['input_data'],
        ContentType=obj['Body'].read())
    
    return {
        'statusCode': 200,
        'body': json.loads(response['Body'].read())
    }
