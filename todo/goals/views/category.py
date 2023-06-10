from rest_framework import (
    generics,
    permissions
)

from ..models import GoalCategory
from ..serializers.category import GoalCategoryCreateSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
