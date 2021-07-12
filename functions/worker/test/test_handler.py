from unittest.mock import Mock, PropertyMock

import pytest

from index import handler
from module.sns_service import SnsProcessor


def test_handler(mocker):
    sqs_read_mock = mocker.patch('module.sqs_service.SqsProcessor.read_messages')
    s3_store_mock = mocker.patch('module.s3_service.S3Processor.store')
    sns_notify_mock = mocker.patch('module.sns_service.SnsProcessor.notify')

    handler("", {})

    assert sqs_read_mock.call_count
    assert s3_store_mock.call_count
    assert sns_notify_mock.call_count


@pytest.fixture
def messages_with_exact_hour():
    messages = {'Messages': [{'Body': '{"timestamp": "2021-07-11 23:00:35"}'},
                             {'Body': '{"timestamp": "2021-07-11 22:03:36"}'}]}
    return messages


@pytest.fixture
def sns_topics_mock():
    return {'Topics': [{'mock': 'mock:timestamp-topic'}]}


def test_sns_exact_hour_message(mocker, messages_with_exact_hour, sns_topics_mock):
    mocker.patch('module.sqs_service.SqsProcessor.read_messages', return_value=messages_with_exact_hour)
    mocker.patch('module.s3_service.S3Processor.store')

    sns_client_mock = Mock()
    type(sns_client_mock).list_topics = PropertyMock(return_value=lambda: sns_topics_mock)

    def __init__(self, sns_topic):
        self.sns_client = sns_client_mock
        self.sns_topic = sns_topic

    mocker.patch.object(SnsProcessor, '__init__', __init__)
    handler("", {})
    sns_client_mock.publish.assert_called_once()

    _, call_kwargs = sns_client_mock.publish.call_args
    assert call_kwargs['TopicArn'] == 'mock:timestamp-topic'
    assert call_kwargs['Message'] == 'Received a timestamp with exact hour. The hour is 23:00.'
    assert call_kwargs['Subject'] == 'AWS-LAMBDA-SQS-APP exact hour notification'
