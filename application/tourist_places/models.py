from django.db import models
from regions.models import Region

class TouristPlace(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tourist_places')
    description = models.TextField()
    opening_hours = models.CharField(max_length=100, null=True, blank=True)
    entrance_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tourist_places/', null=True, blank=True)

    def __str__(self):
        return self.name