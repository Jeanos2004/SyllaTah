from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache
from django.conf import settings

class CustomRateThrottle(SimpleRateThrottle):
    """
    Throttle personnalisé avec des limites différentes selon le type d'utilisateur
    """
    cache_format = 'throttle_%(scope)s_%(ident)s'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def get_rate(self):
        if self.scope == 'login':
            return '5/min'  # Limite les tentatives de connexion
        elif self.scope == 'register':
            return '3/hour'  # Limite les créations de compte
        elif hasattr(self.request, 'user') and self.request.user.is_authenticated:
            if self.request.user.is_lodge_admin:
                return '1000/hour'  # Plus de requêtes pour les admins
            return '100/hour'  # Limite standard pour utilisateurs authentifiés
        return '50/hour'  # Limite pour utilisateurs anonymes

class LoginRateThrottle(CustomRateThrottle):
    scope = 'login'

class RegisterRateThrottle(CustomRateThrottle):
    scope = 'register'

class UserRateThrottle(CustomRateThrottle):
    scope = 'user'

def get_client_ip_address(request):
    """Obtient l'adresse IP réelle du client même derrière un proxy"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def block_suspicious_ip(ip_address, reason='suspicious_activity'):
    """Bloque temporairement une IP suspecte"""
    cache_key = f'blocked_ip_{ip_address}'
    cache.set(cache_key, reason, timeout=3600)  # Bloque pour 1 heure

def is_ip_blocked(ip_address):
    """Vérifie si une IP est bloquée"""
    cache_key = f'blocked_ip_{ip_address}'
    return cache.get(cache_key) is not None
