from django.db.models import Prefetch

class OptimizedQuerySetMixin:
    """
    Mixin pour optimiser les requêtes avec select_related et prefetch_related.
    À utiliser dans les ViewSets pour réduire le nombre de requêtes SQL.
    """
    select_related_fields = []
    prefetch_related_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Appliquer select_related pour les relations ForeignKey
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        
        # Appliquer prefetch_related pour les relations ManyToMany ou reverse ForeignKey
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
            
        return queryset


class SerializerByActionMixin:
    """
    Mixin pour sélectionner automatiquement le sérialiseur approprié en fonction de l'action.
    Définir serializer_classes comme un dictionnaire avec les actions comme clés.
    """
    serializer_classes = {
        'list': None,
        'retrieve': None,
        'create': None,
        'update': None,
        'partial_update': None,
    }
    
    def get_serializer_class(self):
        """Sélectionne le sérialiseur approprié en fonction de l'action"""
        return self.serializer_classes.get(self.action, self.serializer_class)
