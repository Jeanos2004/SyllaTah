import time
import logging
import json
from django.utils.deprecation import MiddlewareMixin

# Configuration du logger
logger = logging.getLogger('api_monitoring')

class APIMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware pour surveiller les performances de l'API.
    Enregistre le temps de réponse, le statut HTTP et d'autres informations utiles.
    """
    
    def process_request(self, request):
        # Marquer le temps de début de la requête
        request.start_time = time.time()
    
    def process_response(self, request, response):
        # Ignorer les requêtes statiques et admin
        if '/static/' in request.path or '/admin/' in request.path:
            return response
            
        # Calculer le temps de réponse
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Préparer les données à journaliser
            log_data = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration': round(duration * 1000, 2),  # en millisecondes
                'user': str(request.user) if request.user.is_authenticated else 'anonymous',
                'ip': self.get_client_ip(request),
            }
            
            # Journaliser les données
            logger.info(json.dumps(log_data))
            
            # Ajouter un en-tête avec le temps de réponse
            response['X-Response-Time-ms'] = str(round(duration * 1000, 2))
            
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
