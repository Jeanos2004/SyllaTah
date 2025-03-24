from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransportViewSet

router = DefaultRouter()
router.register(r'', TransportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]