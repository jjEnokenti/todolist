import requests
from bot.tg.dc import (
    GetUpdatesResponse,
    SendMessageResponse,
    get_updates_schema,
    send_message_schema,
)


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse | None:
        url = self.get_url(method='getUpdates')
        params = {'offset': offset, 'timeout': timeout}
        data = requests.get(url=url, params=params)
        if data.ok:
            return get_updates_schema().load(data.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse | None:
        url = self.get_url(method='sendMessage')
        params = {'chat_id': chat_id, 'text': text}
        data = requests.get(url=url, params=params)
        if data.ok:
            return send_message_schema().load(data.json())
