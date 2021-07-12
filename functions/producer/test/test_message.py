import json
from datetime import datetime

from module.constants import DATE_FORMAT
from module.message_service import MessageService


def test_message():
    message_json = MessageService().timestamp_message()
    message = json.loads(message_json)
    timestamp = message.get('timestamp')
    assert isinstance(datetime.strptime(timestamp, DATE_FORMAT), datetime)
