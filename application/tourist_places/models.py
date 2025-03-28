from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
class Region(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='regions/', null=True, blank=True)

    def __str__(self):
        return self.name
class PlaceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='places/categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Place Categories"

    def __str__(self):
        return self.name
class TouristPlace(models.Model):
    PLACE_TYPES = [
        ('historical', 'Site Historique'),
        ('natural', 'Site Naturel'),
        ('cultural', 'Site Culturel'),
        ('religious', 'Site Religieux'),
        ('entertainment', 'Divertissement')
    ]
    """ OPENING_HOURS = {
        'monday': '9:00 AM - 6:00 PM',
        'tuesday': '9:00 AM - 6:00 PM',
        'wednesday': '9:00 AM - 6:00 PM',
        'thursday': '9:00 AM - 6:00 PM',
        'friday': '9:00 AM - 6:00 PM',
        'saturday': '10:00 AM - 4:00 PM',
        'sunday': '10:00 AM - 4:00 PM'
    }  """

    name = models.CharField(max_length=200)
    description = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    place_type = models.CharField(max_length=20, choices=PLACE_TYPES, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    opening_hours = models.JSONField(default=dict)
    entrance_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contact_info = models.JSONField(default=dict)
    facilities = models.JSONField(default=list)
    accessibility = models.BooleanField(default=True)
    best_visit_time = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='tourist_places/', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.region.name}"

    def update_rating(self, new_rating):
        if self.total_reviews == 0:
            self.rating = new_rating
        else:
            self.rating = ((self.rating * self.total_reviews) + new_rating) / (self.total_reviews + 1)
        self.total_reviews += 1
        self.save()

class PlaceReview(models.Model):
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    visit_date = models.DateField()
    photos = models.ImageField(upload_to='place_reviews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['place', 'user']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.place.update_rating(self.rating)