from django.db import models
import uuid
#from lodge.models import Lodge



class RoomType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return f"{self.name}"

class CategoryAccommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, db_index=True)
    #lodge= models.ForeignKey(Lodge, on_delete=models.CASCADE, null=False, blank=False)
    location = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=500, db_index=True)
    category = models.ForeignKey(CategoryAccommodation, on_delete=models.CASCADE, blank = True, null = True)
    room_types = models.ManyToManyField(RoomType, blank=True)
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, null=True, blank=True)
    image = models.ImageField(upload_to='accommodations/assets', null=True, blank=True)
    capacity = models.PositiveIntegerField(default=1, help_text='Nombre maximum de personnes')

    def __str__(self):
        return self.name