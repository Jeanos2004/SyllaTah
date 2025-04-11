from django.shortcuts import render
from rest_framework import viewsets, permissions

from .filters import AccommodationFilter
from .pagination import LargeResultsSetPagination
from .models import Accommodation, CategoryAccommodation, RoomType
from .serializers import AccommodationSerializer, CategoryAccommodationSerializer, RoomTypeSerializer
from .permissions import IsAdminOrReadOnly
from django_filters import rest_framework as filters
from src.cache import CachedViewSetMixin


class AccommodationViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des hébergements.
    Inclut la pagination, le cache, et l'optimisation des requêtes.
    """
    serializer_class = AccommodationSerializer
    queryset = Accommodation.objects.all()  # Queryset par défaut
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AccommodationFilter
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.AllowAny]
    cache_timeout = 60 * 15  # 15 minutes de cache

    def get_queryset(self):
        """
        Optimise les requêtes en préchargeant les relations
        """
        queryset = Accommodation.objects.select_related(
            'category'
        ).prefetch_related(
            'room_types'
        )

        # Filtre par lodge_id si l'utilisateur est un admin de lodge
        if hasattr(self.request.user, 'is_lodge_admin') and self.request.user.is_lodge_admin:
            return queryset.filter(lodge_id=self.request.user.lodge_id)
        
        return queryset


class RoomTypeViewSets(CachedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des types de chambres.
    Inclut le cache et la pagination.
    """
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]
    pagination_class = LargeResultsSetPagination
    cache_timeout = 60 * 60  # 1 heure de cache


class CategoryAccommodationViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = CategoryAccommodation.objects.all()
    serializer_class = CategoryAccommodationSerializer
    permission_classes = [permissions.AllowAny]
    cache_timeout = 60 * 60  # 1 heure de cache