from django.contrib import admin

from core.admin import BaseAdmin
from users.models import Follow, User


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    list_editable = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
    )
    list_filter = (
        'username',
        'email',
    )


@admin.register(Follow)
class FollowAdmin(BaseAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = ('user',)
    list_filter = ('author',)
