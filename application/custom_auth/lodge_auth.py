from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()

class LodgeLoginSerializer(serializers.Serializer):
    """
    Serializer pour l'authentification avec support des lodges
    """
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
    lodge_id = serializers.UUIDField(required=False, allow_null=True)

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        lodge_id = attrs.get('lodge_id')

        if not username and not email:
            msg = _('Must include either "username" or "email".')
            raise ValidationError(msg)

        # Authentification de base
        if email:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        if username:
            user = self.authenticate(username=username, password=password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        # Vérification de l'activation du compte
        if not user.is_active:
            msg = _('User account is disabled.')
            raise ValidationError(msg)

        # Vérification du lodge_id si fourni
        if lodge_id:
            if not user.lodge_id:
                msg = _('User is not associated with any lodge.')
                raise ValidationError(msg)
            if str(user.lodge_id) != str(lodge_id):
                msg = _('User is not associated with this lodge.')
                raise ValidationError(msg)
            if not user.is_lodge_admin:
                msg = _('User is not an admin of this lodge.')
                raise ValidationError(msg)

        attrs['user'] = user
        return attrs
