from django.contrib import admin

from core.admin import BaseAdmin
from recipes.models import (Tag, Ingredient, Recipe, IngredientAmount,
                            Favourites, ShoppingList)


@admin.register(Recipe)
class RecipesAdmin(BaseAdmin):
    list_display = (
        'id',
        'author',
        'name',
    )
    search_fields = ('name',)
    list_filter = ('author','name','tags',)
    filter_horizontal = ('ingredients', 'tags',)


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


@admin.register(Favourites)
class FavouritesAdmin(BaseAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(ShoppingList)
class ShoppingListAdmin(BaseAdmin):
    list_display = (
        'user',
        'recipe',
    )
