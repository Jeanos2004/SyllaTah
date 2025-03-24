from rest_framework import serializers
from .models import Reservation
from accommodations.serializers import AccommodationSerializer
from transports.serializers import TransportSerializer
from activities.serializers import ActivitySerializer

class ReservationSerializer(serializers.ModelSerializer):
    #accommodation = AccommodationSerializer(read_only=True)
    #transport = TransportSerializer(read_only=True)
    #activity = ActivitySerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'