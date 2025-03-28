from django.contrib import admin
from .models import Reservation, Payment, UserWallet, WalletTransaction, EmailLog

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_number', 'user', 'status', 'payment_status', 'total_price', 'check_in_date']
    list_filter = ['status', 'payment_status', 'reservation_date']
    search_fields = ['reservation_number', 'user__username', 'user__email']
    date_hierarchy = 'reservation_date'
    readonly_fields = ['reservation_number', 'reservation_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'reservation', 'amount', 'payment_type', 'status', 'payment_date']
    list_filter = ['status', 'payment_type', 'payment_date']
    search_fields = ['transaction_id', 'reservation__reservation_number']
    date_hierarchy = 'payment_date'

@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'last_updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated']

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount', 'transaction_type', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['wallet__user__username', 'description']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'email_type', 'recipient', 'sent_at', 'status']
    list_filter = ['email_type', 'status', 'sent_at']
    search_fields = ['reservation__reservation_number', 'recipient', 'subject']
    date_hierarchy = 'sent_at'
    readonly_fields = ['sent_at']
