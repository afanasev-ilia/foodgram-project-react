from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from core.utils import truncatechars

User = get_user_model()


class Tags(models.Model):
    name = models.CharField(
        'название тега',
        max_length=200,
        unique=True,
        help_text='укажите название тега',
    )
    color = models.CharField(
        'цветовой HEX-код тега',
        max_length=10,
        unique=True,
        help_text='укажите цветовой HEX-код тега',
    )
    slug = models.SlugField(
        'текстовый идентификатор тега',
        unique=True,
        help_text='укажите текстовый идентификатор тега',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return truncatechars(self.name, settings.NUMCATECHARS)


class Ingredients(models.Model):
    name = models.CharField(
        'название ингредиента',
        max_length=200,
        unique=True,
        help_text='укажите название ингредиента',
    )
    measurement_unit = models.CharField(
        'единицы измерения ингредиента',
        max_length=200,
        unique=True,
        help_text='укажите единицы измерения ингредиента',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self) -> str:
        return truncatechars(self.name, settings.NUMCATECHARS)


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
        help_text='укажите автора',
    )
    name = models.CharField(
        'название рецепта',
        max_length=200,
        help_text='укажите название рецепта',
    )
    image = models.ImageField(
        'изображение',
        upload_to='recipes/',
        help_text='добавьте изображение',
    )
    text = models.TextField(
        verbose_name='текст',
        help_text='введите текст',
    )
    ingredients = models.ManyToManyField(Ingredients)
    tags = models.ManyToManyField(Tags)
    cooking_time = models.IntegerField(
        verbose_name='время приготовления в минутах',
        help_text='укажите время приготовления в минутах',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return truncatechars(self.name, settings.NUMCATECHARS)
