from django.contrib import admin

from custom_auth.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        list_display =['username', 'email', 'position']
