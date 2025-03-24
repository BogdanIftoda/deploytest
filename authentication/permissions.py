from rest_framework import permissions

from authentication.models import ADMIN


class RBACUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == ADMIN or obj == user:
            return True
        return False
