from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.Model):
    ADMIN = 'admin'
    USER = 'user'
    ROLES = ((ADMIN, 'admin'), (USER, 'user'))


class User(AbstractUser):
    role = models.CharField(max_length=5, choices=UserRole.ROLES, default=UserRole.USER)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
