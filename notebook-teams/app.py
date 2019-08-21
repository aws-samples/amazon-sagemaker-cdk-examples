from aws_cdk import (
    aws_iam as iam_,
    aws_efs as efs_,
    aws_sagemaker as sagemaker_,
    cdk,
    core)

import boto3 
import base64

my_region = boto3.session.Session().region_name
my_acc_id = boto3.client('sts').get_caller_identity().get('Account')

ec2client = boto3.client('ec2')
smclient = boto3.client('sagemaker')

#USER VARIABLES
default_vpc = [x['VpcId'] for x in ec2client.describe_vpcs()['Vpcs'] if x['IsDefault']][0]
default_sg = [x['GroupId'] for x in ec2client.describe_security_groups(Filters=[{'Name':'vpc-id','Values':[default_vpc,]},])['SecurityGroups'] if x['GroupName']=='default']
default_subnet = [x['SubnetId'] for x in ec2client.describe_subnets(Filters=[{'Name':'vpc-id','Values':[default_vpc,]},])['Subnets'] if x['DefaultForAz']][0]
num_instances = 2
LifecycleScriptStr = open("lifecyclescript.sh", "r").read()
LifeCycleConfigName = "CDKLifeCycleConfig"
#--------------


class Notebooks4Teams(core.Stack):

    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        #Create mount instance
        efs = efs_.CfnFileSystem(
            self,
            "commonEFS4Notebooks",
            encrypted=False,
            performance_mode='generalPurpose',
            throughput_mode='bursting')

        print(efs.ref)
        #Create mount target
        mount = efs_.CfnMountTarget(
            self,
            "MountID",
            file_system_id=efs.ref,
            security_groups=default_sg,
            subnet_id=default_subnet,
            )

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
        print(mount.get_att('attr_ip_address').to_string())
        encodedScript = LifecycleScriptStr.format(efs.ref)

        print("Adding following script to the lifecycle config..\n___\n\n"+encodedScript)

        code = [
            {"content": core.Fn.base64(encodedScript)}
        ]

        lifecycleconfig = sagemaker_.CfnNotebookInstanceLifecycleConfig(
            self,
            LifeCycleConfigName,
            notebook_instance_lifecycle_config_name=LifeCycleConfigName,
            on_create=None, on_start=code)

        for i in range(num_instances):
            nid = 'CDK-Notebook-Instance-User-'+str(i) 
            instances.append(sagemaker_.CfnNotebookInstance(
                self,
                nid,
                instance_type = 'ml.t2.medium',
                volume_size_in_gb = 5,
                security_group_ids = default_sg,
                subnet_id = default_subnet,
                notebook_instance_name = nid,
                role_arn = nRole.role_arn,
                lifecycle_config_name = LifeCycleConfigName,
                ))


app = core.App()
Notebooks4Teams(app, "Notebooks4Teams")

app.synth()
