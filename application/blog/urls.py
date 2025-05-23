from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CategoryViewSet, TagViewSet, create_blog_post, list_blog_posts

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/create/', create_blog_post, name='create-blog-post'),
    path('posts/list/', list_blog_posts, name='list-blog-posts'),
]