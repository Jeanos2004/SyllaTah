from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import F
from django.utils.text import slugify

from src.pagination import CustomPagination
from .models import BlogPost, BlogCategory, BlogTag
from .serializers import (
    BlogPostListSerializer, 
    BlogPostDetailSerializer,
    BlogPostCreateSerializer,
    CategorySerializer,
    TagSerializer
)

@api_view(['POST'])
def create_blog_post(request):
    """Vue simple pour créer un article de blog sans utiliser de sérialiseur complexe."""
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Récupérer les données de base
        title = request.data.get('title')
        content = request.data.get('content')
        status_value = request.data.get('status', 'draft')
        featured = request.data.get('featured', False)
        
        # Vérifier les données obligatoires
        if not title or not content:
            return Response({"error": "Title and content are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer l'article
        post = BlogPost(
            title=title,
            content=content,
            author=request.user,
            status=status_value,
            featured=featured
        )
        
        # Gérer la catégorie si fournie
        category_id = request.data.get('category')
        if category_id:
            try:
                category = BlogCategory.objects.get(id=category_id)
                post.category = category
            except BlogCategory.DoesNotExist:
                pass
        
        # Sauvegarder l'article
        post.save()
        
        # Gérer les tags si fournis
        tag_ids = request.data.get('tags', [])
        if tag_ids:
            tags = BlogTag.objects.filter(id__in=tag_ids)
            post.tags.set(tags)
        
        # Retourner les données de l'article créé
        return Response({
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "status": post.status,
            "message": "Blog post created successfully"
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        # Journaliser l'erreur pour le débogage
        print(f"Erreur lors de la création du blog: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_blog_posts(request):
    """Vue simple pour lister les articles de blog sans utiliser de sérialiseur complexe."""
    try:
        # Récupérer les articles publiés
        posts = BlogPost.objects.filter(status='published').order_by('-created_at')
        
        # Préparer les données de réponse
        results = []
        for post in posts:
            author_name = post.author.username if post.author else 'Unknown'
            category_name = post.category.name if post.category else None
            
            post_data = {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "author": author_name,
                "category": category_name,
                "created_at": post.created_at,
                "views_count": post.views_count,
                "featured": post.featured
            }
            results.append(post_data)
        
        # Retourner les données
        return Response({
            "count": len(results),
            "results": results
        })
    
    except Exception as e:
        # Journaliser l'erreur pour le débogage
        print(f"Erreur lors de la récupération des blogs: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'category__name', 'tags__name']
    ordering_fields = ['created_at', 'views_count', 'title']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        # Assurer que l'auteur est défini
        serializer.save(author=self.request.user)

    def get_queryset(self):
        try:
            queryset = BlogPost.objects.all()
            
            # Ajouter les relations avec gestion des erreurs
            try:
                queryset = queryset.select_related('author', 'category')
            except Exception as e:
                print(f"Erreur lors du select_related: {str(e)}")
            
            try:
                queryset = queryset.prefetch_related('tags')
            except Exception as e:
                print(f"Erreur lors du prefetch_related: {str(e)}")
            
            if self.action == 'list':
                return queryset.filter(status='published')
            return queryset
        except Exception as e:
            print(f"Erreur dans get_queryset: {str(e)}")
            # Retourner un queryset vide en cas d'erreur
            return BlogPost.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        elif self.action == 'create':
            return BlogPostCreateSerializer
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