from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger('error_handling')

def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exceptions personnalisé pour l'API
    """
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, ValidationError):
            response = Response({
                'error': 'validation_error',
                'detail': str(exc),
                'code': 'invalid_data'
            }, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, Http404):
            response = Response({
                'error': 'not_found',
                'detail': _('The requested resource was not found.'),
                'code': 'resource_not_found'
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            # Log l'erreur non gérée
            logger.error(f'Unhandled exception: {str(exc)}', exc_info=True)
            response = Response({
                'error': 'server_error',
                'detail': _('An unexpected error occurred.'),
                'code': 'internal_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Ajoute des informations de débogage en développement
    if hasattr(exc, 'get_full_details'):
        response.data['debug_info'] = exc.get_full_details()

    # Log toutes les erreurs 4XX et 5XX
    if response.status_code >= 400:
        logger.warning(
            f'API Error {response.status_code}: {response.data}',
            extra={
                'status_code': response.status_code,
                'view': context.get('view').__class__.__name__,
                'error_detail': response.data
            }
        )

    return response

class ErrorDetail:
    """
    Classe utilitaire pour formater les erreurs de manière cohérente
    """
    @staticmethod
    def validation_error(message, code='invalid_input'):
        return {
            'error': 'validation_error',
            'detail': message,
            'code': code
        }

    @staticmethod
    def permission_error(message, code='permission_denied'):
        return {
            'error': 'permission_error',
            'detail': message,
            'code': code
        }

    @staticmethod
    def not_found_error(message, code='not_found'):
        return {
            'error': 'not_found',
            'detail': message,
            'code': code
        }
