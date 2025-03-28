from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'auth', views.LodgeAuthViewSet, basename='lodge-auth')
router.register(r'dashboard', views.LodgeDashboardViewSet, basename='lodge-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]