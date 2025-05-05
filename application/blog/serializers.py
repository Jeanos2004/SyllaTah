from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, BlogCategory, BlogTag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug']

class BlogPostListSerializer(serializers.ModelSerializer):
    # Utiliser StringRelatedField pour éviter les problèmes avec les relations complexes
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author_username', 'category_name',
                 'image', 'created_at', 'views_count', 'featured']

class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'status', 'featured', 'image']

    def create(self, validated_data):
        # Créer l'article sans les tags
        instance = BlogPost(
            title=validated_data.get('title', ''),
            content=validated_data.get('content', ''),
            author=validated_data.get('author'),
            category=validated_data.get('category'),
            status=validated_data.get('status', 'draft'),
            featured=validated_data.get('featured', False),
            image=validated_data.get('image')
        )
        
        # Sauvegarder l'instance pour générer un ID
        instance.save()
        return instance

class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 
                 'tags', 'image', 'created_at', 'updated_at', 'status', 
                 'views_count', 'featured']
        read_only_fields = ['created_at', 'updated_at', 'views_count', 'slug']