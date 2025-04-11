from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que le propriétaire d'un objet ou un administrateur à y accéder.
    """
    def has_object_permission(self, request, view, obj):
        # Les administrateurs ont toujours accès
        if request.user.is_staff:
            return True
            
        # Vérifier si l'objet a un attribut 'user' et si c'est l'utilisateur actuel
        return hasattr(obj, 'user') and obj.user == request.user


class ReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que les méthodes de lecture (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser les utilisateurs authentifiés à modifier,
    mais permettre à tous de lire.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_authenticated
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que le propriétaire d'un objet à le modifier,
    mais permettre à tous de le lire.
    """
    def has_object_permission(self, request, view, obj):
        # Les méthodes de lecture sont toujours autorisées
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Vérifier si l'objet a un attribut 'user' et si c'est l'utilisateur actuel
        return hasattr(obj, 'user') and obj.user == request.user
