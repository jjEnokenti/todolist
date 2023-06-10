from rest_framework import (
    generics,
    permissions
)

from todo.goals.models import GoalCategory
from todo.goals.serializers.category import GoalCategoryCreateSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
