from django.contrib import admin
from .models import TouristPlace, PlaceCategory


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'place_type', 'address', 'rating']
    list_filter = ['place_type', 'rating']
    search_fields = ['name', 'description', 'address']

@admin.register(PlaceCategory)
class PlaceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
