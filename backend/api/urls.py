from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CustomUsersViewSet,
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
)


router = DefaultRouter()
router.register('users', CustomUsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
# router.register(
#     'v1/titles/(?P<title_id>[0-9]+)/reviews',
#     ReviewsViewSet,
#     basename='reviews',
# )
# router.register(
#     'v1/titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
#     CommentsViewSet,
#     basename='comments',
# )

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
