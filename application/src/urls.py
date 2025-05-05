from django.urls import include, re_path, path
from django.contrib import admin

from django.views.generic import RedirectView, TemplateView
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView
from rest_framework import permissions

# Utilisation de notre vue personnalisée au lieu de SpectacularAPIView
from src.schema import SafeSpectacularAPIView

schema_view = SafeSpectacularAPIView.as_view()

from src.admin_dashboard import admin_dashboard

urlpatterns = [
    # Pages HTML (frontend)
    re_path(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    re_path(r'^signup/$', TemplateView.as_view(template_name="signup.html"), name='signup'),
    re_path(r'^email-verification/$', TemplateView.as_view(template_name="email_verification.html"), name='email-verification'),
    re_path(r'^login/$', TemplateView.as_view(template_name="login.html"), name='login'),
    re_path(r'^logout/$', TemplateView.as_view(template_name="logout.html"), name='logout'),
    re_path(r'^password-reset/$', TemplateView.as_view(template_name="password_reset.html"), name='password-reset'),
    re_path(r'^password-reset/confirm/$', TemplateView.as_view(template_name="password_reset_confirm.html"), name='password-reset-confirm'),
    re_path(r'^user-details/$', TemplateView.as_view(template_name="user_details.html"), name='user-details'),
    re_path(r'^password-change/$', TemplateView.as_view(template_name="password_change.html"), name='password-change'),
    re_path(r'^resend-email-verification/$', TemplateView.as_view(template_name="resend_email_verification.html"), name='resend-email-verification'),

    # URL pour la réinitialisation du mot de passe (email)
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),

    # Authentification (dj-rest-auth et allauth)
    re_path(r'^auth/', include('dj_rest_auth.urls')),
    re_path(r'^auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^accounts/', include('allauth.urls')),

    # Admin
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'), 
    re_path(r'^admin/', admin.site.urls),
    

    # Redirection du profil utilisateur
    re_path(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),

    # Documentation de l'API (drf-spectacular) - Sécurisée
    re_path(r'^api/schema/$', schema_view, name='schema'),
    re_path(r'^api/docs/$', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[permissions.IsAuthenticated]), name='api_docs'),
    re_path(r'^api/redoc/$', SpectacularRedocView.as_view(url_name='schema', permission_classes=[permissions.IsAuthenticated]), name='schema-redoc'),

    # URLs des applications
    re_path(r'^api/regions/', include('regions.urls')),
    re_path(r'^api/tourist-places/', include('tourist_places.urls')),
    re_path(r'^api/accommodations/', include('accommodations.urls')),
    re_path(r'^api/transports/', include('transports.urls')),
    re_path(r'^api/activities/', include('activities.urls')),
    re_path(r'^api/blog/', include('blog.urls')),
    re_path(r'^api/reservations/', include('reservations.urls')),
    re_path(r'^api/lodge/', include('lodge.urls')),
]