import json
import boto3
from botocore.vendored import requests
import os
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('sagemaker')

    print("Calling Sagemaker batch transform")

    try:

        apptime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        response = client.create_transform_job(
        TransformJobName=os.environ['transform_job_name']+apptime,
        ModelName=os.environ['model_name'],
        MaxConcurrentTransforms=int(os.environ['max_concurrent']),
        MaxPayloadInMB=int(os.environ['max_payload_size']),
        BatchStrategy='MultiRecord',
        TransformInput={
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': os.environ['s3_uri_in']
                }
            },
            'ContentType': 'text/libsvm',
            'CompressionType': 'None',
            'SplitType': 'None'
        },
        TransformOutput={
            'S3OutputPath': os.environ['s3_uri_out'],
        },
        TransformResources={
            'InstanceType': os.environ['instance_type'],#|'ml.m4.2xlarge'|'ml.m4.4xlarge'|'ml.m4.10xlarge'|'ml.m4.16xlarge'|'ml.c4.xlarge'|'ml.c4.2xlarge'|'ml.c4.4xlarge'|'ml.c4.8xlarge'|'ml.p2.xlarge'|'ml.p2.8xlarge'|'ml.p2.16xlarge'|'ml.p3.2xlarge'|'ml.p3.8xlarge'|'ml.p3.16xlarge'|'ml.c5.xlarge'|'ml.c5.2xlarge'|'ml.c5.4xlarge'|'ml.c5.9xlarge'|'ml.c5.18xlarge'|'ml.m5.large'|'ml.m5.xlarge'|'ml.m5.2xlarge'|'ml.m5.4xlarge'|'ml.m5.12xlarge'|'ml.m5.24xlarge',
            'InstanceCount': int(os.environ['instance_count'])
        },)


        print(response)

        res = {'status':"Completed", "name":os.environ['transform_job_name']+apptime}

    except Exception as e:

        res = {'status':"Failed", "name":os.environ['transform_job_name']+apptime}
        print(e)
    # response = client.invoke_endpoint(
    #     EndpointName=os.environ['endpoint_name'],
    #     Body=event['data'],
    #     ContentType=os.environ['content_type'])
    
    return res
