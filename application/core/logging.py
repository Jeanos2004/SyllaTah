import logging
import time
import uuid
from functools import wraps

# Configuration du logger
logger = logging.getLogger('api_monitoring')

def log_api_call(view_func):
    """
    Décorateur pour logger les appels d'API avec leur durée d'exécution.
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        request_id = str(uuid.uuid4())
        user = request.user.username if request.user.is_authenticated else 'anonymous'
        
        # Informations de début de requête
        start_time = time.time()
        logger.info(f"API Request {request_id} started - Method: {request.method}, Path: {request.path}, User: {user}")
        
        try:
            # Exécution de la vue
            response = view_func(self, request, *args, **kwargs)
            
            # Calcul de la durée
            duration = round((time.time() - start_time) * 1000, 2)  # en millisecondes
            
            # Log de succès
            logger.info(
                f"API Request {request_id} completed - "
                f"Method: {request.method}, Path: {request.path}, Status: {response.status_code}, "
                f"Duration: {duration}ms, User: {user}"
            )
            
            return response
            
        except Exception as e:
            # Calcul de la durée en cas d'erreur
            duration = round((time.time() - start_time) * 1000, 2)
            
            # Log d'erreur
            logger.error(
                f"API Request {request_id} failed - "
                f"Method: {request.method}, Path: {request.path}, Error: {str(e)}, "
                f"Duration: {duration}ms, User: {user}"
            )
            
            # Relancer l'exception pour que Django la gère
            raise
    
    return wrapper


class APILoggingMixin:
    """
    Mixin pour ajouter automatiquement le logging à toutes les méthodes d'API.
    """
    def dispatch(self, request, *args, **kwargs):
        request_id = str(uuid.uuid4())
        user = request.user.username if request.user.is_authenticated else 'anonymous'
        
        # Informations de début de requête
        start_time = time.time()
        logger.info(f"API Request {request_id} started - Method: {request.method}, Path: {request.path}, User: {user}")
        
        try:
            # Exécution de la vue avec super()
            response = super().dispatch(request, *args, **kwargs)
            
            # Calcul de la durée
            duration = round((time.time() - start_time) * 1000, 2)
            
            # Log de succès
            logger.info(
                f"API Request {request_id} completed - "
                f"Method: {request.method}, Path: {request.path}, Status: {response.status_code}, "
                f"Duration: {duration}ms, User: {user}"
            )
            
            return response
            
        except Exception as e:
            # Calcul de la durée en cas d'erreur
            duration = round((time.time() - start_time) * 1000, 2)
            
            # Log d'erreur
            logger.error(
                f"API Request {request_id} failed - "
                f"Method: {request.method}, Path: {request.path}, Error: {str(e)}, "
                f"Duration: {duration}ms, User: {user}"
            )
            
            # Relancer l'exception pour que Django la gère
            raise
