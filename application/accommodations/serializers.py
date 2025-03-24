from rest_framework import serializers
from .models import Accommodation, CategoryAccommodation, RoomType


class AccommodationSerializer(serializers.ModelSerializer):
    def validate_price_per_night(self, value):
        if value < 0:
            raise serializers.ValidationError("Le prix ne peut pas être négatif.")
        return value
    class Meta:
        model = Accommodation
        fields = '__all__'


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = RoomType
        fields = '__all__'

class CategoryAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryAccommodation
        fields = '__all__'

        