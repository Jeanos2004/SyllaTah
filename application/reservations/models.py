from django.db import models
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

User = get_user_model()
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
        ('refunded', 'Remboursée')
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Non payé'),
        ('partially_paid', 'Partiellement payé'),
        ('paid', 'Payé'),
        ('refunded', 'Remboursé')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    
    # Services réservés
    accommodation = models.ForeignKey('accommodations.Accommodation', on_delete=models.SET_NULL, null=True, blank=True)
    transport = models.ForeignKey('transports.Transport', on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey('activities.Activity', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Dates
    reservation_date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateTimeField(null=True, blank=True)
    check_out_date = models.DateTimeField(null=True, blank=True)
    
    # Prix et paiements
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Informations supplémentaires
    number_of_guests = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-reservation_date']

    def __str__(self):
        return f"Reservation #{self.reservation_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.reservation_number:
            self.reservation_number = self.generate_reservation_number()
        
        if not self.total_price:
            self.calculate_total_price()
            
        self.update_payment_status()
        super().save(*args, **kwargs)

    def clean(self):
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("La date de départ doit être postérieure à la date d'arrivée")
        
        if self.check_in_date < timezone.now():
            raise ValidationError("La date d'arrivée ne peut pas être dans le passé")
        
        self.validate_service_availability()

    def generate_reservation_number(self):
        import uuid
        return f"RES-{uuid.uuid4().hex[:8].upper()}"

    def calculate_total_price(self):
        self.base_price = Decimal('0')
        
        if self.accommodation:
            nights = (self.check_out_date - self.check_in_date).days
            self.base_price += self.accommodation.price_per_night * nights
            
        if self.transport:
            self.base_price += self.transport.price
            
        if self.activity:
            self.base_price += self.activity.price * self.number_of_guests
            
        # Calcul des taxes (exemple: 20%)
        self.taxes = self.base_price * Decimal('0.20')
        
        self.total_price = self.base_price + self.taxes - self.discounts

    def update_payment_status(self):
        if self.amount_paid >= self.total_price:
            self.payment_status = 'paid'
        elif self.amount_paid > 0:
            self.payment_status = 'partially_paid'
        else:
            self.payment_status = 'unpaid'

    def validate_service_availability(self):
        if self.accommodation:
            # Vérifier la disponibilité de l'hébergement
            conflicting_reservations = Reservation.objects.filter(
                accommodation=self.accommodation,
                status='confirmed',
                check_in_date__lt=self.check_out_date,
                check_out_date__gt=self.check_in_date
            ).exclude(pk=self.pk)
            
            if conflicting_reservations.exists():
                raise ValidationError("Cet hébergement n'est pas disponible pour les dates sélectionnées")

        # Ajouter des validations similaires pour transport et activités

    def cancel_reservation(self, reason):
        if self.status not in ['pending', 'confirmed']:
            raise ValidationError("Cette réservation ne peut pas être annulée")
            
        self.status = 'cancelled'
        self.cancellation_reason = reason
        self.cancellation_date = timezone.now()
        self.save()


class Payment(models.Model):
    PAYMENT_TYPES = [
        ('card', 'Carte bancaire'),
        ('transfer', 'Virement bancaire'),
        ('cash', 'Espèces'),
        ('wallet', 'Portefeuille électronique')
    ]

    PAYMENT_STATUS = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé')
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.reservation}"

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet of {self.user.username}"

    def add_funds(self, amount):
        self.balance += Decimal(str(amount))
        self.save()
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='deposit'
        )

    def withdraw_funds(self, amount):
        if self.balance < Decimal(str(amount)):
            raise ValidationError("Solde insuffisant")
        self.balance -= Decimal(str(amount))
        self.save()
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='withdrawal'
        )

class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Dépôt'),
        ('withdrawal', 'Retrait'),
        ('payment', 'Paiement'),
        ('refund', 'Remboursement')
    ]

    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.amount} for {self.wallet.user.username}"


class EmailLog(models.Model):
    EMAIL_TYPES = [
        ('confirmation', 'Confirmation de réservation'),
        ('reminder', 'Rappel'),
        ('cancellation', 'Annulation'),
        ('payment', 'Confirmation de paiement'),
        ('modification', 'Modification de réservation')
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='email_logs')
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=20, default='sent')
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.get_email_type_display()} email for {self.reservation}"
