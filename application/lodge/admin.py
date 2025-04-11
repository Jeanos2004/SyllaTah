from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import Lodge, LodgeAccommodation, LodgeActivity

@admin.register(Lodge)
class LodgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active', 'created_at', 'total_accommodations', 'total_revenue', 'status_colored')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'total_revenue', 'total_accommodations')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
        ('Statistics', {
            'fields': ('total_revenue', 'total_accommodations'),
            'classes': ('collapse',)
        })
    )

    def status_colored(self, obj):
        color = 'green' if obj.is_active else 'red'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html('<span style="color: {};">{}</span>', color, status)
    status_colored.short_description = 'Status'

    def total_accommodations(self, obj):
        return obj.accommodations.count()
    total_accommodations.short_description = 'Total Accommodations'

    def total_revenue(self, obj):
        total = obj.bookings.aggregate(Sum('total_price'))['total_price__sum']
        return f"${total or 0:.2f}"
    total_revenue.short_description = 'Total Revenue'

@admin.register(LodgeAccommodation)
class LodgeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('lodge', 'accommodation', 'is_available', 'price', 'quantity', 'total_value')
    list_filter = ('is_available', 'price')
    search_fields = ('lodge__name', 'accommodation__name')
    list_editable = ('is_available', 'price', 'quantity')
    raw_id_fields = ('lodge', 'accommodation')

    def total_value(self, obj):
        return f"${obj.price * obj.quantity:.2f}"
    total_value.short_description = 'Total Value'

@admin.register(LodgeActivity)
class LodgeActivityAdmin(admin.ModelAdmin):
    list_display = ('lodge', 'activity', 'is_available', 'price', 'schedule_display')
    list_filter = ('is_available', 'price')
    search_fields = ('lodge__name', 'activity__name')
    list_editable = ('is_available', 'price')
    raw_id_fields = ('lodge', 'activity')

    def schedule_display(self, obj):
        if not obj.schedule:
            return "No schedule"
        days = obj.schedule.get('days', [])
        hours = obj.schedule.get('hours', '')
        return f"Days: {', '.join(days)} | Hours: {hours}"
    schedule_display.short_description = 'Schedule'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('lodge', 'activity')