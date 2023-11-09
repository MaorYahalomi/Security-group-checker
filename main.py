import boto3
import os
from botocore.exceptions import ClientError
import datetime

# search for security groups in a list of security groups in print the security group id and vpc id

# session = boto3.Session()


log_only_mode = os.environ['LOGGING_MODE']
s3_bucket_name = os.environ['S3_BUCKET_NAME']
session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    aws_session_token=os.environ['AWS_SESSION_TOKEN'])

# Create an S3 client using the session
ec2 = session.client('ec2', region_name='us-east-1')
s3_resource = boto3.resource('s3')

def revoke_sg_rule(sg_object, sg_rule_list):
    print("remove this role")
    response = ec2.revoke_security_group_ingress(GroupId=sg_object['GroupId'], IpPermissions=sg_rule_list)


def check_sg_rule(sg_object):
    # checks if this sg as an open rule to the world
    open_rule_list = []
    open_rules_log = []
    for permission_set in sg_object['IpPermissions']:
        if permission_set['IpProtocol'] != '-1' and len(permission_set['IpRanges']) > 0:
            if permission_set['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                print(f"Security Group {sg_object['GroupId']} has port {permission_set['FromPort']} open to the world")
                open_rule_list.append(permission_set)
                open_rules_log.append((sg_object['GroupId'], permission_set['FromPort']))
        elif permission_set['IpProtocol'] == '-1' and permission_set['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                print(f"Security Group {sg_object['GroupId']} includes a rule that allows global access for all servicese")
                open_rule_list.append(permission_set)
                open_rules_log.append((sg_object['GroupId'], ''))

    return open_rule_list, open_rules_log


def create_log_file(list_of_rules_to_delete):
    # list_of_open_rules
    # the function get a list of all the sg which has open rules to the world

    file_path = 'sg_logs.txt'
    with open(file_path,'a') as file:
        for item in list_of_rules_to_delete:
            if item[1] == '':
                file.write(f"Security Group {item[0]} is open to the world for every service\n")
            if item[1]:
                file.write(f"Security Group {item[0]} has port {item[1]} open to the world\n")
    

def upload_log_to_s3(bucket_name):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")
    year, month, day = datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day
    response = s3_resource.meta.client.upload_file("sg_logs.txt", bucket_name, f"{year}/{month}/{day}/log_{current_time}.txt")

def logging_mode():
    # check if running in logging mode:
    # True = Logging only mode , False = rule Enforcement Mode
    if log_only_mode == "True":
        return True
    return False


def main():
    # Go over all the SG's on every VPC and create a list
    if logging_mode():
        print("logging Mode is enabled.\n")
    else:
        print("Enforcement mode for rules is enabled.\n")
    try:
        response = ec2.describe_security_groups()
        for sg in response['SecurityGroups']:
            list_of_rules_to_del, list_of_rules_log = check_sg_rule(sg)
            if len(list_of_rules_to_del) > 0:
                create_log_file(list_of_rules_log)
                if not logging_mode():
                    revoke_sg_rule(sg, list_of_rules_to_del)
                # print(list_of_ruls_log)
            # print(f"{sg['GroupId']} {sg['VpcId']}")
        upload_log_to_s3(s3_bucket_name)
    except ClientError as e:
        print(f"Unexpected error: {e}")



# main()
print(log_only_mode)


