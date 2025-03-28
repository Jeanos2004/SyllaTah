from django.db import models

#from lodge.models import Lodge



class RoomType(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return f"{self.name}"

class CategoryAccommodation(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    #lodge= models.ForeignKey(Lodge, on_delete=models.CASCADE, null=False, blank=False)
    location = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=500, db_index=True)
    category = models.ForeignKey(CategoryAccommodation, on_delete=models.CASCADE, blank = True, null = True)
    room_types = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True, blank=True)
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, null=True, blank=True)
    image = models.ImageField(upload_to='accommodations/assets', null=True, blank=True)

    def __str__(self):
        return self.name