import json
import os
from datetime import datetime

import boto3
import yaml

from constants import DATE_FORMAT, SNS_CONFIG_FILE


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
        return SnsConfig('email').read()

    def notify(self, sqs_response):
        for m in sqs_response.get('Messages'):
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
