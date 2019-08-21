#!/bin/bash

cd /home/ec2-user/SageMaker/

mkdir -p efs

sudo yum install -y amazon-efs-utils

sudo mount -t efs {}:/ efs

sudo chmod go+rw ./efs