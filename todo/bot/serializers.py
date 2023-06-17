from bot.models import TgUser
from rest_framework import serializers


class BotVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = ['verification_code']
