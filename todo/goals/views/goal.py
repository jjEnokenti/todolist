from goals.models import Goal
from goals.serializers.goal import GoalListSerializer
from rest_framework import (
    filters,
    generics,
    permissions
)


class GoalListView(generics.ListAPIView):
    serializer_class = GoalListSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    ordering = ['-priority', 'deadline']
    ordering_fields = ['deadline']

    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.filter(
            category__user=self.request.user,
            category__is_deleted=False,
            status__in=(1, 2, 3)
        )
