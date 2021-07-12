import json
import os
from datetime import datetime

import boto3
import yaml

from module.constants import DATE_FORMAT, SNS_CONFIG_FILE, SNS_CONFIG_SUBSCRIPTION
from module.logger import logger


class SnsConfig:
    def __init__(self, subscription):
        self.subscription = subscription

    def read(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SNS_CONFIG_FILE)
        with open(config_path) as f:
            full_config = yaml.load(f)
        return full_config.get(self.subscription)


class SnsProcessor:
    def __init__(self, sns_topic):
        self.sns_client = boto3.client('sns')
        self.sns_topic = sns_topic

    @property
    def config(self):
        return SnsConfig(SNS_CONFIG_SUBSCRIPTION).read()

    def notify(self, sqs_response):
        if sqs_response.get('Messages') is not None:
            for m in sqs_response.get('Messages'):
                logger.debug(f'Processing message {m} to for SNS')
                timestamp = json.loads(m.get('Body')).get('timestamp')
                dt = datetime.strptime(timestamp, DATE_FORMAT)
                if dt.minute == 0:
                    self.send_message(dt.hour)

    def send_message(self, text):
        topics = self.sns_client.list_topics().get('Topics')
        topic_arn = [v for d in topics for v in d.values() if self.sns_topic in v][0]
        hour = f'{text:02d}:00'
        message = self.config['message'] % hour
        self.sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=self.config['subject']
        )
        logger.info(f'SNS notification sent by {SNS_CONFIG_SUBSCRIPTION}')
