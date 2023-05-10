# from django.db.models import Avg, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404

# from rest_framework.views import APIView
from djoser.views import UserViewSet

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets  # , mixins, serializers
from rest_framework.decorators import action

# from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrSuperuser
from api.serializers import (
    CustomUserSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeFollowFavoriteSerializer,
    RecipeSerializer,
    TagSerializer,
)
from core.utils import CustomPageNumberPagination
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Follow, User

# from .filters import TitleFilter
# from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperUser,
#                           IsAuthorOrModeratorOrAdminOrSuperuser)


class CustomUsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination
    http_method_names = ['get', 'post', 'delete']

    @action(
        detail=False,
        methods=['get'],
        pagination_class=None,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get'], detail=False, permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        following = User.objects.filter(following__user=request.user)
        results = self.paginate_queryset(following)
        serializer = FollowSerializer(
            results,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            serializer = FollowSerializer(
                author,
                data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(
                Follow,
                user=request.user,
                author=author,
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthorOrAdminOrSuperuser,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            serializer = RecipeFollowFavoriteSerializer(
                recipe,
                data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            try:
                get_object_or_404(
                    Favorite,
                    user=request.user,
                    recipe=recipe,
                ).delete()
            except Http404:
                return Response(
                    {'detail': 'Рецепта нет в избранном'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(status=status.HTTP_204_NO_CONTENT)


# class GenresViewSet(CRDViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenresSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#     lookup_field = 'slug'


# class TitleViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all().annotate(
#         Avg('reviews__score')
#     ).order_by('id')
#     serializer_class = TitleSerializerCreate
#     permission_classes = (IsAdminOrReadOnly,)
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = TitleFilter

#     def get_serializer_class(self):
#         if self.request.method in ('POST', 'PATCH', 'DELETE',):
#             return TitleSerializerCreate
#         return TitleSerializerRead


# class CategoryViewSet(CRDViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#     lookup_field = 'slug'
#     permission_classes = (IsAdminOrReadOnly,)


# class ReviewsViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewsSerializer
#     permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser,)

#     def get_queryset(self):
#         title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
#         return title.reviews.all()

#     def perform_create(self, serializer):
#         serializer.save(
#             author=self.request.user,
#             title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
#         )


# class CommentsViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentsSerializer
#     permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser,)

#     def get_queryset(self) -> QuerySet:
#         review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
#         return review.comments.select_related('review')

#     def perform_create(self, serializer):
#         serializer.save(
#             author=self.request.user,
#             review=get_object_or_404(
#                 Review,
#                 id=self.kwargs.get('review_id'),
#                 title=self.kwargs.get('title_id'),
#             )
#         )
