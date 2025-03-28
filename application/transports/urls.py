from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransportViewSet, TransportCategoryViewSet

router = DefaultRouter()
router.register(r'transports', TransportViewSet)
router.register(r'categories', TransportCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]