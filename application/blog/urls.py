from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]