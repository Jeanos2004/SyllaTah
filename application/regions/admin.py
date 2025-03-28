from django.contrib import admin

from .models import Region

# Register your models here.


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']