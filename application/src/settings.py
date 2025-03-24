"""
Django settings for SyllaTah project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ma3c@7uu!%e0=tynp+i6+q%$)9v@$t(eulqurym_b=48z82&5n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'dfef-197-149-243-78.ngrok-free.app',
    '127.0.0.1',
    'localhost'
]

# Application definition

INSTALLED_APPS = (
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'requests_oauthlib',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'drf_spectacular',  
    'corsheaders',
    'regions',
    'tourist_places',
    'accommodations',
    'transports',
    'activities',
    'blog',
    'reservations',
    'django_filters',
)

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'src.middleware.APIMonitoringMiddleware',  # Middleware de monitoring
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
)

# For backwards compatibility for Django 1.8
MIDDLEWARE_CLASSES = MIDDLEWARE

ROOT_URLCONF = 'src.urls'

WSGI_APPLICATION = 'src.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_AUTH = {
    'SESSION_LOGIN': True,
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'auth',
    'JWT_AUTH_HTTPONLY': False,
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Ou votre serveur SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jeankelouaouamouno71@gmail.com'  # Votre adresse email
EMAIL_HOST_PASSWORD = 'exqg ncju laue nhjq'  # Votre mot de passe d'application

# Django-allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGIN_METHODS = {'username'}
ACCOUNT_USERNAME_REQUIRED = True
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'


SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Permettre l'accès à tous pendant la phase de test
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Utiliser drf-spectacular pour la documentation
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Nombre d'éléments par page
    
    # Configuration de throttling (limitation de débit)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/hour',  # Limite pour les utilisateurs anonymes
        'user': '1000/hour',  # Limite pour les utilisateurs authentifiés
    },
    
    # Configuration du versionnement de l'API
    'DEFAULT_VERSIONING_CLASS': 'src.versioning.SyllaTahVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_VERSION': 'v1',
    'VERSION_PARAM': 'version',
}

# Configuration CORS pour autoriser les requêtes depuis n'importe quelle origine pendant la phase de test
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend NextJS en développement local
    "https://votre-domaine-de-production.com",  # Remplacer par votre domaine de production
]

CORS_ALLOW_CREDENTIALS = True  # Permet d'envoyer des cookies avec les requêtes cross-origin

CORS_ALLOW_ALL_ORIGINS = True

# Configuration des fournisseurs d'authentification sociale
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id' : 'votre_client_id',
            'secret': 'votre secret key',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Configuration JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
}

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    'check-upcoming-reservations': {
        'task': 'reservations.tasks.check_upcoming_reservations',
        'schedule': timedelta(hours=1),
    },
    'retry-failed-notifications': {
        'task': 'reservations.tasks.retry_failed_notifications',
        'schedule': timedelta(minutes=30),
    },
}
# Configuration de drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'SyllaTah API',
    'DESCRIPTION': 'API pour la plateforme touristique SyllaTah',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}

JAZZMIN_SETTINGS = {
    # Nom et branding de l’admin
    "site_title": "SyllaTaa Administration",
    "site_header": "SyllaTaa",
    "site_brand": "SyllaTaa Administration",
    #"site_logo": "images/logo.png",
    "site_icon": "images/favicon.ico",
    "welcome_sign": "Bienvenue dans l'administration SyllaTaa",
    "copyright": "SyllaTaa",
    
    # Personnalisation du menu
    "custom_links": {
        "auth": [
            {
                "name": "Documentation",
                "url": "https://docs.djangoproject.com/",
                "icon": "fas fa-book",
            },
        ]
    },
    
    # Ordre et structure du menu latéral
    "order_with_respect_to": ["auth", "sites"],
    
    # Autres options, par exemple : changer l’icône de l’application
    "icons": {
        "auth": "fas fa-users-cog",
        "sites": "fas fa-globe",
    },
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Documentation", "url": "https://docs.djangoproject.com", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "Profil", "url": "admin:auth_user_change", "icon": "fas fa-user"},
        {"model": "auth.user"},
    ],
    "show_ui_builder": True,  # Affiche un outil pour réorganiser l’interface
}
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # Thème Bootstrap parmi plusieurs disponibles (ex: 'cerulean', 'cosmo', 'flatly', etc.)
    "dark_mode_theme": "darkly",
    "footer_small_text": True,
    "body_large_text": True,
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "navbar_small": True,
    "body_large_text": True,
    "actions_sticky_top": False

}

SWAGGER_SETTINGS = {
    'LOGIN_URL': 'login',
    'LOGOUT_URL': 'logout',
}



# For SyllaTaa purposes only. Use a white list in the real world.
CORS_ORIGIN_ALLOW_ALL = False

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Ou votre serveur SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jeankelouaouamouno71@gmail.com'  # Votre adresse email
EMAIL_HOST_PASSWORD = 'exqg ncju laue nhjq'  # Votre mot de passe d'application

# Configuration de la journalisation
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/api_monitoring.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'api_monitoring': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Créer le répertoire de logs s'il n'existe pas
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))
