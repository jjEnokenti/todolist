from django.contrib.auth import get_user_model
from django.db import models


user = get_user_model()


class DateTimeMixin(models.Model):
    """Абстрактная модель даты создания и обновления записи."""

    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)


class Board(DateTimeMixin):
    """Модель доски."""

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def __str__(self):
        return self.title


class BoardParticipant(DateTimeMixin):
    """Модель участника доски."""

    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='participants'
    )
    user = models.ForeignKey(
        user,
        verbose_name='Участник',
        on_delete=models.PROTECT,
        related_name='participants'
    )
    role = models.PositiveSmallIntegerField(
        verbose_name='Роль',
        choices=Role.choices,
        default=Role.owner
    )


class GoalCategory(DateTimeMixin):
    """Модель категории целей."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(user, verbose_name='Автор', on_delete=models.PROTECT)
    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.CASCADE,
        related_name='categories'
    )
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def __str__(self):
        return self.title


class Goal(DateTimeMixin):
    """Модель целей."""

    class Status(models.IntegerChoices):
        to_do = (1, 'К выполнению')
        in_progress = (2, 'В процессе')
        done = (3, 'Готово')
        archived = (4, 'В архиве')

    class Priority(models.IntegerChoices):
        low = (1, 'Низкий')
        medium = (2, 'Средний')
        high = (3, 'Высокий')
        critical = (4, 'Критический')

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    title = models.CharField(verbose_name='Название', max_length=155)
    description = models.CharField(
        verbose_name='Описание',
        max_length=500,
        null=True,
        blank=True
    )
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет',
        choices=Priority.choices,
        default=Priority.medium
    )
    due_date = models.DateTimeField(
        verbose_name='Дата дедлайна',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Comment(DateTimeMixin):
    """Модель комментариев к цели."""

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(user, verbose_name='Автор', on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
