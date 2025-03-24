from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission globale pour permettre uniquement aux administrateurs de créer, 
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
    Permission globale pour permettre aux propriétaires d'un objet ou aux administrateurs
    de le modifier ou le supprimer.
    """
    
    def has_object_permission(self, request, view, obj):
        # Autoriser les requêtes GET, HEAD ou OPTIONS pour tout utilisateur authentifié
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
            
        # Vérifier si l'utilisateur est le propriétaire de l'objet ou un administrateur
        if hasattr(obj, 'owner'):
            return obj.owner == request.user or request.user.is_staff
        elif hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
        elif hasattr(obj, 'author'):
            return obj.author == request.user or request.user.is_staff
        
        # Si aucun champ de propriétaire n'est trouvé, seuls les administrateurs peuvent modifier
        return request.user.is_staff

class IsAuthenticatedWithToken(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est authentifié avec un token valide.
    Utile pour les API utilisées par le frontend NextJS.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            'Authorization' in request.headers or 
            request.auth is not None
        )
