from django.db import models
from django.contrib.auth.models import AbstractUser

# Статусы пользователя

STATUS = {
    'admin': 'admin',
    'moderator': 'moderator',
    'user': 'user'
}


class User(AbstractUser):
    """Кастомная модель пользователя."""

    first_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254
    )
    role = models.CharField(
        'Статус пользователя',
        max_length=20,
        choices=STATUS,
        default=STATUS['user']
    )
    confirmation_code = models.CharField(max_length=255)

    @property
    def is_admin(self):
        return (
                self.role == STATUS['admin'] or self.is_staff
                or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == STATUS['moderator']

    def __str__(self):
        return self.username
