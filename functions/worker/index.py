from module.logger import logger
from module.processor import Processor


def handler(event, _context):
    """
    Lambda triggered by SQS queue reading the messages from the queue.
    The function should save every timestamp to a new S3 bucket,
    so that this bucket will contain all timestamps that were sent.
    If the timestamp is an exact hour (13:00, 14:00 ..) it should notify a new SNS topic about it.
    The SNS should have a subscription via EMAIL
    sending an email to you saying "Received a timestamp with exact hour. The hour is HOUR".
    (ignore seconds when calculating exact hour)
    """
    logger.info(f'Received event: {event}')
    Processor().process()


if __name__ == '__main__':
    handler('', {})
