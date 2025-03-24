from django.shortcuts import render
from rest_framework import viewsets
from .models import Transport
from .serializers import TransportSerializer
from .permissions import TransportPermissions
from django.db.models import Avg
from .filters import TransportFilter
from django_filters import rest_framework as filters
from src.cache import CachedViewSetMixin

class TransportViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [TransportPermissions]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TransportFilter
    cache_timeout = 60 * 15  # 15 minutes de cache

    def get_average_price(self):
        return Transport.objects.aggregate(Avg('price'))