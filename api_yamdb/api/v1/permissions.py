from rest_framework.permissions import BasePermission, SAFE_METHODS
from reviews.models import User


class IsOwnerAdminModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.role == User.ADMIN
                or request.user.role == User.MODERATOR)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and request.user.role == User.ADMIN
            or user.is_superuser
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
