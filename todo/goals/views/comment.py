from goals.models import Comment
from goals.serializers.comment import (
    CommentCreateSerializer,
    CommentSerializer
)
from rest_framework import (
    filters,
    generics,
    pagination,
    permissions
)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    ordering = ['-created']

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user,
            goal=self.request.query_params.get('goal')
        )


class CommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user
        )
