from django.shortcuts import render
from rest_framework import viewsets, permissions

from .filters import AccommodationFilter
from .pagination import LargeResultsSetPagination
from .models import Accommodation, CategoryAccommodation, RoomType
from .serializers import AccommodationSerializer, CategoryAccommodationSerializer, RoomTypeSerializer
from .permissions import IsAdminOrReadOnly
from django_filters import rest_framework as filters
from src.cache import CachedViewSetMixin


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AccommodationFilter
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


class RoomTypeViewSets(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    permissions_classes = [permissions.IsAuthenticated]
    cache_timeout = 60 * 60


class CategoryAccommodationViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = CategoryAccommodation.objects.all()
    serializer_class = CategoryAccommodationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    cache_timeout = 60 * 60  # 1 heure de cache