from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend

from .models import Lodge, LodgeAccommodation, LodgeActivity, LodgeStaff, LodgeAmenity, LodgeReview, LodgeGallery
from .serializers import (
    LodgeSerializer, LodgeAccommodationSerializer, LodgeActivitySerializer,
    LodgeStaffSerializer, LodgeAmenitySerializer, LodgeReviewSerializer,
    LodgeGallerySerializer, LodgeDashboardSerializer
)
from .permissions import (
    IsLodgeAdmin, CanManageLodgeAccommodations, CanManageLodgeActivities,
    IsLodgeStaff
)

class LodgeAuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user and user.is_lodge_admin:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'lodge_id': user.lodge_id,
                'user_info': {
                    'name': user.get_full_name(),
                    'email': user.email,
                    'position': user.position
                }
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LodgeViewSet(viewsets.ModelViewSet):
    serializer_class = LodgeSerializer
    permission_classes = [IsLodgeAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'city', 'is_active']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        return Lodge.objects.filter(id=self.request.user.lodge_id)

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        lodge = self.get_object()
        serializer = LodgeDashboardSerializer(lodge)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def advanced_statistics(self, request, pk=None):
        lodge = self.get_object()
        today = timezone.now().date()
        last_month = today - timedelta(days=30)
        last_year = today - timedelta(days=365)

        # Statistiques détaillées des réservations
        booking_stats = lodge.bookings.aggregate(
            total_revenue=Sum('total_price'),
            average_daily_revenue=Avg('total_price'),
            total_bookings=Count('id'),
            monthly_revenue=Sum('total_price', 
                filter=Q(created_at__gte=last_month)),
            yearly_revenue=Sum('total_price', 
                filter=Q(created_at__gte=last_year))
        )

        # Analyse des tendances
        monthly_trends = lodge.bookings.filter(
            created_at__gte=last_year
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            booking_count=Count('id'),
            revenue=Sum('total_price')
        ).order_by('month')

        # Performance des accommodations
        accommodation_performance = lodge.accommodations.annotate(
            booking_count=Count('lodgebooking'),
            total_revenue=Sum('lodgebooking__total_price'),
            average_rating=Avg('lodgebooking__rating')
        ).values('id', 'name', 'booking_count', 'total_revenue', 'average_rating')

        return Response({
            'booking_stats': booking_stats,
            'monthly_trends': monthly_trends,
            'accommodation_performance': accommodation_performance,
            'occupancy_rate': self.calculate_occupancy_rate(lodge),
        })

    @action(detail=True, methods=['post'])
    def manage_availability(self, request, pk=None):
        lodge = self.get_object()
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        accommodation_id = request.data.get('accommodation_id')
        is_available = request.data.get('is_available', True)

        try:
            accommodation = lodge.accommodations.get(id=accommodation_id)
            availability = accommodation.update_availability(
                start_date, end_date, is_available)
            return Response(availability)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def revenue_forecast(self, request, pk=None):
        lodge = self.get_object()
        upcoming_bookings = lodge.bookings.filter(
            check_in_date__gte=timezone.now().date()
        ).aggregate(
            confirmed_revenue=Sum('total_price', 
                filter=Q(status='confirmed')),
            pending_revenue=Sum('total_price', 
                filter=Q(status='pending'))
        )

        seasonal_analysis = self.analyze_seasonal_trends(lodge)

        return Response({
            'upcoming_bookings': upcoming_bookings,
            'seasonal_analysis': seasonal_analysis,
            'forecast': self.calculate_revenue_forecast(lodge)
        })

    def calculate_occupancy_rate(self, lodge):
        today = timezone.now().date()
        total_rooms = lodge.accommodations.count()
        occupied_rooms = lodge.bookings.filter(
            check_in_date__lte=today,
            check_out_date__gte=today,
            status='confirmed'
        ).count()
        
        return {
            'current_occupancy': (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0,
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms
        }

    def analyze_seasonal_trends(self, lodge):
        # Analyse des tendances saisonnières
        return lodge.bookings.annotate(
            season=ExtractQuarter('check_in_date')
        ).values('season').annotate(
            avg_revenue=Avg('total_price'),
            booking_count=Count('id')
        ).order_by('season')

    def calculate_revenue_forecast(self, lodge):
        # Calcul des prévisions de revenus basé sur l'historique
        historical_data = lodge.bookings.filter(
            status='completed'
        ).annotate(
            month=TruncMonth('check_in_date')
        ).values('month').annotate(
            revenue=Sum('total_price')
        ).order_by('-month')[:12]

        # Logique de prévision
        return self.apply_forecasting_model(historical_data)

class LodgeActivityViewSet(viewsets.ModelViewSet):
    serializer_class = LodgeActivitySerializer
    permission_classes = [CanManageLodgeActivities]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_available']
    search_fields = ['activity__name']

    def get_queryset(self):
        return LodgeActivity.objects.filter(lodge__id=self.request.user.lodge_id)

    def perform_create(self, serializer):
        serializer.save(lodge_id=self.request.user.lodge_id)

class LodgeStaffViewSet(viewsets.ModelViewSet):
    serializer_class = LodgeStaffSerializer
    permission_classes = [IsLodgeAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'is_active']

    def get_queryset(self):
        return LodgeStaff.objects.filter(lodge__id=self.request.user.lodge_id)

class LodgeAmenityViewSet(viewsets.ModelViewSet):
    serializer_class = LodgeAmenitySerializer
    permission_classes = [IsLodgeStaff]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return LodgeAmenity.objects.filter(lodge__id=self.request.user.lodge_id)

class LodgeReviewViewSet(viewsets.ModelViewSet):
    serializer_class = LodgeReviewSerializer
    permission_classes = [IsLodgeStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating']
    ordering_fields = ['created_at', 'rating']

    def get_queryset(self):
        return LodgeReview.objects.filter(lodge__id=self.request.user.lodge_id)

class LodgeGalleryViewSet(viewsets.ModelViewSet):
    serializer_class = LodgeGallerySerializer
    permission_classes = [IsLodgeStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_main']

    def get_queryset(self):
        return LodgeGallery.objects.filter(lodge__id=self.request.user.lodge_id)
