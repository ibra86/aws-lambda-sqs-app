import json

import boto3

from module.logger import logger


class S3Processor:

    def __init__(self, bucket):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket

    def store(self, sqs_response):
        if sqs_response.get('Messages') is not None:
            for m in sqs_response.get('Messages'):
                logger.debug(f'Processing message {m} to be stored in S3')
                body = m.get('Body')
                timestamp = json.loads(body).get('timestamp')
                file_name = f"timestamp_{timestamp.replace(' ', '_')}.json"
                self.s3_client.put_object(Body=body, Bucket=self.bucket, Key=file_name)
                logger.info(f'File {file_name} stored to S3 {self.bucket}')
        else:
            logger.info('Nothing to store in S3')
