from rest_framework import (
    exceptions,
    serializers,
)

from goals.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    """Goal serializer."""

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'category'
        )


class GoalCreateSerializer(serializers.ModelSerializer):
    """Goal create serializer.

    define category validate method.
    """

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
        )

    def validate_category(self, category):
        if category.is_deleted:
            raise serializers.ValidationError('Category was deleted.')
        if category.board.participants.filter(
                user=self.context['request'].user,
                board=category.board,
                role__in=(category.board.participants.model.Role.owner,
                          category.board.participants.model.Role.writer)
        ):
            return category
        raise exceptions.PermissionDenied('You do not have permissions to this category.')
