from django.urls import path, include
from django.contrib import admin
from django.conf.urls import handler404, handler500, handler403, handler400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('reservations/', include('reservations.urls')),
    path('tourist_places/', include('tourist_places.urls')),
    path('transports/', include('transports.urls')),
]

# Error handlers
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
handler403 = 'django.views.defaults.permission_denied'
handler400 = 'django.views.defaults.bad_request'