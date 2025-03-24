from django.db import models

class Transport(models.Model):
    company_name = models.CharField(max_length=200)
    transport_type = models.CharField(max_length=100)
    schedule = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.company_name