from goals.models import Goal
from rest_framework import serializers


class GoalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('title', 'priority', 'deadline', 'category')


class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        extra_kwargs = {
            'description': {'required': False},
            'deadline': {'required': False},
        }
        read_only_fields = (
            'id',
            'created',
            'updated'
        )

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('Category was deleted.')
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('This category not your.')

        return value
