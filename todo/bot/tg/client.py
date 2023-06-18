import requests
from aiogram.types import Update
from bot.tg.dc import (
    GetUpdatesResponse,
    SendMessageResponse
)


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url(method='getUpdates')
        raw_response = requests.get(url=url, params={'offset': offset, 'timeout': timeout}, verify=False).json()
        updates = [Update(**update) for update in raw_response['result']]
        response = GetUpdatesResponse(ok=raw_response['ok'], result=updates)
        return response

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        method = f'sendMessage?chat_id={chat_id}&text={text}'
        raw_response = requests.get(self.get_url(method=method), verify=False).json()
        response = SendMessageResponse(**raw_response)
        return response
