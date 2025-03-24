from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    image = models.ImageField(upload_to='activities/', null=True, blank=True)

    def __str__(self):
        return self.name