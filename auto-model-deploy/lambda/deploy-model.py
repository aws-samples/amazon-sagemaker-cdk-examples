import json
import boto3
from botocore.vendored import requests
import os
import datetime

import time
from botocore.exceptions import ClientError

sagemaker_role = os.environ['sagemaker_role']

class InputException(Exception): pass

def valid_json(input_json):
    def valid_str(input_str):
        return (input_str is not None and input_str.strip() != '')
    
    if not valid_str(input_json['model_name']):
        raise InputException('model_name')
    if not valid_str(input_json['version']):
        raise InputException('version')
    
    containers_def = input_json['containers']
    if (not containers_def or len(containers_def) < 1):
        raise InputException('containers')
    for c in containers_def:
        if not valid_str(c['Image']):
            raise InputException('containers')
    
    return True

def deploy_model(config):
    model_name = '{}-{}'.format(config['model_name'], config['version'].replace('.','-'))
    sagemaker = boto3.client('sagemaker')
    try:
        res = sagemaker.delete_model(ModelName=model_name)
    except ClientError as e:
        if (e.response['Error']['Code'] == 'ValidationException'):
            pass
        else:
            raise(e)
    
    tags = []
    for key in config['tags']:
        tags.append({
            'Key': key,
            'Value': config['tags'][key] 
        })
    
    if len(config['containers']) < 2:
        res = sagemaker.create_model(ModelName=model_name, 
                                    PrimaryContainer=config['containers'][0], 
                                    ExecutionRoleArn=sagemaker_role,
                                    Tags=tags)
    else:
        res = sagemaker.create_model(ModelName=model_name, 
                                    Containers=config['containers'],
                                    ExecutionRoleArn=sagemaker_role,
                                    Tags=tags)
    print('Create Model:', res)

    # Determine what to do based on the stage tags
    if (config['tags']['stage'] == 'test'):
        # Kick off any testing here
        print('Try kicking off some testing here')
        return res

    if (config['tags']['stage'] != 'production'):
        print('This model is not tagged as production, will not deploy')
        return res

    def mod_variant_info(item, model_name=model_name):
        item['ModelName'] = model_name
        item['VariantName'] = model_name + '-' + item['InstanceType'].replace('.','-')
        return item

    config['endpoint']['config']['variants'] = list(map(mod_variant_info, 
                                                        config['endpoint']['config']['variants']))

    try:
        sagemaker.delete_endpoint_config(EndpointConfigName=model_name)
    except ClientError as e:
        if (e.response['Error']['Code'] == 'ValidationException'):
            pass
        else:
            raise(e)

    res = sagemaker.create_endpoint_config(EndpointConfigName=model_name,
                ProductionVariants=config['endpoint']['config']['variants'],
                Tags=tags)
    print('Create Endpoint Config:', res)

    try:
        sagemaker.delete_endpoint(EndpointName=model_name)
        while True:
            res = sagemaker.describe_endpoint(EndpointName=model_name)
            if (res['EndpointStatus'] != 'Deleting'):
                break
            time.sleep(1)
    except ClientError as e:
        if (e.response['Error']['Code'] == 'ValidationException'):
            pass
        else:
            raise(e)
    
    res = sagemaker.create_endpoint(EndpointName=model_name, 
                          EndpointConfigName=model_name,
                          Tags=tags)
    
    print('Created Endpoint:', res)
    return res

def lambda_handler(event, context):
    print(event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    inputKey = event['Records'][0]['s3']['object']['key']

    # Read JSON
    s3 = boto3.client('s3')

    config = s3.get_object(Bucket=bucket, Key=inputKey)
    config = json.loads(config['Body'].read())
    print(config)

    # Check that JSON has appropriate fields
    if not valid_json(config):
        return False

    res = deploy_model(config)
    
    return res