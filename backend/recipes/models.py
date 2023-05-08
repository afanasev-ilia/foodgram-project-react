from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from core.models import DefaultModel
from core.utils import truncatechars

User = get_user_model()


class Tag(DefaultModel):
    name = models.CharField(
        'название тега',
        max_length=200,
        unique=True,
        help_text='укажите название тега',
    )
    color = models.CharField(
        'цветовой HEX-код тега',
        max_length=7,
        unique=True,
        help_text='укажите цветовой HEX-код тега',
    )
    slug = models.SlugField(
        'текстовый идентификатор тега',
        max_length=200,
        unique=True,
        help_text='укажите текстовый идентификатор тега',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return truncatechars(self.name, settings.NUMCATECHARS)


class Ingredient(DefaultModel):
    name = models.CharField(
        'название ингредиента',
        max_length=200,
        help_text='укажите название ингредиента',
    )
    measurement_unit = models.CharField(
        'единицы измерения ингредиента',
        max_length=200,
        help_text='укажите единицы измерения ингредиента',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self) -> str:
        return truncatechars(self.name, settings.NUMCATECHARS)


class Recipe(DefaultModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
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
        'текстовое описание',
        help_text='введите текстовое описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='ингредиенты',
        help_text='выберите ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги',
        help_text='выберите теги',
    )
    cooking_time = models.IntegerField(
        'время приготовления (в минутах)',
        validators=[
            MinValueValidator(1, message='значение должно быть больше 1')
        ],
        help_text='укажите время приготовления (в минутах)',
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return truncatechars(self.name, settings.NUMCATECHARS)


class IngredientAmount(DefaultModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='укажите рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
        help_text='укажите ингредиент',
    )
    amount = models.IntegerField(
        'количество',
        validators=[
            MinValueValidator(1, message='значение должно быть больше 1')
        ],
    )

    class Meta:
        default_related_name = 'ingredient_amount'
        verbose_name = 'Количеcтво ингредиента в рецепте'
        verbose_name_plural = 'Количеcтво ингредиента в рецепте'

    def __str__(self):
        return (
            f'{self.ingredient} ({self.ingredient.measurement_unit})'
            f' - {self.amount} '
        )


class Favorite(DefaultModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='укажите пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='укажите рецепт для избранного',
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite',
        )
        default_related_name = 'favorite'
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'

    def __str__(self) -> str:
        return f'{self.recipe} добавлен в избранное пользователя {self.user}'


class ShoppingCart(DefaultModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='укажите пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='укажите рецепт для списка покупок',
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_shopping_cart',
        )
        default_related_name = 'shopping_cart'
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'

    def __str__(self) -> str:
        return (
            f'{self.recipe} добавлен в список покупок пользователя {self.user}'
        )
