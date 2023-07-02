from rest_framework import serializers

from bot.models import TgUser


class BotVerifySerializer(serializers.ModelSerializer):
    """Bot verify serializer."""
    class Meta:
        model = TgUser
        fields = ['verification_code']
