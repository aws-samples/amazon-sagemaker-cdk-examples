import json
import boto3
from botocore.vendored import requests
import os

def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('sagemaker-runtime')
    
    print("Calling Sagemaker endpoint")

    response = client.invoke_endpoint(
        EndpointName=os.environ['endpoint_name'],
        Body=json.loads(event['body'])['data'],
        ContentType=os.environ['content_type'])
    
    return {
        'statusCode': 200,
        'body': json.loads(response['Body'].read())
    }
