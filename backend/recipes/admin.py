from django.contrib import admin

from core.admin import BaseAdmin
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag,
)


@admin.register(Recipe)
class RecipesAdmin(BaseAdmin):
    list_display = (
        'id',
        'author',
        'name',
    )
    search_fields = ('name',)
    list_filter = (
        'author',
        'name',
        'tags',
    )
    filter_horizontal = (
        'ingredients',
        'tags',
    )


@admin.register(Tag)
class TagsAdmin(BaseAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Ingredient)
class IngredientsAdmin(BaseAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(BaseAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Favorite)
class FavouritesAdmin(BaseAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(ShoppingCart)
class ShoppingListAdmin(BaseAdmin):
    list_display = (
        'user',
        'recipe',
    )
