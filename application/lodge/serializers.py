from rest_framework import serializers
from .models import Lodge, LodgeAccommodation, LodgeActivity
from accommodations.serializers import AccommodationSerializer
from activities.serializers import ActivitySerializer
from drf_spectacular.utils import extend_schema_field

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
    # Utilisation de related_name au lieu de _set pour éviter les problèmes avec drf-spectacular
    accommodations = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()
    total_accommodations = serializers.SerializerMethodField()
    total_activities = serializers.SerializerMethodField()

    class Meta:
        model = Lodge
        fields = ['id', 'name', 'email', 'phone', 'address', 'description',
                 'is_active', 'type', 'created_at', 'accommodations', 'activities',
                 'total_accommodations', 'total_activities']
        # Ajouter ref_name pour éviter les conflits de noms
        ref_name = 'LodgeDetail'

    @extend_schema_field(LodgeAccommodationSerializer(many=True))
    def get_accommodations(self, obj):
        return LodgeAccommodationSerializer(obj.lodge_accommodations.all(), many=True).data
        
    @extend_schema_field(LodgeActivitySerializer(many=True))
    def get_activities(self, obj):
        return LodgeActivitySerializer(obj.lodge_activities.all(), many=True).data

    @extend_schema_field(serializers.IntegerField())
    def get_total_accommodations(self, obj):
        return obj.lodge_accommodations.count()

    @extend_schema_field(serializers.IntegerField())
    def get_total_activities(self, obj):
        return obj.lodge_activities.count()