#!/usr/bin/env python3
import sys
import boto3
from botocore.exceptions import ClientError
aws_profile = "default"

aws_access_key_id = None
aws_secret_access_key = None
aws_region = "eu-west-2"

boto3_client_ec2 = None

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
    global boto3_client_ec2
    try:
        boto3_client_ec2 = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )
    except Exception as e:
        print(e)
        sys.exit()
        

def create_instance():
    try: 
        response = boto3_client_ec2.create_image(
            BlockDeviceMappings =[
              { 'DeviceName': '/dev/xvda', 
                'Ebs' : {
                    'DeleteOnTermination': False,
                    'VolumeSize': 20,
                }
              } 
            ],
            Description='An AMI for my test server - 5',
            InstanceId= sys.argv[1],
            Name=sys.argv[2],
        )
        print(response)    
    except Exception as e:
        print(e)
        sys.exit()

def main():
    get_aws_credentials()
    make_boto3_client()
    create_instance()


if __name__ == '__main__':
    
    
    main()
