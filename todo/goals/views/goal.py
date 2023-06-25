from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from goals.filters import GoalListFilters
from goals.models import Goal
from goals.permissions import GoalPermission
from goals.serializers.goal import (
    GoalCreateSerializer,
    GoalSerializer,
)
from rest_framework import (
    filters,
    generics,
    pagination,
    permissions,
)


@extend_schema(
    tags=['goals'],
    description='Response list of goals',
    summary='list of goals'
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

    ordering = ['-priority']
    ordering_fields = ['-priority', 'due_date']

    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


@extend_schema(
    tags=['goals'],
    description='Create new goal method',
    summary='create new goal'
)
class GoalCreateView(generics.CreateAPIView):
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=['goals'])
class GoalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, GoalPermission]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.select_related('category').filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.status = Goal.Status.archived
            instance.save(update_fields=('status',))
            instance.comment_set.filter(goal=instance).delete()
