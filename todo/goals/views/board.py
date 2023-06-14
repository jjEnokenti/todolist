from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from goals.models import (
    Board,
    Goal
)
from goals.permissions import BoardPermission
from goals.serializers.board import (
    BoardCreateSerializer,
    BoardListSerializer,
    BoardSerializer
)
from rest_framework import (
    filters,
    generics,
    pagination,
    permissions
)


class BoardListView(generics.ListAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [permissions.IsAuthenticated, BoardPermission]
    pagination_class = pagination.LimitOffsetPagination

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]

    ordering = ['title']

    search_fields = ['title']

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated, BoardPermission]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardCreateView(generics.CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [permissions.IsAuthenticated, BoardPermission]
