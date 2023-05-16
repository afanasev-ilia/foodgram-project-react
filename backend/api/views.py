from typing import Dict, Union

from django.db.models import Model, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from api.filters import CustomRecipeFilter
from api.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrSuperuser
from api.serializers import (
    CustomUserSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeFavoriteSerializer,
    RecipeSerializer,
    RecipeShoppingCartSerializer,
    TagSerializer,
)
from core.utils import CustomPageNumberPagination
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Follow, User


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
    def me(self, request: HttpRequest) -> HttpResponse:
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request: HttpRequest) -> HttpResponse:
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
    def subscribe(self, request: HttpRequest, id: int) -> HttpResponse:
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

        get_object_or_404(Follow, user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-created')
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthorOrAdminOrSuperuser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilter

    def perform_create(
        self,
        serializer: Dict[str, Union[str, int, float]],
    ) -> None:
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    def favorite_shopping_cart(
            self,
            request: HttpRequest,
            pk: int,
            serializer: ModelSerializer,
            model: Model,
    ) -> HttpResponse:
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            serializer = serializer(
                recipe,
                data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            model.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        get_object_or_404(model, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request: HttpRequest, pk: int) -> HttpResponse:
        return self.favorite_shopping_cart(
            request,
            pk,
            RecipeFavoriteSerializer,
            Favorite,
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request: HttpRequest, pk: int) -> HttpResponse:
        return self.favorite_shopping_cart(
            request,
            pk,
            RecipeShoppingCartSerializer,
            ShoppingCart,
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request: HttpRequest) -> HttpResponse:
        ingredients = (
            IngredientAmount.objects.filter(
                recipe__shopping_cart__user=request.user,
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(sum_amount=Sum('amount'))
            .values_list(
                'ingredient__name',
                'sum_amount',
                'ingredient__measurement_unit',
            )
        )
        shopping_cart = []
        for ingredient in ingredients:
            shopping_cart.append('{} - {} {}.\n'.format(*ingredient))
        filename = 'shopping-list.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename,
        )
        return response
