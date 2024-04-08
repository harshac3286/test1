import os
import boto3

class AwsConnect:
    def session_connect(self):
        session = boto3.Session(
            region_name=os.getenv('AWS_REGION'), 
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        return session

    def client_connect(self):
        client = boto3.Session(
            region_name=os.getenv('AWS_REGION'), 
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        return client