import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="dask_fargate",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "dask_fargate"},
    packages=setuptools.find_packages(where="dask_fargate"),

    install_requires=[
        "aws-cdk.core",
	"aws-cdk.aws_ec2",
	"aws-cdk.aws_ecs",
	"aws-cdk.aws_ecs_patterns",
    "aws-cdk.aws_ecr",
    "aws_cdk.aws_ecr_assets",
    "aws_cdk.aws_logs",
    "aws_cdk.aws_iam",
    "aws_cdk.aws_sagemaker"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
