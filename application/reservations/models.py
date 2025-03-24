from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from accommodations.models import Accommodation
from transports.models import Transport
from activities.models import Activity

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, null=True, blank=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cancellation_reason = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def clean(self):
        if not any([self.accommodation, self.transport, self.activity]):
            raise ValidationError("Au moins un service doit être sélectionné")
        
        if self.check_in_date and self.check_out_date:
            if self.check_in_date > self.check_out_date:
                raise ValidationError("La date d'arrivée doit être antérieure à la date de départ")
            
            if self.check_in_date < timezone.now().date():
                raise ValidationError("La date d'arrivée ne peut pas être dans le passé")

    @property
    def duration(self):
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0

    @property
    def total_price(self):
        if self.accommodation:
            return self.accommodation.price_per_night * self.duration
        elif self.transport:
            return self.transport.price
        elif self.activity:
            return self.activity.price
        return 0

    def cancel(self, reason):
        if self.status not in ['completed', 'cancelled']:
            self.status = 'cancelled'
            self.cancellation_reason = reason
            self.save()
            return True
        return False

    def __str__(self):
        return f"Reservation du Client {self.user.username} pour le {self.check_in_date}"

    @property
    def service_type(self):
        if self.accommodation:
            return "Hébergement"
        elif self.transport:
            return "Transport"
        elif self.activity:
            return "Activité"
        return "Non spécifié"

    @classmethod
    def check_availability(cls, service_type, service_id, check_in, check_out):
        overlapping = cls.objects.filter(
            models.Q(
                check_in_date__lte=check_out,
                check_out_date__gte=check_in
            ),
            status__in=['pending', 'confirmed']
        )
        
        if service_type == 'accommodation':
            overlapping = overlapping.filter(accommodation_id=service_id)
        elif service_type == 'transport':
            overlapping = overlapping.filter(transport_id=service_id)
        elif service_type == 'activity':
            overlapping = overlapping.filter(activity_id=service_id)
            
        return not overlapping.exists()

    def save(self, *args, **kwargs):
        is_new = not self.pk
        
        # Check availability for new reservations
        if is_new:
            if self.accommodation and not self.check_availability(
                'accommodation', 
                self.accommodation.id, 
                self.check_in_date, 
                self.check_out_date
            ):
                raise ValidationError("Cette période n'est pas disponible pour cet hébergement")
            
            if self.transport and not self.check_availability(
                'transport',
                self.transport.id,
                self.check_in_date,
                self.check_out_date
            ):
                raise ValidationError("Ce transport n'est pas disponible à cette date")
                
            if self.activity and not self.check_availability(
                'activity',
                self.activity.id,
                self.check_in_date,
                self.check_out_date
            ):
                raise ValidationError("Cette activité n'est pas disponible à cette date")
        
        super().save(*args, **kwargs)
        
        # Send notifications
        if is_new:
            from .tasks import send_reservation_email
            send_reservation_email.delay(self.id, 'confirmation')
        
        if self.status == 'cancelled':
            send_reservation_email.delay(self.id, 'cancellation')

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé')
    ]

    PAYMENT_TYPES = [
        ('full', 'Paiement complet'),
        ('deposit', 'Acompte'),
        ('balance', 'Solde restant')
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Paiement {self.payment_type} pour réservation #{self.reservation.id}"

    def process_refund(self):
        if self.status == 'completed':
            self.status = 'refunded'
            self.save()
            
            # Create refund transaction in wallet
            self.reservation.user.wallet.add_transaction(
                amount=self.amount,
                transaction_type='refund',
                reservation=self.reservation,
                description=f"Remboursement pour réservation #{self.reservation.id}"
            )
            return True
        return False

class UserWallet(models.Model):
    TRANSACTION_TYPES = [
        ('payment', 'Paiement'),
        ('refund', 'Remboursement'),
        ('credit', 'Crédit'),
        ('debit', 'Débit')
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    last_updated = models.DateTimeField(auto_now=True)

    def add_transaction(self, amount, transaction_type, reservation=None):
        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type=transaction_type,
            reservation=reservation
        )
        if transaction_type in ['refund', 'credit']:
            self.balance += amount
        else:
            self.balance -= amount
        self.save()

    def __str__(self):
        return f"Portefeuille de {self.user.username}"

class WalletTransaction(models.Model):
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=UserWallet.TRANSACTION_TYPES)
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} de {self.amount}€ pour {self.wallet.user.username}"

class EmailLog(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    email_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    recipient = models.EmailField()
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
