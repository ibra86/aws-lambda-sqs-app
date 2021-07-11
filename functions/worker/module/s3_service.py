import json

import boto3


class S3Processor:

    def __init__(self, bucket):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket

    def store(self, sqs_response):
        for m in sqs_response.get('Messages'):
            body = m.get('Body')
            timestamp = json.loads(body).get('timestamp')
            file_name = f"timestamp_{timestamp.replace(' ', '_')}.json"
            self.s3_client.put_object(Body=body, Bucket=self.bucket, Key=file_name)
