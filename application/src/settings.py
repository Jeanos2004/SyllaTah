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

INSTALLED_APPS = [
    'jazzmin',
    'custom_auth.apps.CustomAuthConfig',
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
    'lodge',  # Ajout de l'application lodge
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
]

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
    'custom_auth.middleware.SecurityMiddleware',  
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
    'LOGIN_SERIALIZER': 'custom_auth.serializers.LoginSerializer',
    'USER_DETAILS_SERIALIZER': 'custom_auth.serializers.CustomUserSerializer',
    'REGISTER_SERIALIZER': 'custom_auth.registration.serializers.CustomRegisterSerializer',
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
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'  # Changez 'http' en 'https' si vous utilisez ngrok


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
            'client_id' : '650062601357-5lctpaj24740pk1mhh14qhqsq6of60h0.apps.googleusercontent.com',
            'secret': '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',
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
# Configuration supplémentaire allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_METHOD = {'email'}
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_RATE_LIMITS = ['login_failed']
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
# Configuration JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
}

# Celery Configuration
CELERY_BROKER_URL = 'memory:///'
CELERY_RESULT_BACKEND = 'cache+memory:///'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_ALWAYS_EAGER = True  # This will make Celery run tasks synchronously
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_CACHE_BACKEND = 'django-cache'
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
    "site_title": "SyllaTah Admin",
    "site_header": "SyllaTah",
    "site_brand": "SyllaTah",
    "welcome_sign": "Bienvenue dans l'administration de SyllaTah",
    "site_logo": None,
    
    # Configuration du menu
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Tableau de bord", "url": "admin_dashboard", "permissions": ["auth.view_user"]},
        {"name": "Bonjour"}
    ],

    # Configuration du menu latéral
    "order_with_respect_to": ["auth", "reservations", "activities", "accommodations", "transports"],
    
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        # Réservations
        "reservations.Reservation": "fas fa-calendar-check",
        "reservations.Payment": "fas fa-money-bill-wave",
        
        # Régions
        "regions.Region": "fas fa-map-marked-alt",
        "regions.City": "fas fa-city",
        
        # Lieux touristiques
        "tourist_places.TouristPlace": "fas fa-landmark",
        "tourist_places.PlaceCategory" : "fas fa-tags",
        "tourist_places.PlaceReview" : "fas fa-star",

        
        # Hébergements
        "accommodations.Accommodation": "fas fa-hotel",
        "accommodations.Room": "fas fa-bed",
        "accommodations.RoomType": "fas fa-door-closed",
        
        # Transports
        "transports.Transport": "fas fa-bus",
        "transports.TransportCategory": "fas fa-truck-moving",
        
        # Activités
        "activities.Activity": "fas fa-hiking",
        "activities.ActivityCategory": "fas fa-list",
        "activities.ActivityReview": "fas fa-comment-dots",
        
        # Blog
        "blog.BlogPost": "fas fa-blog",
        "blog.BlogCategory": "fas fa-folder",
        "blog.BlogTag": "fas fa-tag",

        # Lodge (Hébergeurs)
        "lodge.Lodge": "fas fa-building",
        "lodge.LodgeProfile": "fas fa-id-card",
        "lodge.LodgeStaff": "fas fa-user-tie",
        "lodge.LodgeService": "fas fa-concierge-bell",
        "lodge.LodgeAmenity": "fas fa-spa",
        "lodge.LodgeReview": "fas fa-star",
        "lodge.LodgeGallery": "fas fa-images",
        "lodge.LodgeBooking": "fas fa-calendar-alt",
        
        
        # Sites
        "sites.Site": "fas fa-globe",
        
        # Socialaccount
        "socialaccount.SocialApp": "fas fa-share-alt",
        "socialaccount.SocialAccount": "fas fa-user-circle",
        "socialaccount.SocialToken": "fas fa-key",
        
        # Account
        "account.EmailAddress": "fas fa-envelope",
        "account.EmailConfirmation": "fas fa-envelope-open-text",
        
        # Token
        "authtoken.TokenProxy": "fas fa-key",
        "authtoken.Token": "fas fa-shield-alt",
    },

    # Liens personnalisés dans le menu latéral
    #"custom_links": {
    #    "reservations": [{
    #       "name": "Statistiques",
    #        "url": "admin_dashboard",
    #        "icon": "fas fa-chart-line"
     #   }]
    
    #},
}

# Configuration additionnelle de Jazzmin
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
""" JAZZMIN_UI_TWEAKS = {
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

} """

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



AUTH_USER_MODEL = 'custom_auth.CustomUser'
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
STRIPE_PUBLIC_KEY = 'votre_clé_publique'
STRIPE_SECRET_KEY = 'votre_clé_secrète'
STRIPE_WEBHOOK_SECRET = 'votre_clé_webhook'
