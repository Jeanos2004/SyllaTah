from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ViewSet

class CachedViewSetMixin:
    """
    Mixin pour ajouter du cache aux ViewSets.
    Utilise le décorateur cache_page de Django pour mettre en cache les réponses.
    """
    cache_timeout = 60 * 15  # 15 minutes par défaut
    
    @method_decorator(cache_page(cache_timeout))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(cache_timeout))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
