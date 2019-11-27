#!/usr/bin/env python3

from aws_cdk import core

from dask_fargate.dask_fargate_stack import DaskFargateStack


app = core.App()
DaskFargateStack(app, "dask-fargate")

app.synth()
