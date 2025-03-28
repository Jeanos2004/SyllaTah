from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import authenticate, get_user_model
from rest_framework.fields import MaxLengthValidator


User = get_user_model()
class ActivityCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='activities/categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Activity Categories"

    def __str__(self):
        return self.name

class Activity(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
        ('expert', 'Expert')
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    duration = models.DurationField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    min_participants = models.IntegerField(default=1, null=True, blank=True)
    max_participants = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    equipment_provided = models.BooleanField(default=False)
    equipment_required = models.TextField(blank=True)
    age_restriction = models.PositiveIntegerField(null=True, blank=True)
    fitness_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    image = models.ImageField(upload_to='activities/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0),MaxLengthValidator(5)])
    total_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def update_rating(self, new_rating):
        if self.total_reviews == 0:
            self.rating = new_rating
        else:
            self.rating = ((self.rating * self.total_reviews) + new_rating) / (self.total_reviews + 1)
        self.total_reviews += 1
        self.save()

class ActivityReview(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photos = models.ImageField(upload_to='activities/reviews/', null=True, blank=True)

    class Meta:
        unique_together = ['activity', 'user']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.activity.update_rating(self.rating)