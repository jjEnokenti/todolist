from core.serializers import UserProfileSerializer
from goals.models import (
    BoardParticipant,
    Comment,
)
from rest_framework import (
    exceptions,
    serializers,
)


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer.

    override update method for
    checking whether a comment belongs to the user.
    """
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'goal': {'read_only': True},
        }

    def update(self, instance, validated_data):
        if instance.user != self.context['request'].user:
            raise exceptions.PermissionDenied('You do not have permissions to update this comment.')

        return super().update(instance, validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """Comment create serializer.

    define goal validate method
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'user': {'read_only': True},
        }

    def validate_goal(self, goal):
        if goal.status == goal.Status.archived:
            raise serializers.ValidationError({'create error': 'goal is deleted.'})
        if BoardParticipant.objects.filter(
                board=goal.category.board,
                user=self.context['request'].user,
                role__in=(
                        BoardParticipant.Role.owner,
                        BoardParticipant.Role.writer
                )
        ).exists():
            return goal

        raise exceptions.PermissionDenied('You do not have permissions to write comments.')
