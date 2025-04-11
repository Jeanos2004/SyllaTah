from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
import logging
from .models import Reservation
from .serializers import (
    ReservationSerializer, ReservationListSerializer, 
    ReservationCreateSerializer, ReservationDetailSerializer,
    ReservationUpdateSerializer
)
from core.mixins import OptimizedQuerySetMixin, SerializerByActionMixin
from core.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from core.logging import APILoggingMixin

# Configuration du logger pour ce module
logger = logging.getLogger('api_monitoring')

class ReservationViewSet(APILoggingMixin, OptimizedQuerySetMixin, SerializerByActionMixin, viewsets.ModelViewSet):
    """
    Vue pour la gestion des réservations avec des sérialiseurs spécifiques pour chaque opération.
    Utilise des mixins pour optimiser les performances et la sélection des sérialiseurs.
    Sécurisé avec des permissions personnalisées.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    # Optimisation des requêtes avec select_related
    select_related_fields = ['user', 'accommodation', 'transport', 'activity']
    
    # Configuration des sérialiseurs par action
    serializer_classes = {
        'list': ReservationListSerializer,
        'create': ReservationCreateSerializer,
        'retrieve': ReservationDetailSerializer,
        'update': ReservationUpdateSerializer,
        'partial_update': ReservationUpdateSerializer,
    }
    
    def perform_create(self, serializer):
        """Crée une réservation en l'associant à l'utilisateur connecté"""
        # Associer l'utilisateur connecté à la réservation
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annule une réservation"""
        reservation = self.get_object()
        reservation.status = 'cancelled'
        reservation.cancellation_reason = request.data.get('reason', '')
        reservation.save()
        return Response({'status': 'Réservation annulée avec succès'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def process_reservation(self, request, pk=None):
        """Traitement simplifié de la réservation sans paiement"""
        reservation = self.get_object()
        
        if reservation.status == 'cancelled':
            return Response(
                {'error': 'Cette réservation a été annulée'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = 'confirmed'
        reservation.save()
        return Response({'status': 'Réservation confirmée avec succès'}, status=status.HTTP_200_OK)