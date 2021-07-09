import boto3


class SqsPublisher:
    def __init__(self):
        self.sqs_client = boto3.client('sqs')

    def publish(self, message):
        queue_url = self.sqs_client.get_queue_url(
            QueueName="lambda-queue",
        ).get('QueueUrl')
        response = self.sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )