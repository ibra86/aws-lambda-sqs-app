import boto3

from module.constants import SQS_WAIT_TIME_SECONDS, SQS_VISIBILITY_TIMEOUT, SQS_MAX_NUMBER_OF_MESSAGES


class SqsProcessor:
    def __init__(self, queue_name):
        self.sqs_client = boto3.client('sqs')
        self.queue_name = queue_name
        self.sqs_response = self.read_messages()

    @property
    def queue_url(self):
        return self.sqs_client.get_queue_url(QueueName=self.queue_name).get('QueueUrl')

    def read_messages(self):
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=SQS_MAX_NUMBER_OF_MESSAGES,
            VisibilityTimeout=SQS_VISIBILITY_TIMEOUT,
            WaitTimeSeconds=SQS_WAIT_TIME_SECONDS,
        )
        return response
