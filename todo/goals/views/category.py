from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import (
    filters,
    generics,
    pagination,
    permissions,
)

from goals.models import (
    Goal,
    GoalCategory,
)
from goals.permissions import GoalCategoryPermission
from goals.serializers.category import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
)


@extend_schema(
    tags=['goal categories'],
    description='New goal category create method',
    summary='create new goal category'
)
class GoalCategoryCreateView(generics.CreateAPIView):
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=['goal categories'],
    description='Response list of goal categories',
    summary='list of goal categories'
)
class GoalCategoryListView(generics.ListAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['board']

    ordering = ['title']
    ordering_fields = ['title', 'created']

    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').select_related('board').filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )


@extend_schema(tags=['goal categories'])
class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermission]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goal_set.update(status=Goal.Status.archived)

            for goal in instance.goal_set.filter(category=instance):
                goal.comment_set.filter(goal=goal).delete()
