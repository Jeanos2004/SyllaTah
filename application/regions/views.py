from django.shortcuts import render
from rest_framework import viewsets
from .models import Region
from .serializers import RegionSerializer
from .permissions import RegionPermissions
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
""" 
def get_regions():
    regions = cache.get('regions')
    if not regions:
        regions = Region.objects.all()
        cache.set('regions', regions, timeout=60*15)  # Cache pour 15 minutes
    return regions """

@swagger_auto_schema(
    operation_description="Récupère la liste des régions",
    responses={200: RegionSerializer(many=True)}
)


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [RegionPermissions]

    def get_queryset(self):
        queryset = cache.get('regions')
        if queryset is None:
            queryset = Region.objects.all()
            cache.set('regions', queryset, timeout=60*15)
        return queryset
""" 
class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer """