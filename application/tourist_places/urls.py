from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TouristPlaceViewSet

router = DefaultRouter()
router.register(r'', TouristPlaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]