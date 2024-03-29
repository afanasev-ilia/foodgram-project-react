from collections import OrderedDict
from typing import Dict, List

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

from api.fields import Base64ImageField
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj: User) -> bool:
        if (
            self.context.get('request')
            and not self.context.get('request').user.is_anonymous
        ):
            return (
                self.context.get('request')
                .user.follower.select_related()
                .filter(author=obj)
                .exists()
            )
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        read_only=True,
        source='ingredient_amount',
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj: Recipe) -> bool:
        if self.context.get('request').user.is_anonymous:
            return False
        return (
            self.context.get('request')
            .user.favorite.select_related()
            .filter(recipe=obj)
            .exists()
        )

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        if self.context.get('request').user.is_anonymous:
            return False
        return (
            self.context.get('request')
            .user.shopping_cart.select_related()
            .filter(recipe=obj)
            .exists()
        )


class IngredientAmounCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmounCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author',
        )

    def validate_ingredients(
        self,
        value: List[OrderedDict],
    ) -> List[OrderedDict]:
        if not value:
            raise serializers.ValidationError(
                'Это поле не может быть пустым.',
            )
        ingredients_list = []
        for ingredient_value in value:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_value['id'],
            )
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Ингридиенты не могут повторяться.',
                )
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value: List[OrderedDict]) -> List[OrderedDict]:
        if not value:
            raise serializers.ValidationError(
                'Это поле не может быть пустым.',
            )
        tags_list = []
        for tag in value:
            if tag in tags_list:
                raise serializers.ValidationError('Тэги не могут повторяться.')
            tags_list.append(tag)
        return value

    def ingredients_tags_set(
        self,
        ingredients: List[OrderedDict],
        tags: Tag,
        recipe: Recipe,
    ) -> None:
        recipe.tags.set(tags)
        IngredientAmount.objects.bulk_create(
            [
                IngredientAmount(
                    ingredient_id=ingredient_data['id'],
                    recipe=recipe,
                    amount=ingredient_data['amount'],
                )
                for ingredient_data in ingredients
            ],
        )

    def create(self, validated_data: Dict[str, OrderedDict]) -> Recipe:
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.ingredients_tags_set(
            ingredients,
            tags,
            recipe,
        )
        return recipe

    def update(
        self,
        instance: Recipe,
        validated_data: Dict[str, OrderedDict],
    ) -> Recipe:
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.ingredients_tags_set(ingredients, tags, instance)
        return super().update(instance, validated_data)


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('email', 'username')

    def get_is_subscribed(self, obj: User) -> bool:
        return (
            self.context.get('request')
            .user.follower.select_related()
            .filter(author=obj)
            .exists()
        )

    def get_recipes(self, obj: User) -> List[OrderedDict]:
        recipes = obj.recipes.select_related()
        limit = self.context.get('request').GET.get('recipes_limit')
        if limit:
            recipes = recipes[: int(limit)]
        return RecipeFollowSerializer(recipes, many=True).data

    def get_recipes_count(self, obj: User) -> int:
        return obj.recipes.count()

    def validate(self, data: OrderedDict) -> OrderedDict:
        if (
            self.context.get('request')
            .user.follower.select_related()
            .filter(author=self.instance)
            .exists()
        ):
            raise serializers.ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if self.context.get('request').user == self.instance:
            raise serializers.ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class RecipeFollowSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeFavoriteSerializer(RecipeFollowSerializer):
    def validate(self, data: OrderedDict) -> OrderedDict:
        if (
            self.context.get('request')
            .user.favorite.select_related()
            .filter(recipe=self.instance)
            .exists()
        ):
            raise serializers.ValidationError(
                detail='Рецепт уже есть в избранном',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class RecipeShoppingCartSerializer(RecipeFollowSerializer):
    def validate(self, data: OrderedDict) -> OrderedDict:
        if (
            self.context.get('request')
            .user.shopping_cart.select_related()
            .filter(recipe=self.instance)
            .exists()
        ):
            raise serializers.ValidationError(
                detail='Рецепт уже есть в списке покупок',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
