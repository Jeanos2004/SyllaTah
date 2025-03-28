from rest_framework import permissions

class IsLodgeAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'lodge_id'))

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.lodge_id

class CanManageLodgeAccommodations(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   hasattr(request.user, 'lodge_id'))

    def has_object_permission(self, request, view, obj):
        return obj.lodge.id == request.user.lodge_id

class CanManageLodgeActivities(permissions.BasePermission):
    message = "You do not have permission to manage activities for this lodge."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   hasattr(request.user, 'lodge_id'))

    def has_object_permission(self, request, view, obj):
        return obj.lodge.id == request.user.lodge_id