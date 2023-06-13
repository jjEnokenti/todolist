from django.contrib.auth import get_user_model
from django.db import models


user = get_user_model()


class DateTimeMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)


class GoalCategory(DateTimeMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(user, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def __str__(self):
        return self.title


class Goal(DateTimeMixin):
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
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(user, verbose_name='Автор', on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
