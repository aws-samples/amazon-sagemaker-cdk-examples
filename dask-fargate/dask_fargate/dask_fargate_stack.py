from aws_cdk import (core, aws_ec2 as ec2, aws_ecr,
    aws_ecs as ecs, aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets, aws_logs as logs,
    aws_servicediscovery as sd, aws_iam as iam_)

use_rapids = False
use_notebook = False

class DaskFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        CONTAINER_IMAGE = 'daskdev/dask:0.19.4'
        if use_rapids:
        	CONTAINER_IMAGE = 'rapidsai/rapidsai:latest'

        if use_notebook:
        	CONTAINER_IMAGE = 'daskdev/dask-notebook:latest'

        #Create ECR repository
        #ecr = aws_ecr.Repository(self, 'MyECR', repository_name='dask')
        # not needed if you use an asset like below:

        #Create asset in build time
        dockerimage = ecr_assets.DockerImageAsset(self, 'MyDocker', directory = 'dockerstuff', build_args=['-t dask .'], repository_name='dask')

        # Create vpc
        vpc = ec2.Vpc(self, 'MyVpc', max_azs=3)     # default is all AZs in region


        # Create log groups for the scheduler and workers
        s_logs = logs.LogGroup(self, 'SlogGroup', log_group_name='SlogGroup')
        w_logs = logs.LogGroup(self, 'WlogGroup', log_group_name='WlogGroup')

        #Create private namespace
        nspace = sd.PrivateDnsNamespace(self, 'MyNamespace', vpc=vpc, name='local-dask')

        # #Create role for ECS
        nRole = iam_.Role(self,'ECSExecutionRole',
            assumed_by = iam_.ServicePrincipal('ecs-tasks'))
        
        nPolicy = iam_.Policy(
            self,
            "ECSExecutionPolicy",
            policy_name = "ECSExecutionPolicy",
            statements = [iam_.PolicyStatement(actions = 
                ['ecr:BatchCheckLayerAvailability',
                'ecr:GetDownloadUrlForLayer',
                'ecr:BatchGetImage',
                'ecr:GetAuthorizationToken',
                'logs:CreateLogStream',
                'logs:PutLogEvents'], resources=['*',]),]).attach_to_role(nRole)


        # Create ECS cluster
        cluster = ecs.Cluster(self, 'DaskCluster', vpc=vpc, cluster_name='Fargate-Dask-Cluster')

        schedulerRegistry = sd.Service(self,'serviceRegistryScheduler', 
            namespace=nspace,dns_ttl=core.Duration.seconds(60),
            custom_health_check=sd.HealthCheckCustomConfig(failure_threshold=10),
            name='Dask-Scheduler')

        workerRegistry = sd.Service(self,'workerRegistryScheduler', 
            namespace=nspace,dns_ttl=core.Duration.seconds(60),
            custom_health_check=sd.HealthCheckCustomConfig(failure_threshold=10),
            name='Dask-Worker')


        #------------------------------------------------------------------------

        # Very less control with ECS patterns, did not work

        # ecs_patterns.ApplicationLoadBalancedFargateService(self, "DaskFargateStack",
        #     cluster=cluster,            # Required
        #     cpu=512,                    # Default is 256
        #     desired_count=6,            # Default is 1
        #     task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
        #         image=ecs.ContainerImage.from_registry(CONTAINER_IMAGE)),
        #     memory_limit_mib=2048,      # Default is 512
        #     public_load_balancer=True)  # Default is False
