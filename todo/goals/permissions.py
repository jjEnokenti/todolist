from goals.models import BoardParticipant
from rest_framework import permissions


permission_roles = (
    BoardParticipant.Role.owner,
    BoardParticipant.Role.writer
)


class BoardPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        attrs = {'user': request.user, 'board': obj}

        if request.method not in permissions.SAFE_METHODS:
            attrs['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**attrs).exists()


class GoalCategoryPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        attrs = {'user': request.user, 'board': obj.board}

        if request.method not in permissions.SAFE_METHODS:
            attrs['role__in'] = permission_roles
        return BoardParticipant.objects.filter(**attrs).exists()


class GoalPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        attrs = {'user': request.user, 'board': obj.category.board}

        if request.method not in permissions.SAFE_METHODS:
            attrs['role__in'] = permission_roles

        return BoardParticipant.objects.filter(**attrs).exists()


class CommentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        attrs = {'user': request.user, 'board': obj.goal.category.board}

        if request.method not in permissions.SAFE_METHODS:
            attrs['role__in'] = permission_roles

        return BoardParticipant.objects.filter(**attrs).exists()
