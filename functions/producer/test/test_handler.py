from unittest.mock import Mock

from index import handler
from module.sqs_service import SqsPublisher


def test_handler(mocker):
    sqs_client_mock = Mock()

    def __init__(self, queue_name):
        self.sqs_client = sqs_client_mock
        self.queue_name = queue_name

    mocker.patch.object(SqsPublisher, '__init__', __init__)
    handler("", {})
    sqs_client_mock.send_message.assert_called_once()

    _, call_kwargs = sqs_client_mock.send_message.call_args
    assert 'QueueUrl' in call_kwargs
