# from django.http import HttpRequest
# from django.core import exceptions as django_exceptions
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
)
from djoser.serializers import UserSerializer, UserCreateSerializer
# from rest_framework.generics import get_object_or_404
# from rest_framework.validators import UniqueValidator

from users.models import User, Follow
from recipes.models import Ingredient, Tag, Recipe, IngredientAmount


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        if (
            self.context.get("request")
            and not self.context["request"].user.is_anonymous
        ):
            return Follow.objects.filter(
                user=self.context["request"].user, author=obj
            ).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = CharField(required=True)

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


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientAmountSerializer(ModelSerializer):
    class Meta:
        model = IngredientAmount
        fields = ('id', 'name')


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True, read_only=True)  # SerializerMethodField()
    # # image = Base64ImageField()
    # is_favorited = SerializerMethodField(read_only=True)
    # is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            #     'is_favorited',
            #     'is_in_shopping_cart',
            'name',
            #     'image',
            'text',
            'cooking_time',
        )


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('name', 'slug')
#         lookup_field = 'slug'
#         extra_kwargs = {
#             'url': {'lookup_field': 'slug'}
#         }


# class TitleSerializerRead(serializers.ModelSerializer):
#     """Сериализатор для работы с title при LIST/RETRIEVE."""
#     category = CategorySerializer(read_only=True)
#     genre = GenresSerializer(many=True, read_only=True)
#     rating = serializers.IntegerField(
#         source='reviews__score__avg', read_only=True
#     )

#     class Meta:
#         fields = '__all__'
#         model = Title


# class TitleSerializerCreate(serializers.ModelSerializer):
#     """Сериализатор для работы с title при POST/PUT/PATCH."""
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
