from goals.models import Goal
from rest_framework import (
    exceptions,
    serializers
)


class GoalSerializer(serializers.ModelSerializer):
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
                role__in=(
                        category.board.participants.model.Role.owner,
                        category.board.participants.model.Role.writer
                )
        ):
            return category
        raise exceptions.PermissionDenied('You do not have permissions to this category.')
