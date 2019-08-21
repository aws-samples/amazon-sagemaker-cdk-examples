import json
import boto3
from botocore.vendored import requests
import os

def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('sagemaker')
    
    response = client.describe_transform_job(TransformJobName=event["name"])
    
    print(response)
  
    return {
        'status': response["TransformJobStatus"],
        'name': event["name"]
    }
