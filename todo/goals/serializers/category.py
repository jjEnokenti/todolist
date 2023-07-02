from rest_framework import (
    exceptions,
    serializers,
)

from core.serializers import UserProfileSerializer
from goals.models import GoalCategory


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """Category create serializer.

    define board validate method.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'user', 'created', 'updated')
        fields = '__all__'

    def validate_board(self, board):
        """Validate board object for goal category."""
        if board.is_deleted:
            raise serializers.ValidationError({'create error': 'Board is deleted.'})
        if board.participants.filter(
                board=board,
                user=self.context['request'].user,
                role__in=(board.participants.model.Role.owner,
                          board.participants.model.Role.writer)
        ).exists():
            return board

        raise exceptions.PermissionDenied('You do not have permissions for edite this board.')


class GoalCategorySerializer(serializers.ModelSerializer):
    """Category serializer."""
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')
