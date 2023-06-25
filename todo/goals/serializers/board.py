from django.contrib.auth import get_user_model
from django.db import transaction
from goals.models import (
    Board,
    BoardParticipant,
)
from rest_framework import serializers


USER_MODEL = get_user_model()


class BoardParticipantSerializer(serializers.ModelSerializer):
    """Board participants serializer."""
    role = serializers.ChoiceField(
        required=True,
        choices=BoardParticipant.Role.choices
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=USER_MODEL.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    """Board serializer.

    override update method for add and remove board participants.
    """
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data):
        user_owner = self.context['request'].user or validated_data.pop('user')
        participants_data = validated_data.pop('participants')
        title = validated_data.pop('title')

        new_participants = {participant['user']: participant for participant in participants_data}

        with transaction.atomic():
            board_participants = instance.participants.exclude(user=user_owner)
            for old_participant in board_participants:
                if old_participant.user not in new_participants:
                    old_participant.delete()
                else:
                    if (new_participants[old_participant.user]['role'] != old_participant.role
                            and new_participants[old_participant.user]['role'] != 1):
                        old_participant.role = new_participants[old_participant.user]['role']
                        old_participant.save()
                    new_participants.pop(old_participant.user)

            for participant in new_participants.values():
                role = participant.get('role')
                user = participant.get('user')

                BoardParticipant.objects.create(
                    user=user, board=instance, role=role
                )
            if instance.title != title:
                instance.title = title
            instance.save()

        return instance


class BoardCreateSerializer(serializers.ModelSerializer):
    """Board create serializer."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def create(self, validated_data):
        owner = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=owner, board=board, role=BoardParticipant.Role.owner
        )

        return board


class BoardListSerializer(serializers.ModelSerializer):
    """Board list serializer."""
    class Meta:
        model = Board
        fields = '__all__'
