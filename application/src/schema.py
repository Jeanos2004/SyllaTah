from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.views import SpectacularAPIView
import logging
import traceback
from rest_framework.views import APIView
from rest_framework import permissions
from django.http import JsonResponse
import json
import os

logger = logging.getLogger('api_monitoring')

class SafeSchemaGenerator(SchemaGenerator):
    """
    Générateur de schéma personnalisé qui capture les erreurs et continue
    la génération du schéma même en cas de problème avec certains endpoints.
    """
    def _get_paths_and_endpoints(self):
        """
        Surcharge de la méthode pour capturer les erreurs lors de la génération
        des chemins et endpoints.
        """
        result = {}
        
        # Récupérer tous les endpoints
        endpoints = self.get_all_endpoints()
        
        # Traiter chaque endpoint individuellement pour isoler les erreurs
        for path, path_regex, method, view in endpoints:
            try:
                # Ignorer les endpoints de l'application lodge qui causent des problèmes
                if 'lodge' in path:
                    continue
                    
                # Essayer de générer le schéma pour cet endpoint
                if path not in result:
                    result[path] = {}
                
                # Générer le schéma pour cette méthode
                operation = self.get_operation(path, method, view)
                
                # Ajouter l'opération au résultat
                result[path][method.lower()] = operation
                
            except Exception as e:
                # Enregistrer l'erreur mais continuer avec les autres endpoints
                logger.error(
                    f"Erreur lors de la génération du schéma pour {method} {path}: {str(e)}\n"
                    f"Traceback: {traceback.format_exc()}"
                )
                # Ne pas ajouter cet endpoint au schéma
                continue
        
        return result

    def get_schema(self, request=None, public=False):
        """
        Surcharge de la méthode pour capturer les erreurs lors de la génération du schéma.
        """
        try:
            schema = super().get_schema(request, public)
            return schema
        except Exception as e:
            logger.error(
                f"Erreur lors de la génération du schéma: {str(e)}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            
            # Retourner un schéma minimal en cas d'erreur
            return {
                "openapi": "3.0.3",
                "info": {
                    "title": "SyllaTah API",
                    "version": "1.0.0",
                    "description": "API pour la gestion des réservations, hébergements, transports et activités"
                },
                "paths": {}
            }


class SafeSpectacularAPIView(SpectacularAPIView):
    """
    Vue API personnalisée qui utilise notre générateur de schéma sécurisé.
    """
    generator_class = SafeSchemaGenerator
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        Surcharge de la méthode GET pour utiliser directement le schéma statique.
        Vérifie également que l'utilisateur est authentifié.
        """
        # Vérifier que l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return JsonResponse(
                {"detail": "Authentification requise pour accéder à la documentation API."}, 
                status=401
            )
        
        # Utiliser directement le schéma statique au lieu d'essayer de générer un schéma dynamique
        static_schema_path = os.path.join(os.path.dirname(__file__), 'static_schema.json')
        
        if os.path.exists(static_schema_path):
            try:
                with open(static_schema_path, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                return JsonResponse(schema)
            except Exception as e:
                logger.error(f"Erreur lors du chargement du schéma statique: {str(e)}")
        
        # Si le schéma statique n'est pas disponible, essayer la génération normale
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(
                f"Erreur lors de la génération du schéma: {str(e)}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            
            # Retourner un schéma minimal en cas d'erreur
            schema = {
                "openapi": "3.0.3",
                "info": {
                    "title": "SylliTaa API",
                    "version": "1.0.0",
                    "description": "API pour la gestion des réservations, hébergements, transports et activités"
                },
                "paths": {}
            }
            
            return JsonResponse(schema)
