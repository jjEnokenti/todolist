from django_filters.rest_framework import DjangoFilterBackend
from goals.models import Comment
from goals.permissions import CommentPermission
from goals.serializers.comment import (
    CommentCreateSerializer,
    CommentSerializer,
)
from rest_framework import (
    exceptions,
    filters,
    generics,
    pagination,
    permissions,
)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = ['goal']

    ordering = ['-created']

    def get_queryset(self):
        return Comment.objects.select_related('goal').select_related('user').filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermission]

    def get_queryset(self):
        return Comment.objects.select_related('goal').select_related('user').filter(
            goal__category__board__participants__user=self.request.user
        )

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise exceptions.PermissionDenied('You do not have permissions to delete this comment.')
        return super().perform_destroy(instance)
