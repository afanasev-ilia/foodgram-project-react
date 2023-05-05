# from django.db.models import Avg, QuerySet
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets, serializers
from rest_framework.decorators import action
# from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.views import UserViewSet

from users.models import User
from recipes.models import Ingredient, Tag, Recipe
from core.utils import CustomPagination
from api.serializers import CustomUserSerializer, IngredientSerializer, TagSerializer
from api.permissions import IsAdminOrReadOnly
# from .filters import TitleFilter
# from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperUser,
#                           IsAuthorOrModeratorOrAdminOrSuperuser)


class CustomUsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    http_method_names = ['get', 'post']
    # lookup_field = 'username'
    # filter_backends = (SearchFilter,)
    # search_fields = ('username',)

    # @action(
    #     methods=['get'],
    #     detail=False,
    #     permission_classes=(IsAuthenticated, ),
    #     url_path='subscriptions',
    # )
    # def get_subscriptions(self, request):
    #     serializer = CustomUserSerializer(request.user)
    #     return Response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)

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
