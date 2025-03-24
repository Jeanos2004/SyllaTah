from rest_framework import permissions

class ActivityPermissions(permissions.BasePermission):
    """
    Permissions spécifiques pour les activités touristiques:
    - Lecture: Tous les utilisateurs authentifiés
    - Création: Administrateurs uniquement
    - Modification/Suppression: Administrateurs uniquement
    """
    
    def has_permission(self, request, view):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Création/Modification/Suppression réservées aux administrateurs
        return request.user and request.user.is_staff
