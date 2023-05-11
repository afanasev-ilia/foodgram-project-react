# from django.http import HttpRequest
# from django.core import exceptions as django_exceptions
# from rest_framework.generics import get_object_or_404
# from rest_framework.validators import UniqueValidator
import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from recipes.models import (
    Ingredient,
    IngredientAmount,
    Recipe,
    Tag,
    Favorite,
    ShoppingCart,
)
from users.models import Follow, User


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

    def get_is_subscribed(self, obj):
        if (
            self.context.get('request')
            and not self.context.get('request').user.is_anonymous
        ):
            return (
                self.context.get('request')
                .user.follower.select_related('following')
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
        fields = ('name', 'measurement_unit')


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


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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

    def get_is_favorited(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return (
            self.context.get('request')
            .user.favorite.select_related('recipe')
            .filter(recipe=obj)
            .exists()
        )

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return (
            self.context.get('request')
            .user.shopping_cart.select_related('recipe')
            .filter(recipe=obj)
            .exists()
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        read_only=True,
        source='ingredient_amount',
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )


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

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request')
            .user.follower.select_related('following')
            .filter(author=obj)
            .exists()
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.select_related('author')
        limit = self.context.get('request').GET.get('recipes_limit')
        if limit:
            recipes = recipes[: int(limit)]
        return RecipeFollowSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Follow.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise ValidationError(
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

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if Favorite.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError(
                detail='Рецепт уже есть в избранном',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class RecipeShoppingCartSerializer(RecipeFollowSerializer):

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError(
                detail='Рецепт уже есть в списке покупок',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('name', 'slug')
#         lookup_field = 'slug'
#         extra_kwargs = {
#             'url': {'lookup_field': 'slug'}
#         }


# class TitleSerializerRead(serializers.ModelSerializer):
#     '''Сериализатор для работы с title при LIST/RETRIEVE.'''
#     category = CategorySerializer(read_only=True)
#     genre = GenresSerializer(many=True, read_only=True)
#     rating = serializers.IntegerField(
#         source='reviews__score__avg', read_only=True
#     )

#     class Meta:
#         fields = '__all__'
#         model = Title


# class TitleSerializerCreate(serializers.ModelSerializer):
#     '''Сериализатор для работы с title при POST/PUT/PATCH.'''
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(),
#         slug_field='slug'
#     )
#     genre = serializers.SlugRelatedField(
#         queryset=Genre.objects.all(),
#         slug_field='slug',
#         many=True
#     )

#     class Meta:
#         fields = '__all__'
#         model = Title


# class ReviewsSerializer(serializers.ModelSerializer):
#     title = serializers.SlugRelatedField(
#         slug_field='name',
#         read_only=True,
#     )
#     author = serializers.SlugRelatedField(
#         default=serializers.CurrentUserDefault(),
#         slug_field='username',
#         read_only=True
#     )

#     def get_author(self, request: HttpRequest) -> User:
#         return self.context.get('request').user

#     def get_title(self, request: HttpRequest) -> Title:
#         return get_object_or_404(
#             Title,
#             pk=self.context.get('view').kwargs.get('title_id'),
#         )

#     def validate(self, data):
#         if self.context.get('request').method == 'POST':
#             if Review.objects.filter(
#                     title=self.get_title(self),
#                     author=self.get_author(self),
#             ).exists():
#                 raise ValidationError(
#                     'На одно произведение можно оставить только один отзыв',
#                 )
#         return data

#     class Meta:
#         model = Review
#         fields = ('author', 'title', 'id', 'text', 'pub_date', 'score')


# class CommentsSerializer(serializers.ModelSerializer):
#     review = serializers.SlugRelatedField(
#         slug_field='text',
#         read_only=True
#     )
#     author = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True
#     )

#     class Meta:
#         model = Comment
#         fields = ('author', 'review', 'id', 'text', 'pub_date')
