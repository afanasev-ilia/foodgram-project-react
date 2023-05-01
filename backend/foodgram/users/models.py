from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
ADMIN = 'admin'

POSSIBLE_ROLES = [
    (USER, USER),
    (ADMIN, ADMIN)
]


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Электронная почта',
    )
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Имя пользователя',
    )
    role = models.CharField(
        choices=POSSIBLE_ROLES,
        default=USER,
        max_length=10,
        verbose_name='Роль'
    )
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        ordering = ['id']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
