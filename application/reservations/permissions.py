from rest_framework import permissions

class ReservationPermissions(permissions.BasePermission):
    """
    Permissions spécifiques pour les réservations:
    - Lecture: Propriétaire de la réservation ou administrateur
    - Création: Utilisateurs authentifiés
    - Modification/Suppression: Propriétaire de la réservation ou administrateur
    
    Cette permission est plus restrictive car les réservations contiennent
    des données personnelles des utilisateurs.
    """
    
    def has_permission(self, request, view):
        # Tous les utilisateurs authentifiés peuvent créer une réservation
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Seul le propriétaire de la réservation ou un administrateur peut la consulter/modifier/supprimer
        return (hasattr(obj, 'user') and obj.user == request.user) or request.user.is_staff
