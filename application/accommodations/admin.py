from django.contrib import admin
from django.contrib.admin import ModelAdmin, filters
from .models import Accommodation, CategoryAccommodation, RoomType

""" admin.site.register(Accommodation)
admin.site.register(CategoryAccommodation) """




@admin.register(CategoryAccommodation)
class CategoryAccommodationAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(RoomType)
class RoomType(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'location', 'amenities', 'category', 'price_per_night']
    filter_horizontal = ['room_types']

# Register your models here.
