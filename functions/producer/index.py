from module.logger import logger
from module.message_service import MessageService
from module.sqs_service import SqsPublisher


def handler(event, _context):
    """
    Create a Lambda function (producer lambda) that wakes up from a cron trigger every 3 minutes.
    This function writes a JSON message to a new SQS queue.
    The message contains the timestamp in which the message was created, so would be something like:
    {
     timestamp: "12.12.20 14:47:05"
    }
    """
    logger.info(f'Received event: {event}')
    message = MessageService().timestamp_message()
    SqsPublisher().publish(message)


if __name__ == '__main__':
    handler('', {})
