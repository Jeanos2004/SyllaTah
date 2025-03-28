from django.db import models
import uuid
from django.contrib.auth.models import User, AbstractUser
from accommodations.models import Accommodation
from activities.models import Activity

class LodgeAdmin(AbstractUser):
    lodge_id = models.UUIDField(unique=True, null=True)
    is_lodge_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)

    # Ajout des related_name pour résoudre les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='lodge_admin_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='lodge_admin_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Lodge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relations
    accommodations = models.ManyToManyField(Accommodation, through='LodgeAccommodation')
    activities = models.ManyToManyField(Activity, through='LodgeActivity')

    def __str__(self):
        return self.name

class LodgeAccommodation(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

class LodgeActivity(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    schedule = models.JSONField(default=dict)