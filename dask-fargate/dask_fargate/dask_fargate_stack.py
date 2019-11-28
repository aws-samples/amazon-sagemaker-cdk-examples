from aws_cdk import (core, aws_ec2 as ec2, aws_ecs as ecs, aws_ecs_patterns as ecs_patterns)

use_rapids = False
use_notebook = True

class DaskFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        CONTAINER_IMAGE = 'daskdev/dask:0.19.4'
        if use_rapids:
        	CONTAINER_IMAGE = 'rapidsai/rapidsai:latest'

        if use_notebook:
        	CONTAINER_IMAGE = 'daskdev/dask-notebook:latest'

        
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)     # default is all AZs in region

        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "DaskFargateStack",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=6,            # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(CONTAINER_IMAGE)),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True)  # Default is False
