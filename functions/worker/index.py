import json
from datetime import datetime

from logger import logger
from sqs_publisher import SqsPublisher

DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'


def handler(event, _context):
    """
    Lambda triggered by SQS queue reading the messages from the queue.
    The function should save every timestamp to a new S3 bucket,
    so that this bucket will contain all timestamps that were sent.
    """
    logger.info(f'Received event: {event}')


if __name__ == '__main__':
    handler('', {})
