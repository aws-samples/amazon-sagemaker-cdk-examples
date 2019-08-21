import json
import boto3
from botocore.vendored import requests
import os
import datetime

from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print(event)
    # Insert your own code here to handle Sagemaker status changes
    return event