from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


user = get_user_model()


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


class GoalCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(user, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    title = models.CharField(verbose_name='Название', max_length=155)
    description = models.CharField(verbose_name='Описание', max_length=500)
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
    deadline = models.DateTimeField(
        verbose_name='Дата дедлайна',
        default=timezone.now() + timezone.timedelta(days=2)
    )
    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
