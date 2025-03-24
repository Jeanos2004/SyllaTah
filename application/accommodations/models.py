from django.db import models



class RoomType(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class CategoryAccommodation(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    location = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=500, db_index=True)
    category = models.ForeignKey(CategoryAccommodation, on_delete=models.CASCADE, blank = True, null = True)
    room_types = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True, blank=True)
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    image = models.ImageField(upload_to='accommodations/assets', null=True, blank=True)

    def __str__(self):
        return self.name