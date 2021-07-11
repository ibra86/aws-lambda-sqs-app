import json
from datetime import datetime

from module.constants import DATE_FORMAT


class MessageService:

    @staticmethod
    def timestamp_message():
        body = {'timestamp': datetime.utcnow().strftime(DATE_FORMAT)}
        message = json.dumps(body)
        return message
