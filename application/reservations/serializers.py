from rest_framework import serializers

from accommodations.models import Accommodation
from activities.models import Activity
from transports.models import Transport
from reservations.models import Reservation, Payment
from django.contrib.auth.models import User

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

class ReservationSerializer(serializers.ModelSerializer):
    """Sérialiseur principal pour les réservations"""
    user = UserSerializer(read_only=True)
    accommodation = AccommodationSerializer(read_only=True)
    transport = TransportSerializer(read_only=True)
    activity = ActivitySerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)


    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'reservation_number', 'status', 'status_display',
            'payment_status', 'payment_status_display', 'accommodation',
            'transport', 'activity', 'check_in_date', 'check_out_date',
            'base_price', 'taxes', 'discounts', 'total_price', 'amount_paid',
            'number_of_guests', 'special_requests', 'payments',
            'reservation_date', 'cancellation_reason', 'cancellation_date'
        ]
        read_only_fields = [
            'reservation_number', 'status', 'payment_status',
            'base_price', 'taxes', 'total_price', 'amount_paid',
            'reservation_date', 'cancellation_date'
        ]

    def validate(self, data):
        """
        Validation personnalisée pour les réservations
        """
        # Vérifier qu'au moins un service est sélectionné
        if not any([
            data.get('accommodation'),
            data.get('transport'),
            data.get('activity')
        ]):
            raise serializers.ValidationError(
                "Au moins un service (hébergement, transport ou activité) doit être sélectionné"
            )

        # Vérifier les dates
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError(
                "La date de départ doit être postérieure à la date d'arrivée"
            )

        # Vérifier le nombre de personnes
        if data['number_of_guests'] < 1:
            raise serializers.ValidationError(
                "Le nombre de personnes doit être au moins 1"
            )

        return data

    def create(self, validated_data):
        """
        Création d'une réservation avec génération automatique du numéro
        """
        validated_data['user'] = self.context['request'].user
        reservation = Reservation.objects.create(**validated_data)
        reservation.calculate_total_price()
        return reservation