from typing import override
from django.db import models
import uuid





class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='regions/assets', null=True, blank=True)

    def __str__(self):
        return self.name

""" class Ville(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique = True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=False, null=False)


    @override
    def __str__(self):
        return self._check_field_name_clashes """