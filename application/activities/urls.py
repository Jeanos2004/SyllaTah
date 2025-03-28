from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityCategoryViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'categories', ActivityCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]