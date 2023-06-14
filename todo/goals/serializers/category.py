from core.serializers import UserProfileSerializer
from goals.models import GoalCategory
from rest_framework import (
    exceptions,
    serializers
)


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'user', 'created', 'updated')
        fields = '__all__'

    def validate_board(self, board):
        if board.is_deleted:
            raise serializers.ValidationError({'create error': 'Board is deleted.'})
        if not board.participants.filter(
                board=board,
                user=self.context['request'].user,
                role__in=(
                        board.participants.model.Role.owner,
                        board.participants.model.Role.writer
                )
        ):
            raise exceptions.PermissionDenied
        return board


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')
