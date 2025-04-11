from rest_framework import serializers
from .models import Lodge, LodgeAccommodation, LodgeActivity
from accommodations.serializers import AccommodationSerializer
from activities.serializers import ActivitySerializer

class LodgeAccommodationSerializer(serializers.ModelSerializer):
    accommodation_details = AccommodationSerializer(source='accommodation', read_only=True)
    
    class Meta:
        model = LodgeAccommodation
        fields = ['id', 'lodge', 'accommodation', 'accommodation_details', 
                 'is_available', 'price', 'quantity']
        extra_kwargs = {
            'lodge': {'required': True}  # Ensure lodge is required
        }

    def validate_lodge(self, value):
        """Validate that the lodge exists"""
        if not value:
            raise serializers.ValidationError("Lodge is required")
        return value
class LodgeActivitySerializer(serializers.ModelSerializer):
    activity_details = ActivitySerializer(source='activity', read_only=True)
    
    class Meta:
        model = LodgeActivity
        fields = ['id', 'lodge', 'activity', 'activity_details', 
                 'is_available', 'price', 'schedule']
        extra_kwargs = {
            'lodge': {'required': True}
        }
        
    def validate_lodge(self, value):
        if not value:
            raise serializers.ValidationError("Lodge is required")
        return value

class LodgeSerializer(serializers.ModelSerializer):
    accommodations = LodgeAccommodationSerializer(source='lodgeaccommodation_set', many=True, read_only=True)
    activities = LodgeActivitySerializer(source='lodgeactivity_set', many=True, read_only=True)
    total_accommodations = serializers.SerializerMethodField()
    total_activities = serializers.SerializerMethodField()

    class Meta:
        model = Lodge
        fields = ['id', 'name', 'email', 'phone', 'address', 'description',
                 'is_active', 'type', 'created_at', 'accommodations', 'activities',
                 'total_accommodations', 'total_activities']

    def get_total_accommodations(self, obj):
        return obj.lodgeaccommodation_set.count()

    def get_total_activities(self, obj):
        return obj.lodgeactivity_set.count()