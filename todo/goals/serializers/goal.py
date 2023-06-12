from goals.models import Goal
from rest_framework import serializers


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'category': {'read_only': True},
            'due_date': {'required': False},
            'description': {'required': False}
        }


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
