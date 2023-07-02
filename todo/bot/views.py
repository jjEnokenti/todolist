import os

from django.core import exceptions
from dotenv import load_dotenv
from rest_framework import (
    generics,
    permissions,
)
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import BotVerifySerializer
from bot.tg.client import TgClient


load_dotenv()


class BotVerify(generics.UpdateAPIView):
    """Bot verify update view class.

    only patch method.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BotVerifySerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        data = self.get_serializer(request.data).data
        tg_user = TgUser.objects.filter(verification_code=data['verification_code']).first()
        tg_client = TgClient(os.getenv('BOT_TOKEN'))

        if not tg_user:
            raise exceptions.BadRequest('verification code not correct')

        tg_user.user = request.user
        tg_user.save()

        tg_client.send_message(chat_id=tg_user.chat_id, text='Ваша верификация успешно завершена.')
        return Response('OK', status=200)
