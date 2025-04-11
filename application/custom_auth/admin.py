from django.contrib import admin

from custom_auth.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display =['username', 'email', 'position', 'lodge_id', 'phone_number']
