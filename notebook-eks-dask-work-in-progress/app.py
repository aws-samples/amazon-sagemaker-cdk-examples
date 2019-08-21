from aws_cdk import (
    aws_iam as iam_,
    aws_eks as eks_,
    aws_sagemaker as sagemaker_,
    cdk,
    core)

import boto3 
import base64

my_region = boto3.session.Session().region_name

ec2client = boto3.client('ec2')
smclient = boto3.client('sagemaker')

#USER VARIABLES
default_vpc = [x['VpcId'] for x in ec2client.describe_vpcs()['Vpcs'] if x['IsDefault']][0]
default_sg = [x['GroupId'] for x in ec2client.describe_security_groups(Filters=[{'Name':'vpc-id','Values':[default_vpc,]},])['SecurityGroups'] if x['GroupName']=='default']
default_subnet = [x['SubnetId'] for x in ec2client.describe_subnets(Filters=[{'Name':'vpc-id','Values':[default_vpc,]},])['Subnets'] if x['DefaultForAz']][0]
num_instances = 1
#LifecycleScriptStr = open("lifecyclescript.sh", "r").read()
#LifeCycleConfigName = "CDKLifeCycleConfig"
#--------------


class SMNotebookEKSdask(core.Stack):

    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)


        #Create role for Notebook instance
        nRole = iam_.Role(
            self,
            "notebookAccessRole",
            assumed_by = iam_.ServicePrincipal('sagemaker'))
        
        nPolicy = iam_.Policy(
            self,
            "notebookAccessPolicy",
            policy_name = "notebookAccessPolicy",
            statements = [iam_.PolicyStatement(actions = ['s3:*',], resources=['*',]),]).attach_to_role(nRole)

        #Create notebook instances cluster
        instances = []

        for i in range(num_instances):
            nid = 'Imday-Notebook-Instance-' 
            instances.append(sagemaker_.CfnNotebookInstance(
                self,
                nid,
                instance_type = 'ml.t2.medium',
                volume_size_in_gb = 5,
                security_group_ids = default_sg,
                subnet_id = default_subnet,
                notebook_instance_name = nid,
                role_arn = nRole.role_arn,
                ))


app = core.App()
SMNotebookEKSdask(app, "SMNotebookEKSdask")

app.synth()
