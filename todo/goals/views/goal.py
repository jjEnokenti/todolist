from django_filters.rest_framework import DjangoFilterBackend
from goals.filters import GoalListFilters
from goals.models import (
    Goal,
    Status
)
from goals.serializers.goal import (
    GoalCreateSerializer,
    GoalManageSerializer
)
from rest_framework import (
    filters,
    generics,
    pagination,
    permissions
)


class GoalListView(generics.ListAPIView):
    serializer_class = GoalManageSerializer
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
            category__is_deleted=False,
            status__in=(1, 2, 3)
        )


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalManageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalManageSerializer

    def get_queryset(self):
        return Goal.objects.filter(category__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()
        return instance
