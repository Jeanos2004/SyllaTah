from rest_framework import serializers
from django.utils import timezone
from django.db import transaction

from accommodations.models import Accommodation
from activities.models import Activity
from transports.models import Transport
from reservations.models import Reservation, Payment
from django.contrib.auth.models import User
from .validators import (
    validate_future_date, validate_check_out_after_check_in,
    validate_minimum_stay, validate_maximum_stay, validate_number_of_guests,
    validate_at_least_one_service, validate_reservation_period
)

class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les informations basiques de l'utilisateur"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        

class AccommodationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les informations d'hébergement"""
    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'location', 'description', 'price_per_night']

class TransportSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les informations de transport"""
    class Meta:
        model = Transport
        fields = ['id', 'transport_type', 'vehicle_type', 'category', 'luggage_capacity', 'capacity']

class ActivitySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les informations d'activité"""
    class Meta:
        model = Activity
        fields = ['id', 'name', 'location', 'min_participants', 'max_participants']

class PaymentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les paiements"""
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_type', 'payment_date', 'status']
        read_only_fields = ['payment_date', 'status']

# Sérialiseur de base pour les réservations
class ReservationBaseSerializer(serializers.ModelSerializer):
    """Sérialiseur de base pour les réservations"""
    class Meta:
        model = Reservation
        fields = ['id', 'reservation_number', 'status']

# Sérialiseur léger pour les hébergements dans les listes
class AccommodationLightSerializer(serializers.ModelSerializer):
    """Sérialiseur léger pour les informations d'hébergement"""
    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'location', 'price_per_night', 'description', 'capacity', 'amenities']

# Sérialiseur léger pour les transports dans les listes
class TransportLightSerializer(serializers.ModelSerializer):
    """Sérialiseur léger pour les informations de transport"""
    class Meta:
        model = Transport
        fields = ['id', 'transport_type', 'vehicle_type', 'capacity', 'luggage_capacity', 'category', 'price']

# Sérialiseur léger pour les activités dans les listes
class ActivityLightSerializer(serializers.ModelSerializer):
    """Sérialiseur léger pour les informations d'activité"""
    class Meta:
        model = Activity
        fields = ['id', 'name', 'location', 'description', 'min_participants', 'max_participants', 'price', 'duration']

# Sérialiseur pour la liste des réservations (GET /reservations/)
class ReservationListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la liste des réservations"""
    # Utilisation de sérialiseurs légers pour avoir des informations essentielles sans surcharger
    user = serializers.StringRelatedField(read_only=True)
    accommodation = AccommodationLightSerializer(read_only=True)
    transport = TransportLightSerializer(read_only=True)
    activity = ActivityLightSerializer(read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'reservation_number', 'status', 'payment_status',
            'user', 'accommodation', 'transport', 'activity',
            'check_in_date', 'check_out_date', 'total_price'
        ]
        read_only_fields = fields

# Sérialiseur pour la création de réservations (POST /reservations/)
class ReservationCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création de réservations"""
    # Relations avec PrimaryKeyRelatedField pour permettre la sélection par ID
    accommodation = serializers.PrimaryKeyRelatedField(queryset=Accommodation.objects.all(), required=False, allow_null=True)
    transport = serializers.PrimaryKeyRelatedField(queryset=Transport.objects.all(), required=False, allow_null=True)
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), required=False, allow_null=True)
    
    # Champs en lecture seule pour retourner les informations après création
    accommodation_details = AccommodationLightSerializer(source='accommodation', read_only=True)
    transport_details = TransportLightSerializer(source='transport', read_only=True)
    activity_details = ActivityLightSerializer(source='activity', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'accommodation', 'transport', 'activity',
            'accommodation_details', 'transport_details', 'activity_details',
            'check_in_date', 'check_out_date', 
            'number_of_guests', 'special_requests'
        ]
    
    def validate(self, data):
        """Validation simplifiée pour les réservations"""
        # Vérifier qu'au moins un service est sélectionné
        if not any([
            data.get('accommodation'),
            data.get('transport'),
            data.get('activity')
        ]):
            raise serializers.ValidationError({
                'non_field_errors': ['Au moins un service (hébergement, transport ou activité) doit être sélectionné']
            })
        
        # Vérification des dates si elles sont fournies
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_in and check_out and check_in >= check_out:
            raise serializers.ValidationError({
                'check_out_date': ['La date de départ doit être postérieure à la date d’arrivée']
            })
        
        return data

# Sérialiseur pour les détails d'une réservation (GET /reservations/{id}/)
class ReservationDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les détails d'une réservation"""
    # Relations détaillées pour avoir plus d'informations
    user = UserSerializer(read_only=True)
    accommodation = AccommodationSerializer(read_only=True)
    transport = TransportSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'reservation_number', 'status', 'payment_status',
            'user', 'accommodation', 'transport', 'activity',
            'check_in_date', 'check_out_date', 'reservation_date',
            'base_price', 'taxes', 'discounts', 'total_price', 'amount_paid',
            'number_of_guests', 'special_requests',
            'cancellation_reason', 'cancellation_date'
        ]
        read_only_fields = [
            'id', 'reservation_number', 'status', 'payment_status',
            'base_price', 'taxes', 'total_price', 'amount_paid',
            'reservation_date', 'cancellation_date'
        ]

# Sérialiseur pour la mise à jour d'une réservation (PUT/PATCH /reservations/{id}/)
class ReservationUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour d'une réservation"""
    class Meta:
        model = Reservation
        fields = [
            'check_in_date', 'check_out_date',
            'number_of_guests', 'special_requests'
        ]

# Sérialiseur principal utilisé par défaut dans la vue
class ReservationSerializer(ReservationDetailSerializer):
    """Sérialiseur principal pour les réservations"""
    pass