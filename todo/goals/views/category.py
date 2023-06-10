from goals.models import GoalCategory
from goals.serializers.category import (
    GoalCategoryCreateSerializer,
    GoalCategoryListSerializer
)
from rest_framework import (
    generics,
    permissions
)


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCategoryListView(generics.ListAPIView):
    serializer_class = GoalCategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )
