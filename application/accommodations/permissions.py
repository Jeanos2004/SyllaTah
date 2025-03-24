from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre uniquement aux administrateurs de créer, 
    modifier ou supprimer des objets. Les utilisateurs authentifiés peuvent seulement lire.
    """
    
    def has_permission(self, request, view):
        # Autoriser les requêtes GET, HEAD ou OPTIONS pour tout utilisateur authentifié
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Autoriser les requêtes POST, PUT, DELETE uniquement pour les administrateurs
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission personnalisée pour permettre aux propriétaires d'un objet ou aux administrateurs
    de le modifier ou le supprimer. Utile pour les réservations ou les avis.
    """
    
    def has_object_permission(self, request, view, obj):
        # Autoriser les requêtes GET, HEAD ou OPTIONS pour tout utilisateur authentifié
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        # Vérifier si l'utilisateur est le propriétaire de l'objet ou un administrateur
        # Note: Ajustez 'owner' au champ approprié dans votre modèle si nécessaire
        return (hasattr(obj, 'owner') and obj.owner == request.user) or request.user.is_staff
