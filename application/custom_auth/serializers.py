from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.urls import exceptions as url_exceptions
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle CustomUser avec validation personnalisée.
    Gère les données des utilisateurs du système de lodge.
    """
    # Champ calculé pour déterminer le rôle de l'utilisateur
    role = serializers.SerializerMethodField()
    
    # Champ pour la validation du mot de passe lors de la création
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = (
            'id', 
            'username', 
            'email', 
            'lodge_id',
            'is_lodge_admin', 
            'phone_number', 
            'position',
            'role',
            'password'
        )
        read_only_fields = ('id', 'is_lodge_admin', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def get_role(self, obj):
        """
        Détermine le rôle de l'utilisateur basé sur ses attributs
        Returns:
            str: 'admin', 'staff', ou 'guest'
        """
        if obj.is_lodge_admin:
            return 'admin'
        elif obj.lodge_id:
            return 'staff'
        return 'guest'

    def validate_lodge_id(self, value):
        """
        Valide que le lodge_id correspond à un lodge existant
        """
        if value:
            from lodge.models import Lodge
            try:
                Lodge.objects.get(id=value)
            except Lodge.DoesNotExist:
                raise serializers.ValidationError("Lodge specified does not exist")
        return value

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec un mot de passe hashé
        """
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """
        Met à jour un utilisateur existant en gérant le mot de passe séparément
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

from .app_settings import api_settings

if 'allauth' in settings.INSTALLED_APPS:
    from .forms import AllAuthPasswordResetForm

from .models import TokenModel

# Get the UserModel
UserModel = get_user_model()

class LoginSerializer(BaseLoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
    lodge_id = serializers.UUIDField(required=False)

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)
        return user

    def _validate_username(self, username, password):
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)
        return user

    def get_auth_user(self, username, email, password):
        if 'allauth' in settings.INSTALLED_APPS:
            try:
                from allauth.account import app_settings as allauth_account_settings
                if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.EMAIL:
                    return self._validate_email(email, password)
                elif allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.USERNAME:
                    return self._validate_username(username, password)
            except url_exceptions.NoReverseMatch:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)

        # Fallback to default authentication
        if email:
            user = self._validate_email(email, password)
        elif username:
            user = self._validate_username(username, password)
        else:
            raise exceptions.ValidationError(_('Must include either "username" or "email".'))
        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        lodge_id = attrs.get('lodge_id')

        user = self.get_auth_user(username, email, password)

        if not user:
            raise exceptions.ValidationError(_('Invalid credentials.'))

        if not user.is_active:
            raise exceptions.ValidationError(_('User account is disabled.'))

        # Lodge validation
        if lodge_id:
            if not hasattr(user, 'lodge_id') or str(user.lodge_id) != str(lodge_id):
                raise exceptions.ValidationError(_('User is not associated with this lodge.'))
        elif getattr(user, 'lodge_id', None) and not user.is_lodge_admin:
            raise exceptions.ValidationError(_('Lodge ID is required for staff members.'))

        # Email verification if needed
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs


    def _validate_username_email(self, username, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, username, email, password):
        from allauth.account import app_settings as allauth_account_settings

        # Authentication through email
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.EMAIL:
            return self._validate_email(email, password)

        # Authentication through username
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.USERNAME:
            return self._validate_username(username, password)

        # Authentication through either username or email
        return self._validate_username_email(username, email, password)

    def get_auth_user_using_orm(self, username, email, password):
        if email:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        if username:
            return self._validate_username_email(username, '', password)

        return None
    
    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user, email=None):
        from allauth.account import app_settings as allauth_account_settings
        if (
            allauth_account_settings.EMAIL_VERIFICATION == allauth_account_settings.EmailVerificationMethod.MANDATORY and not user.emailaddress_set.filter(email=user.email, verified=True).exists()
        ):
            raise serializers.ValidationError(_('E-mail is not verified.'))


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = TokenModel
        fields = ('key',)


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    @staticmethod
    def validate_username(username):
        if 'allauth.account' not in settings.INSTALLED_APPS:
            # We don't need to call the all-auth
            # username validator unless its installed
            return username

        from allauth.account.adapter import get_adapter
        username = get_adapter().clean_username(username)
        return username

    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        JWTUserDetailsSerializer = api_settings.USER_DETAILS_SERIALIZER

        user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
        return user_data


class JWTSerializerWithExpiration(JWTSerializer):
    """
    Serializer for JWT authentication with expiration times.
    """
    access_expiration = serializers.DateTimeField()
    refresh_expiration = serializers.DateTimeField()


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    reset_form = None

    @property
    def password_reset_form_class(self):
        if 'allauth' in settings.INSTALLED_APPS:
            return AllAuthPasswordResetForm
        else:
            return PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account.forms import default_token_generator
        else:
            from django.contrib.auth.tokens import default_token_generator

        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset attempt.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    _errors = {}
    user = None
    set_password_form = None

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account.forms import default_token_generator
            from allauth.account.utils import url_str_to_user_pk as uid_decoder
        else:
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_decode as uid_decoder

        # Decode the uidb64 (allauth use base36) to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': [_('Invalid value')]})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': [_('Invalid value')]})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    set_password_form = None

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = api_settings.OLD_PASSWORD_FIELD_ENABLED
        self.logout_on_password_change = api_settings.LOGOUT_ON_PASSWORD_CHANGE
        super().__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            err_msg = _('Your old password was entered incorrectly. Please enter it again.')
            raise serializers.ValidationError(err_msg)
        return value

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )

        self.custom_validation(attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)


class LoginResponseSerializer(serializers.Serializer):
    user = CustomUserSerializer()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    lodge_info = serializers.SerializerMethodField()
    session_info = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    def get_session_info(self, obj):
        request = self.context.get('request')
        return {
            'ip_address': request.META.get('REMOTE_ADDR'),
            'device': request.META.get('HTTP_USER_AGENT', ''),
            'login_time': timezone.now().isoformat()
        }

    def get_permissions(self, obj):
        user = obj['user']
        return {
            'can_manage_lodge': user.is_lodge_admin,
            'can_manage_users': user.is_staff or user.is_lodge_admin,
            'can_view_reports': user.is_lodge_admin or (user.lodge_id is not None)
        }

    def get_lodge_info(self, obj):
        user = obj['user']
        if not user.lodge_id:
            return None
        
        from lodge.models import Lodge
        try:
            lodge = Lodge.objects.get(id=user.lodge_id)
            return {
                'id': lodge.id,
                'name': lodge.name,
                'role': 'admin' if user.is_lodge_admin else 'staff'
            }
        except Lodge.DoesNotExist:
            return None

class UserSessionSerializer(serializers.Serializer):
    device_type = serializers.CharField(required=False)
    ip_address = serializers.IPAddressField(required=False)
    last_activity = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['ip_address'] = request.META.get('REMOTE_ADDR')
        attrs['device_type'] = request.META.get('HTTP_USER_AGENT', '')
        attrs['last_activity'] = timezone.now()
        return attrs


class TokenValidationSerializer(serializers.Serializer):
    token = serializers.CharField()
    lodge_id = serializers.UUIDField(required=False)

    def validate(self, attrs):
        from rest_framework_simplejwt.tokens import AccessToken
        from django.core.exceptions import ValidationError
        
        try:
            token = AccessToken(attrs['token'])
            user_id = token.payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            
            if attrs.get('lodge_id') and user.lodge_id != attrs['lodge_id']:
                raise serializers.ValidationError(_('Token non valide pour ce lodge'))
                
            attrs['user'] = user
            attrs['token_exp'] = datetime.fromtimestamp(token.payload['exp'])
            
        except (ValidationError, CustomUser.DoesNotExist):
            raise serializers.ValidationError(_('Token invalide'))
            
        return attrs

