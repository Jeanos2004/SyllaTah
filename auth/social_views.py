from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .social_serializers import TwitterLoginSerializer

class FacebookLogin(SocialLoginView):
    """
    Vue pour l'authentification via Facebook.
    Utilise l'adaptateur OAuth2 de Facebook fourni par django-allauth.
    """
    adapter_class = FacebookOAuth2Adapter
    callback_url = 'http://localhost:3000/auth/facebook/callback'
    client_class = OAuth2Client

class GoogleLogin(SocialLoginView):
    """
    Vue pour l'authentification via Google.
    Utilise l'adaptateur OAuth2 de Google fourni par django-allauth.
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/auth/google/callback'
    client_class = OAuth2Client

class TwitterLogin(SocialLoginView):
    """
    Vue pour l'authentification via Twitter (X).
    Utilise l'adaptateur OAuth de Twitter fourni par django-allauth.
    """
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter
