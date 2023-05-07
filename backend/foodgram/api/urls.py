from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CustomUsersViewSet,
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
)


router = DefaultRouter()
router.register('v1/users', CustomUsersViewSet, basename='users')
router.register('v1/tags', TagViewSet, basename='tags')
router.register('v1/ingredients', IngredientViewSet, basename='ingredients')
router.register('v1/recipes', RecipeViewSet, basename='recipes')
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
    path('v1/auth/', include('djoser.urls.authtoken')),
]
