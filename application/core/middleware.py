import json
import logging
import traceback
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException

# Configuration du logger
logger = logging.getLogger('api_monitoring')

class APIExceptionMiddleware:
    """
    Middleware pour capturer et formater les exceptions de l'API de manière cohérente.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Traitement de la requête normale
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Méthode appelée lorsqu'une exception est levée pendant le traitement d'une requête.
        """
        # Récupérer les détails de l'exception
        error_class = exception.__class__.__name__
        error_message = str(exception)
        stack_trace = traceback.format_exc()
        
        # Journaliser l'erreur avec les détails complets
        logger.error(
            f"Exception non gérée: {error_class} - {error_message}\n"
            f"Path: {request.path}\n"
            f"Method: {request.method}\n"
            f"User: {request.user}\n"
            f"Stack trace: {stack_trace}"
        )
        
        # Préparer la réponse d'erreur
        error_response = {
            'error': 'server_error',
            'detail': 'Une erreur inattendue est survenue.',
            'code': 'internal_error'
        }
        
        # Pour les exceptions DRF, utiliser leurs informations
        if isinstance(exception, APIException):
            error_response = {
                'error': error_class.lower(),
                'detail': error_message,
                'code': getattr(exception, 'default_code', 'api_error')
            }
            return JsonResponse(error_response, status=exception.status_code)
        
        # Pour les autres exceptions, retourner une erreur 500
        return JsonResponse(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
