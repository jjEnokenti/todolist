from goals.models import BoardParticipant
from rest_framework import permissions


class BoardPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        attrs = {'user': request.user, 'board': obj}

        if request.method not in permissions.SAFE_METHODS:
            attrs['role'] = obj.participants.model.Role.owner
        return BoardParticipant.objects.filter(**attrs).exists()


class GoalCategoryPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        attrs = {'user': request.user, 'board': obj.board}

        if request.method not in permissions.SAFE_METHODS:
            attrs['role__in'] = (obj.board.participants.model.Role.owner,
                                 obj.board.participants.model.Role.writer,)
        return BoardParticipant.objects.filter(**attrs).exists()
