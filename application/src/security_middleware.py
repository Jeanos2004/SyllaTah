from django.http import HttpResponseForbidden
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import re

class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware pour améliorer la sécurité de l'application.
    Ajoute des en-têtes de sécurité et effectue des vérifications basiques.
    """
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.sql_pattern = re.compile(r'(\b(select|insert|update|delete|drop|union|alter)\b)', re.IGNORECASE)
        self.xss_pattern = re.compile(r'(<script|javascript:|data:text/html|vbscript:)', re.IGNORECASE)
    
    def process_request(self, request):
        # Vérification basique contre les injections SQL
        for key, value in request.GET.items():
            if self.sql_pattern.search(str(value)):
                return HttpResponseForbidden("Requête potentiellement malveillante détectée")
                
        # Vérification basique contre les XSS
        for key, value in request.GET.items():
            if self.xss_pattern.search(str(value)):
                return HttpResponseForbidden("Contenu potentiellement malveillant détecté")
        
        return None
    
    def process_response(self, request, response):
        # Ajout d'en-têtes de sécurité
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline';"
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
