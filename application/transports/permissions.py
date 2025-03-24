from rest_framework import permissions

class TransportPermissions(permissions.BasePermission):
    """
    Permissions spécifiques pour les transports:
    - Lecture: Tous les utilisateurs authentifiés
    - Création/Modification/Suppression: Administrateurs uniquement
    
    Les informations de transport sont des données de référence qui ne devraient
    être modifiées que par les administrateurs.
    """
    
    def has_permission(self, request, view):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Création/Modification/Suppression réservées aux administrateurs
        return request.user and request.user.is_staff
