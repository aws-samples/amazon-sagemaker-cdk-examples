from aws_cdk import core
from aws_cdk import (aws_ec2 as ec2, aws_sagemaker as sm, aws_efs as efs, aws_iam as iam_)

num_instances = 3
LifecycleScriptStr = open("lifecyclescript.sh", "r").read()
LifeCycleConfigName = "CDKLifeCycleConfig"

class MultinotebookefsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # VPC
        self.vpc = ec2.Vpc(self, "VPC",
                   max_azs=2,
                   cidr="10.10.0.0/16",
                   subnet_configuration=[ec2.SubnetConfiguration(
                       subnet_type=ec2.SubnetType.PUBLIC,
                       name="Public",
                       cidr_mask=24
                   ), ec2.SubnetConfiguration(
                       subnet_type=ec2.SubnetType.PRIVATE,
                       name="Private",
                       cidr_mask=24
                   )
                   ],
                   nat_gateways=1
                   )
        
        # Security group
        # self.sg = ec2.SecurityGroup(self, "securityGroup", self.vpc)
        self.sg = ec2.SecurityGroup.from_security_group_id(self, "securityGroup", self.vpc.vpc_default_security_group,mutable=False)

                   
        # Create EFS inside VPC
        self.efs = efs.FileSystem(
            self,
            "commonEFS4Notebooks",
            vpc = self.vpc,
            encrypted=True,
            enable_automatic_backups=True,
            performance_mode=efs.PerformanceMode('MAX_IO'),
            throughput_mode=efs.ThroughputMode('BURSTING'),
            security_group = self.sg)
        
        
        # Mount target for EFS
        # self.mount = efs.CfnMountTarget(
        #     self,
        #     "MountID",
        #     file_system_id=self.efs.file_system_id,security_groups=[self.sg.security_group_id,],
        #     subnet_id=self.vpc.private_subnets[0].subnet_id,
        #     )
        
        # IAM Roles
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

        # print(self.mount.get_att('attr_ip_address').to_string())
        encodedScript = LifecycleScriptStr.format(self.efs.file_system_id)
        # print("Adding following script to the lifecycle config..\n___\n\n"+encodedScript)

        code = [
            {"content": core.Fn.base64(encodedScript)}
        ]

        lifecycleconfig = sm.CfnNotebookInstanceLifecycleConfig(
            self,
            "LifeCycleConfig",
            notebook_instance_lifecycle_config_name=LifeCycleConfigName,
            on_create=None, on_start=code)
    
        
        instances = []
        for i in range(num_instances):
            nid = 'CDK-Notebook-Instance-User-'+str(i) 
            instances.append(sm.CfnNotebookInstance(
                self,
                nid,
                instance_type = 'ml.t2.medium',
                volume_size_in_gb = 5,
                security_group_ids = [self.sg.security_group_id],
                subnet_id = self.vpc.private_subnets[0].subnet_id,
                notebook_instance_name = nid,
                role_arn = nRole.role_arn,
                lifecycle_config_name = lifecycleconfig.notebook_instance_lifecycle_config_name
                ))

        core.CfnOutput(self, "VPC_id",value=self.vpc.vpc_id)
        core.CfnOutput(self, "EFS_id",value=self.efs.file_system_id)
        [core.CfnOutput(self, "NotebookInstance_"+str(c),value=notebook.notebook_instance_name) for c,notebook in enumerate(instances)]