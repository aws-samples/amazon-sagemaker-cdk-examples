#!/usr/bin/env python3

from aws_cdk import core

from multinotebookefs.multinotebookefs_stack import MultinotebookefsStack


app = core.App()
MultinotebookefsStack(app, "multinotebookefs")

app.synth()
