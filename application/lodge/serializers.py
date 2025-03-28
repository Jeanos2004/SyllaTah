from rest_framework import serializers
from django.contrib.auth import get_user_model
from accommodations.serializers import AccommodationSerializer
from activities.serializers import ActivitySerializer
from .models import Lodge, LodgeAdmin, LodgeAccommodation, LodgeActivity

class LodgeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgeAdmin
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'position', 'lodge_id')
        read_only_fields = ('lodge_id',)

class LodgeAccommodationSerializer(serializers.ModelSerializer):
    accommodation_details = AccommodationSerializer(source='accommodation', read_only=True)
    
    class Meta:
        model = LodgeAccommodation
        fields = ('id', 'lodge', 'accommodation', 'accommodation_details', 
                 'is_available', 'price', 'quantity')

    def validate(self, data):
        if data.get('price', 0) < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return data

class LodgeActivitySerializer(serializers.ModelSerializer):
    activity_details = ActivitySerializer(source='activity', read_only=True)
    
    class Meta:
        model = LodgeActivity
        fields = ('id', 'lodge', 'activity', 'activity_details', 
                 'is_available', 'price', 'schedule')

    def validate_schedule(self, value):
        required_keys = ['days', 'hours']
        if not all(key in value for key in required_keys):
            raise serializers.ValidationError("Schedule must contain days and hours")
        return value

class LodgeSerializer(serializers.ModelSerializer):
    accommodations = LodgeAccommodationSerializer(source='lodgeaccommodation_set', many=True, read_only=True)
    activities = LodgeActivitySerializer(source='lodgeactivity_set', many=True, read_only=True)
    total_accommodations = serializers.SerializerMethodField()
    total_activities = serializers.SerializerMethodField()

    class Meta:
        model = Lodge
        fields = ('id', 'name', 'email', 'phone', 'address', 'description',
                 'is_active', 'created_at', 'accommodations', 'activities',
                 'total_accommodations', 'total_activities')

    def get_total_accommodations(self, obj):
        return obj.accommodations.count()

    def get_total_activities(self, obj):
        return obj.activities.count()

class LodgeDashboardSerializer(serializers.ModelSerializer):
    available_accommodations = serializers.SerializerMethodField()
    available_activities = serializers.SerializerMethodField()
    recent_bookings = serializers.SerializerMethodField()
    revenue_stats = serializers.SerializerMethodField()

    class Meta:
        model = Lodge
        fields = ('id', 'name', 'available_accommodations', 'available_activities',
                 'recent_bookings', 'revenue_stats')

    def get_available_accommodations(self, obj):
        return obj.lodgeaccommodation_set.filter(is_available=True).count()

    def get_available_activities(self, obj):
        return obj.lodgeactivity_set.filter(is_available=True).count()

    def get_recent_bookings(self, obj):
        # Logique pour obtenir les réservations récentes
        return []

    def get_revenue_stats(self, obj):
        # Logique pour calculer les statistiques de revenus
        return {
            'daily': 0,
            'weekly': 0,
            'monthly': 0
        }