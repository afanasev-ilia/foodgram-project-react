import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models


# USER = 'user'
# ADMIN = 'admin'

# # possible user roles in application
# POSSIBLE_ROLES = [
#     (USER, USER),
#     (ADMIN, ADMIN)
# ]


class User(AbstractUser):
    username = models.CharField(
        unique=True, max_length=150,
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        max_length=254,
        verbose_name='Электронная почта',
    )
    first_name = models.CharField(
        blank=True, max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия',
    )
    # role = models.CharField(
    #     choices=POSSIBLE_ROLES,
    #     default=USER,
    #     max_length=10,
    #     verbose_name='Роль'
    # )

    def __str__(self):
        return self.username

    # @property
    # def is_user(self):
    #     return self.role == USER

    # @property
    # def is_admin(self):
    #     return self.role == ADMIN

    # @property
    # def confirmation_code(self):
    #     return hashlib.md5(self.username.encode()).hexdigest()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
