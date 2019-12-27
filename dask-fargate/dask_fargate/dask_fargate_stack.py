from aws_cdk import (core, aws_ec2 as ec2, aws_ecr,
    aws_ecs as ecs, aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets, aws_logs as logs,
    aws_servicediscovery as sd, aws_iam as iam_,
    aws_sagemaker as sagemaker_)

use_rapids = False
use_notebook = False

class DaskFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        # CONTAINER_IMAGE = 'daskdev/dask:0.19.4'
        # if use_rapids:
        #   CONTAINER_IMAGE = 'rapidsai/rapidsai:latest'

        # if use_notebook:
        #   CONTAINER_IMAGE = 'daskdev/dask-notebook:latest'

        #TODO : Create ECR repository
        #Update: Not required sunce ecs.ContainerImage already creates and pushes using same asset

        #ecr = aws_ecr.Repository(self, 'MyECR', repository_name='dask')
        # not needed if you use an asset like below:

        dockercontainer = ecs.ContainerImage.from_asset(directory = 'dockerstuff', build_args=['-t dask .'])
        
        # Create vpc
        vpc = ec2.Vpc(self, 'MyVpc', max_azs=3)     # default is all AZs in region
        subnets = vpc.private_subnets

        # Create log groups for the scheduler and workers
        s_logs = logs.LogGroup(self, 'SlogGroup', log_group_name='SlogGroup')
        w_logs = logs.LogGroup(self, 'WlogGroup', log_group_name='WlogGroup')

        #Create private namespace
        #nspace = sd.PrivateDnsNamespace(self, 'MyNamespace', vpc=vpc, name='local-dask')

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
                'logs:PutLogEvents','sagemaker:*','s3:*'], resources=['*',]),]).attach_to_role(nRole)


        # Create ECS cluster
        cluster = ecs.Cluster(self, 'DaskCluster', 
            vpc=vpc, cluster_name='Fargate-Dask-Cluster')

        nspace = cluster.add_default_cloud_map_namespace(name='local-dask',type=sd.NamespaceType.DNS_PRIVATE,vpc=vpc)

        #TO DO: Use default namespace for cluster and use cmap options within fargate service
        #Update: done

        # schedulerRegistry = sd.Service(self,'serviceRegistryScheduler', 
        #     namespace=nspace,dns_ttl=core.Duration.seconds(60),
        #     custom_health_check=sd.HealthCheckCustomConfig(failure_threshold=10),
        #     name='Dask-Scheduler')
       
        # # schedulerRegistry.register_ip_instance(id='serviceRegistryScheduler',ipv4='')

        # workerRegistry = sd.Service(self,'workerRegistryScheduler', 
        #     namespace=nspace,dns_ttl=core.Duration.seconds(60),
        #     custom_health_check=sd.HealthCheckCustomConfig(failure_threshold=10),
        #     name='Dask-Worker')
       

        # -------------------- Add scheduler task ------------------------
        schedulerTask = ecs.TaskDefinition(self, 'taskDefinitionScheduler',
            compatibility=ecs.Compatibility.FARGATE,
            cpu='4096', memory_mib='8192',
            network_mode=ecs.NetworkMode.AWS_VPC,
            placement_constraints=None, execution_role=nRole,
            family='Dask-Scheduler', task_role=nRole)

        schedulerTask.add_container('MySchedulerImage', image=dockercontainer,
            command=['dask-scheduler'], cpu=4096, essential=True,
            logging=ecs.LogDriver.aws_logs(stream_prefix='ecs',log_group = s_logs),
            memory_limit_mib=8192, memory_reservation_mib=8192)


        # -------------------- Add worker task -----------------------------
        workerTask = ecs.TaskDefinition(self, 'taskDefinitionWorker',
            compatibility=ecs.Compatibility.FARGATE,
            cpu='4096', memory_mib='8192',
            network_mode=ecs.NetworkMode.AWS_VPC,
            placement_constraints=None, execution_role=nRole,
            family='Dask-Worker', task_role=nRole)

        workerTask.add_container('MyWorkerImage', image=dockercontainer,
            command=['dask-worker','dask-scheduler.local-dask:8786','--memory-limit 1800MB',
            '--worker-port 9000','--nanny-port 9001','--bokeh-port 9002'], 
            cpu=4096, essential=True,
            logging=ecs.LogDriver.aws_logs(stream_prefix='ecs',log_group = s_logs),
            memory_limit_mib=8192, memory_reservation_mib=8192)

        # Task security group
        sg = ec2.SecurityGroup(self, 'MySG',
            vpc=vpc,description='Enable Scheduler ports access',
            security_group_name='DaskSecurityGroup')

        # Ingress rule requires IPeer not Peer
        # TO DO: fix from any ipv4 to SG
        p1 = ec2.Peer().ipv4('0.0.0.0/0'); p2 = ec2.Peer().ipv4('0.0.0.0/0');

        sg.add_ingress_rule(peer = p1, connection = ec2.Port(protocol=ec2.Protocol.TCP,
                string_representation='p1', 
                from_port=8786, to_port=8789))

        sg.add_ingress_rule(peer = p2, connection = ec2.Port(protocol=ec2.Protocol.TCP,
                string_representation='p2', 
                from_port=9000, to_port=9002))

        # ----------------- Add Scheduler Service -----------------------

        # deployconfig = ecs.CfnService.DeploymentConfigurationProperty(maximum_percent=200,minimum_healthy_percent=100)

        # vpcconfig = ecs.CfnService.AwsVpcConfigurationProperty(subnets = subnets,assign_public_ip=True,security_groups=[sg])

        # networkconfig = ecs.CfnService.NetworkConfigurationProperty(awsvpc_configuration=vpcconfig)

        # schedulerService = ecs.CfnService(self, 'DaskSchedulerService', 
        #     task_definition = schedulerTask, deployment_configuration=deployconfig,
        #     cluster=cluster, desired_count=1, enable_ecs_managed_tags=None,
        #     launch_type='FARGATE',network_configuration=networkconfig,
        #     service_registries=schedulerRegistry)

        #ecs.CfnService.ServiceRegistryProperty()

        # Try fargate service? No service registry option available
        #using default cluster namespace
        cmap1 = ecs.CloudMapOptions(dns_ttl=core.Duration.seconds(60), failure_threshold=10, name='Dask-Scheduler')

        schedulerService = ecs.FargateService(self, 'DaskSchedulerService',
            task_definition=schedulerTask,
            assign_public_ip=True,security_group=sg,
            #vpc_subnets=subnets, 
        cluster=cluster,desired_count=1,
            max_healthy_percent=200, min_healthy_percent=100,
            service_name='Dask-Scheduler',cloud_map_options=cmap1)

        # schedulerService.enable_cloud_map(name = 'serviceRegistryScheduler')
        # schedulerRegistry.register_non_ip_instance(self,instance_id='DaskSchedulerService')

        # ----------------- Add Worker Service -----------------------
        #using default cluster namespace
        cmap2 = ecs.CloudMapOptions(dns_ttl=core.Duration.seconds(60), failure_threshold=10, name='Dask-Worker')


        workerService = ecs.FargateService(self, 'DaskWorkerService',
            task_definition=workerTask,
            assign_public_ip=True,security_group=sg,
            #vpc_subnets=subnets, 
        cluster=cluster,desired_count=1,
            max_healthy_percent=200, min_healthy_percent=100,
            service_name='Dask-Worker',cloud_map_options=cmap2)

        # workerService.enable_cloud_map(name = 'workerRegistryScheduler')



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


        # Start a notebook in the same vpc
        # print(type(sg.security_group_id))
        # print("------------------------------")
        # print(subnets[0].subnet_id)
                #Create role for Notebook instance
        smRole = iam_.Role(
            self,
            "notebookAccessRole",
            assumed_by = iam_.ServicePrincipal('sagemaker'))
        
        smPolicy = iam_.Policy(
            self,
            "notebookAccessPolicy",
            policy_name = "notebookAccessPolicy",
            statements = [iam_.PolicyStatement(actions = ['s3:*','ecs:*'], resources=['*',]),]).attach_to_role(smRole)


        notebook = sagemaker_.CfnNotebookInstance(
                self,
                'DaskNotebook',
                instance_type = 'ml.t2.medium',
                volume_size_in_gb = 50,
                security_group_ids = [sg.security_group_id],
                subnet_id = subnets[0].subnet_id,
                notebook_instance_name = 'DaskNotebook',
                role_arn = smRole.role_arn,
                root_access='Enabled',
                direct_internet_access='Enabled',
                default_code_repository='https://github.com/w601sxs/dask-examples.git')
