#!/usr/bin/env python3
import sys
import boto3
from botocore.exceptions import ClientError
aws_profile = "default"

aws_access_key_id = None
aws_secret_access_key = None
aws_region = "eu-west-2"

boto3_client_asg = None

def get_aws_credentials():
    import configparser
    import os
    global aws_profile
    global aws_access_key_id
    global aws_secret_access_key
    path = os.environ['HOME'] + '/.aws/credentials'
    config = configparser.ConfigParser()
    config.read(path)
    
    
    if aws_profile in config.sections():
        aws_access_key_id = config[aws_profile]['aws_access_key_id']
        aws_secret_access_key = config[aws_profile]['aws_secret_access_key']
    else:
        print("Cannot find profile '{}' in {}".format(aws_profile, path), True)
        sys.exit()
        
    if aws_access_key_id is None or aws_secret_access_key is None:
        print("AWS config values not set in '{}' in {}".format(aws_profile, path), True)
        sys.exit()
        
def make_boto3_client():
    global boto3_client_asg
    try:
        boto3_client_asg = boto3.client(
            'autoscaling',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
    except Exception as e:
        print(e)
        sys.exit()
        
def asg_instance_refresh():
    try:
        response = boto3_client_asg.start_instance_refresh(
            AutoScalingGroupName =  'testasg',
            DesiredConfiguration={
                'LaunchTemplate': {
                    'LaunchTemplateName': 'mytemplate',
                     'Version': '$Latest',
                },
            },
            Preferences={
                'MinHealthyPercentage': 0,
                'InstanceWarmup': 60,
                'SkipMatching': False,
            }
        )
        print(response) 
    except Exception as e:
        print(e)
        sys.exit()
    
def main():
    get_aws_credentials()
    make_boto3_client()
    asg_instance_refresh()


if __name__ == '__main__':
    
    
    main()
