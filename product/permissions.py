from rest_framework import permissions

from authentication.models import ADMIN, SELLER


class RBACCategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role == ADMIN:
            return True
        return False


class IsSellerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in (ADMIN, SELLER)

    def has_object_permission(self, request, view, obj):
        return request.user.role == ADMIN or (request.user.role == SELLER and obj.seller == request.user)
