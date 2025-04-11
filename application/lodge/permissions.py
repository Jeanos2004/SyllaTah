from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

class IsLodgeAdmin(permissions.BasePermission):
    message = "You must be a lodge administrator to perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'lodge_id') and
            request.user.is_lodge_admin
        )

    def has_object_permission(self, request, view, obj):
        try:
            return obj.id == request.user.lodge_id
        except ObjectDoesNotExist:
            return False

class CanManageLodgeAccommodations(permissions.BasePermission):
    message = "You don't have permission to manage lodge accommodations."

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'lodge_id') and
            (request.user.is_lodge_admin or request.user.has_perm('lodge.manage_accommodations'))
        )

    def has_object_permission(self, request, view, obj):
        try:
            return obj.lodge.id == request.user.lodge_id
        except ObjectDoesNotExist:
            return False

class CanManageLodgeActivities(permissions.BasePermission):
    message = "You don't have permission to manage lodge activities."

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'lodge_id') and
            (request.user.is_lodge_admin or request.user.has_perm('lodge.manage_activities'))
        )

    def has_object_permission(self, request, view, obj):
        try:
            return obj.lodge.id == request.user.lodge_id
        except ObjectDoesNotExist:
            return False