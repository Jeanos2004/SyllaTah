from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.authtoken.models import Token as DefaultTokenModel
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

from .app_settings import api_settings


class CustomUser(AbstractUser):
    lodge_id = models.UUIDField(unique=True, null=True, blank=True)
    is_lodge_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def is_lodge_staff(self):
        return bool(self.lodge_id)

    def get_lodge_role(self):
        if self.is_lodge_admin:
            return 'admin'
        elif self.lodge_id:
            return 'staff'
        return None

def get_token_model():
    token_model = api_settings.TOKEN_MODEL
    session_login = api_settings.SESSION_LOGIN
    use_jwt = api_settings.USE_JWT

    if not any((session_login, token_model, use_jwt)):
        raise ImproperlyConfigured(
            'No authentication is configured for rest auth. You must enable one or '
            'more of `TOKEN_MODEL`, `USE_JWT` or `SESSION_LOGIN`'
        )
    if (
        token_model == DefaultTokenModel and 'rest_framework.authtoken' not in settings.INSTALLED_APPS
    ):
        raise ImproperlyConfigured(
            'You must include `rest_framework.authtoken` in INSTALLED_APPS '
            'or set TOKEN_MODEL to None'
        )
    return token_model


TokenModel = get_token_model()
