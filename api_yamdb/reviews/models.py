<<<<<<<< HEAD:api_yamdb/reviews/models.py
========
from django.db import models

>>>>>>>> origin/feature/users_model_and_jwt:api_yamdb/api/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import CHOICES, USER, ADMIN, MODERATOR


class User(AbstractUser):
    """Кастомная модель пользователя."""

    first_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=100
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
        return (
                self.role == ADMIN or self.is_staff
                or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
