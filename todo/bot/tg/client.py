import requests
from requests import Response

from bot.tg.dc import (
    GetUpdatesResponse,
    SendMessageResponse,
    get_updates_schema,
    send_message_schema,
)


class TgClient:
    """Telegram client."""
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str) -> str:
        """Formatted url"""
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse | Response:
        """Get updates from telegram server."""
        url = self.get_url(method='getUpdates')
        params = {'offset': offset, 'timeout': timeout}
        data = requests.get(url=url, params=params, timeout=timeout)
        if data.ok:
            return get_updates_schema().load(data.json())
        return data

    def send_message(self, chat_id: int, text: str, timeout: int = 60) -> SendMessageResponse | Response:
        """Send message to telegram client."""
        url = self.get_url(method='sendMessage')
        params = {'chat_id': chat_id, 'text': text}
        data = requests.get(url=url, params=params, timeout=timeout)
        if data.ok:
            return send_message_schema().load(data.json())
        return data
