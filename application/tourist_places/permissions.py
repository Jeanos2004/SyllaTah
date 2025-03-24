from rest_framework import permissions

class TouristPlacePermissions(permissions.BasePermission):
    """
    Permissions spécifiques pour les lieux touristiques:
    - Lecture: Tous les utilisateurs authentifiés
    - Création/Modification/Suppression: Administrateurs uniquement
    
    Les lieux touristiques sont des données de référence qui ne devraient
    être modifiées que par les administrateurs.
    """
    
    def has_permission(self, request, view):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Création/Modification/Suppression réservées aux administrateurs
        return request.user and request.user.is_staff
        
class ReviewPermissions(permissions.BasePermission):
    """
    Permissions spécifiques pour les avis sur les lieux touristiques:
    - Lecture: Tous les utilisateurs authentifiés
    - Création: Utilisateurs authentifiés
    - Modification/Suppression: Auteur de l'avis ou administrateur
    """
    
    def has_permission(self, request, view):
        # Tous les utilisateurs authentifiés peuvent lire ou créer un avis
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        # Modification/Suppression uniquement par l'auteur ou un administrateur
        return (hasattr(obj, 'user') and obj.user == request.user) or request.user.is_staff
