from rest_framework import serializers
from .models import Region

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
""" 
class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = '__all__' """