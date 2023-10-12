from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'У вас нет прав владельца!'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        raise PermissionDenied(self.message)
