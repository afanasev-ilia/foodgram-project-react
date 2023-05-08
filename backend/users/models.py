from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import DefaultModel


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    email = models.EmailField(
        'электронная почта',
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        'Имя пользователя',
        unique=True,
        max_length=150,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username


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
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
