from goals.models import Goal
from rest_framework import serializers


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

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('Category was deleted.')
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('This category not your.')

        return value
