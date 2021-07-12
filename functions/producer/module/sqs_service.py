import boto3

from module.logger import logger


class SqsPublisher:
    def __init__(self, queue_name):
        self.sqs_client = boto3.client('sqs')
        self.queue_name = queue_name

    @property
    def queue_url(self):
        return self.sqs_client.get_queue_url(QueueName=self.queue_name).get('QueueUrl')

    def publish(self, message):
        self.sqs_client.send_message(QueueUrl=self.queue_url, MessageBody=message)
        logger.info(f'Send message to SQS: {message}')
