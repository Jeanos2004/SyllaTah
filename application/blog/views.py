from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import F
from .models import BlogPost, BlogCategory, BlogTag
from .serializers import (
    BlogPostListSerializer, 
    BlogPostDetailSerializer,
    CategorySerializer,
    TagSerializer
)

class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'category__name', 'tags__name']
    ordering_fields = ['created_at', 'views_count', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = BlogPost.objects.select_related('author', 'category').prefetch_related('tags')
        if self.action == 'list':
            return queryset.filter(status='published')
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        post = self.get_object()
        post.featured = not post.featured
        post.save()
        return Response({'status': 'featured status updated'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count = F('views_count') + 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=True)
    def posts(self, request, slug=None):
        category = self.get_object()
        posts = BlogPost.objects.filter(
            category=category,
            status='published'
        ).order_by('-created_at')
        serializer = BlogPostListSerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    @action(detail=True)
    def posts(self, request, slug=None):
        tag = self.get_object()
        posts = BlogPost.objects.filter(
            tags=tag,
            status='published'
        ).order_by('-created_at')
        serializer = BlogPostListSerializer(
            posts, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)