from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour les articles de blog:
    - Lecture: Tous les utilisateurs authentifiés
    - Modification/Suppression: Uniquement l'auteur de l'article ou un administrateur
    """
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        # Modification/Suppression uniquement par l'auteur ou un administrateur
        return (obj.author == request.user) or (request.user and request.user.is_staff)

class BlogAdminPermission(permissions.BasePermission):
    """
    Permission pour la gestion des catégories et tags de blog:
    - Lecture: Tous les utilisateurs authentifiés
    - Création/Modification/Suppression: Administrateurs uniquement
    """
    def has_permission(self, request, view):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        # Création/Modification/Suppression réservées aux administrateurs
        return request.user and request.user.is_staff