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
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='blogpost-detail')

    class Meta:
        model = BlogPost
        fields = ['id', 'url', 'title', 'slug', 'author', 'category', 
                 'tags', 'image', 'created_at', 'views_count', 'featured']

class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(),
        write_only=True,
        source='category'
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=BlogTag.objects.all(),
        write_only=True,
        many=True,
        source='tags'
    )

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 
                 'category_id', 'tags', 'tag_ids', 'image', 'created_at', 
                 'updated_at', 'status', 'views_count', 'featured']
        read_only_fields = ['created_at', 'updated_at', 'views_count', 'slug']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)