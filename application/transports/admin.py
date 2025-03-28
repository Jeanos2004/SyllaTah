from django.contrib import admin
from .models import Transport, TransportCategory

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ['vehicle_type', 'transport_type', 'category', 'price', 'capacity', 'luggage_capacity', 'company_name']
    list_filter = ['category', 'capacity', 'created_at', 'company_name']
    search_fields = ['vehicle_type', 'transport_type', 'description']
    ordering = ['transport_type']

@admin.register(TransportCategory)
class CategoryTransportAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
