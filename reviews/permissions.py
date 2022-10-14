from rest_framework import permissions
from rest_framework.views import Request, View
from reviews.models import Review


class IsAdmOrCritic(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_critic or request.user.is_superuser


class IsAdmOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Review):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id == request.user or request.user.is_superuser
