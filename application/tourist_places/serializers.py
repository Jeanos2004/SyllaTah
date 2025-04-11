from rest_framework import serializers
from .models import TouristPlace, Region, PlaceReview

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        # Résoudre le conflit de noms avec regions.serializers.RegionSerializer
        ref_name = 'TouristPlaceRegion'

class PlaceReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = PlaceReview
        fields = ['id', 'place', 'user', 'rating', 'comment', 
                 'visit_date', 'photos', 'created_at']
        read_only_fields = ['created_at']

class TouristPlaceSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        write_only=True,
        source='region'
    )
    reviews = PlaceReviewSerializer(many=True, read_only=True)
    average_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        source='rating',
        read_only=True
    )

    class Meta:
        model = TouristPlace
        fields = '__all__'
        read_only_fields = ['rating', 'total_reviews', 'created_at', 'updated_at']