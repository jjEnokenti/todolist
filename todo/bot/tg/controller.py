from typing import Any

from bot.models import TgUser
from bot.tg.dc import (
    Message,
    User,
)
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from goals.models import (
    Board,
    BoardParticipant,
    Goal,
    GoalCategory,
)


USER_MODEL = get_user_model()


class Controller:
    def __init__(self, message: Message, allowed_commands: list | None = None):
        self.allowed_commands = allowed_commands or ['/create', '/cancel', '/goals', '/start']
        self.message = message
        self.user: User = message.from_user

        self.tg_user, self.created = TgUser.objects.get_or_create(
            tg_username=self.user.username or self.user.first_name,
            tg_user_id=self.user.id,
            chat_id=self.message.chat.id
        )

    def create_goal(self, title: str, pk: Any) -> Goal:

        category = self.get_category(pk)
        new_goal = Goal.objects.create(
            category_id=category.id,
            title=title
        )

        return new_goal

    def get_goals(self) -> QuerySet[Goal] | None:
        goals = Goal.objects.filter(
            category__board__participants__user=self.tg_user.user,
            category__board__participants__role=BoardParticipant.Role.owner

        ).exclude(
            status=Goal.Status.archived
        )

        return goals

    def get_category(self, pk: int) -> GoalCategory | None:
        return GoalCategory.objects.filter(
            pk=pk,
            board__participants__user=self.tg_user.user,
            board__participants__role=BoardParticipant.Role.owner,
            is_deleted=False).first()

    def get_categories(self) -> QuerySet[GoalCategory]:
        categories = GoalCategory.objects.filter(
            board__participants__user=self.tg_user.user,
            board__participants__role=BoardParticipant.Role.owner,
            is_deleted=False
        )
        if not categories:
            board = Board.objects.filter(
                participants__user=self.tg_user.user,
                participants__role=BoardParticipant.Role.owner,
                is_deleted=False
            ).first()
            if not board:
                board = Board.objects.create(title='Мои цели')
                BoardParticipant.objects.create(board=board, user=self.tg_user.user, role=BoardParticipant.Role.owner)
            categories = [GoalCategory.objects.create(title='Новая категория', user=self.tg_user.user, board=board)]

        return categories
