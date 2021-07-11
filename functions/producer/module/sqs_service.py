import boto3

from module.constants import SQS_QUEUE_NAME
from module.logger import logger


class SqsPublisher:
    def __init__(self):
        self.sqs_client = boto3.client('sqs')

    def publish(self, message):
        queue_url = self.sqs_client.get_queue_url(QueueName=SQS_QUEUE_NAME).get('QueueUrl')
        self.sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)
        logger.info(f'Send message to SQS: {message}')
