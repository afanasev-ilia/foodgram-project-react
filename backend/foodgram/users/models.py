from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import DefaultModel


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
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

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Follow(DefaultModel):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='подписчик',
        help_text='укажите подписчика',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
        help_text='укажите автора на которого подписываются',
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follow',
        )
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.author.username}'
