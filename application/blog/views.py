from django.shortcuts import render
from rest_framework import viewsets

from .permissions import IsAuthorOrReadOnly
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer