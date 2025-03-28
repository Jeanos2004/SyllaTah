from django.contrib import admin
from .models import BlogPost, BlogCategory, BlogTag

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'views_count', 'featured']
    list_filter = ['status', 'category', 'created_at', 'featured']
    search_fields = ['title', 'content', 'author__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('Publication', {
            'fields': ('author', 'category', 'tags', 'status', 'featured')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
