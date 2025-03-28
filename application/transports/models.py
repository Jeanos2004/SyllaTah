from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()
class TransportCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='transport/categories/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Transport Categories"

class Transport(models.Model):
    AVAILABILITY_STATUS = [
        ('available', 'Disponible'),
        ('maintenance', 'En maintenance'),
        ('booked', 'Réservé'),
        ('inactive', 'Inactif')
    ]

    company_name = models.CharField(max_length=200, null=False, blank=False)
    transport_type = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(TransportCategory, on_delete=models.SET_NULL, null=True)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    luggage_capacity = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    air_conditioned = models.BooleanField(default=True)
    wifi_available = models.BooleanField(default=False)
    driver_languages = models.JSONField(default=list)
    insurance_included = models.BooleanField(default=True)
    cancellation_policy = models.TextField(null=True, blank=True)
    schedule = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='transport/vehicles/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.company_name} - {self.vehicle_type}"

    def update_rating(self, new_rating):
        if self.total_reviews == 0:
            self.rating = new_rating
        else:
            self.rating = ((self.rating * self.total_reviews) + new_rating) / (self.total_reviews + 1)
        self.total_reviews += 1
        self.save()

class TransportReview(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['transport', 'user']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.transport.update_rating(self.rating)