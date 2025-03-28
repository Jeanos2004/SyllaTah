from django.contrib import admin
from .models import Activity, ActivityCategory, ActivityReview

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration', 'max_participants', 'rating', 'total_reviews']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'

@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(ActivityReview)
class ActivityReviewAdmin(admin.ModelAdmin):
    list_display = ['activity', 'user', 'rating', 'comment', 'photos']
    search_fields = ['activity', 'user', 'rating']
