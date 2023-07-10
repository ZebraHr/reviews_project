from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import ADMIN, CHOICES, MODERATOR, USER


class User(AbstractUser):
    """Кастомная модель пользователя."""

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )
    password = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Статус пользователя',
        max_length=25,
        choices=CHOICES,
        default=USER
    )
    bio = models.TextField(
        'Информация о пользователе',
        blank=True,
    )
    confirmation_code = models.CharField(max_length=150)

    @property
    def is_admin(self):
        return (self.role == ADMIN or self.is_staff
                or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
