from rest_framework.versioning import URLPathVersioning

class SyllaTahVersioning(URLPathVersioning):
    """
    Classe de versionnement personnalisée pour l'API SyllaTah.
    Permet de gérer différentes versions de l'API via l'URL.
    """
    default_version = 'v1'
    allowed_versions = ['v1', 'v2']
    version_param = 'version'
