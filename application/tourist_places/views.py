from django.shortcuts import render

from rest_framework import viewsets
from .models import TouristPlace
from .serializers import TouristPlaceSerializer
from .permissions import TouristPlacePermissions
from src.cache import CachedViewSetMixin
from .filters import TouristPlaceFilter
from django_filters import rest_framework as filters

class TouristPlaceViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = TouristPlace.objects.all()
    serializer_class = TouristPlaceSerializer
    permission_classes = [TouristPlacePermissions]
    cache_timeout = 60 * 30  # 30 minutes de cache
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TouristPlaceFilter