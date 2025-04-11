from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import uuid
from django.db import models
from accommodations.models import Accommodation
from activities.models import Activity

class Lodge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        null=True,
        blank=True
    )
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=[
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('guesthouse', 'Guest House'),
    ], default='hotel')
    
    # Relations avec related_name explicite pour éviter les problèmes avec drf-spectacular
    accommodations = models.ManyToManyField(
        Accommodation, 
        through='LodgeAccommodation',
        related_name='lodges'
    )
    activities = models.ManyToManyField(
        Activity, 
        through='LodgeActivity',
        related_name='lodges'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_active=True) | models.Q(is_active=False),
                name='valid_lodge_status'
            )
        ]

    def clean(self):
        if not self.email or not self.phone:
            raise ValidationError("Email and phone are required")

    def __str__(self):
        return self.name

class LodgeAccommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, related_name='lodge_accommodations')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='lodge_accommodations')
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

class LodgeActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, related_name='lodge_activities')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='lodge_activities')
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    schedule = models.JSONField(default=dict)