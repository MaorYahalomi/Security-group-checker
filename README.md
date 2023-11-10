# Security Group Open Rule Checker
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) - Version 3.9

## Table Of Contents ###
- [Description](#description)
- [GitHub Workflows](#GitHub-Workflows )
- [Prerequisites](#Prerequisites )
- [Configurable-variables](#Configurable-variables )
- [How To Use](#how-to-use )
  * [Running Manually Using Python](#running-manually-using-python)
  * [Using Docker container](#using-docker-container)

## Description ##
Security Group Open Rule Checker is an open-source tool written in Python that allows a cloud administrator to verify<br>
If there is any rule in the Security Group that allows access from the internet.<br>
The tool can be configured in 2 modes:<br>
1. **Logging Mode only** - Which only stores all the security groups that have access to the world in a log file in an S3 bucket.<br>
2. **Rule Enforcement mode** - Which removes automatically any security groups rules that are opened to the world and store the results in S3 as well.

## GitHub Workflows ##
There are two main workflows that are configured to run wh
1.  **Docker Build and Push** - Triggered each time there is a change in the code and push to the main branch, build a docker container,<br> and push the image to DockerHub.
2.  **Daily workflow** - Runs the script every day at 8 AM.

## Prerequisites ##
In order to run operations on AWS APIS's the script needs to be configured with AWS ACCESS-KEY, SECRET-KEY, and SESSION-TOKEN
which allows to perform uploading objects to S3 bucket, in order to upload the logs that contain all the security groups id's that have open rules<br>

**Note** - SESSION-TOKEN secret should be provided in cases when assuming a role in order to make the API calls.<br>
All the secrets above should be configured as GitHub Secrets in the following way:

```
#  AWS_ACCESS_KEY_ID
#  AWS_SECRET_ACCESS_KEY
#  AWS_SESSION_TOKEN
```

In order to push the container to DockerHub, the user should also provide DockerHub credentials as GitHub secrets in the following way:

```
#  DOCKER_USERNAME
#  DOCKER_PASSWORD
```

## Configurable-variables ##

The Python script can be configured to run with different variables in order to provide flexibility for each environment
The Following variable can be configured on the "Daily Workflow" Action:
* **Enable logging mode only** - Allow the script to run in "logging mode" only. (Default - True)
* **S3 bucket name** -  The name of the S3 bucket to upload the log file.
* **AWS Region** -  The AWS region name. (Default - us-east-1 [N.Verginia])
  
![trigger](https://github.com/MaorYahalomi/maven-project/assets/30255797/9c6a6abe-bcfd-4e09-be06-a743ba797d27)


