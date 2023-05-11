from typing import Any

from django.http import HttpRequest
from rest_framework import permissions, viewsets


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(
        self,
        request: HttpRequest,
        unused: viewsets,
    ) -> bool:
        del unused
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_staff
        )


class IsAuthorOrAdminOrSuperuser(permissions.BasePermission):
    def has_permission(
        self,
        request: HttpRequest,
        unused: viewsets,
    ) -> bool:
        del unused
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request: HttpRequest,
        unused: viewsets,
        obj: Any,
    ) -> bool:
        del unused
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
            or request.user.is_superuser
        )
