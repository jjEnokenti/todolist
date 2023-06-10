from goals.models import Goal
from rest_framework import serializers


class GoalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('title', 'priority', 'deadline', 'category')
