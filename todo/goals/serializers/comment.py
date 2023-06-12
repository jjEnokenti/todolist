from core.serializers import UserProfileSerializer
from goals.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'goal': {'read_only': True},
        }


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'user': {'read_only': True},
        }
