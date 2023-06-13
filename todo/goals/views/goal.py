from django_filters.rest_framework import DjangoFilterBackend
from goals.filters import GoalListFilters
from goals.models import (
    Goal,
    Status
)
from goals.serializers.goal import (
    GoalCreateSerializer,
    GoalSerializer
)
from rest_framework import (
    filters,
    generics,
    pagination,
    permissions
)


class GoalListView(generics.ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_class = GoalListFilters

    ordering = ['-priority', 'due_date']
    ordering_fields = ['due_date']

    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.filter(
            category__user=self.request.user,
            category__is_deleted=False
        ).exclude(status=Status.archived)


class GoalCreateView(generics.CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(category__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()
        return instance
