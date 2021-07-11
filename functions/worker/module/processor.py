from module.constants import SQS_QUEUE_NAME, S3_BUCKET, SNS_TOPIC
from module.s3_service import S3Processor
from module.sns_service import SnsProcessor
from module.sqs_service import SqsProcessor


class Processor:
    @staticmethod
    def process():
        sqs_response = SqsProcessor(SQS_QUEUE_NAME).read_messages()
        S3Processor(S3_BUCKET).store(sqs_response)
        SnsProcessor(SNS_TOPIC).notify(sqs_response)
