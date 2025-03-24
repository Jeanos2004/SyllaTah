from rest_framework import serializers
from .models import TouristPlace
from regions.serializers import RegionSerializer

class TouristPlaceSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)  # Pour afficher les détails de la région

    class Meta:
        model = TouristPlace
        fields = '__all__'