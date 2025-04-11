from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'auth', views.LodgeAuthViewSet, basename='lodge-auth')  # Add auth endpoint
router.register(r'lodge', views.LodgeViewSet, basename='lodge')
router.register(r'accommodations', views.LodgeAccommodationViewSet, basename='lodge-accommodation')
router.register(r'activities', views.LodgeActivityViewSet, basename='lodge-activity')

urlpatterns = [
    path('', include(router.urls)),
]