from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import TouristPlace, Region, PlaceReview
from .serializers import TouristPlaceSerializer, RegionSerializer, PlaceReviewSerializer

class TouristPlaceViewSet(viewsets.ModelViewSet):
    queryset = TouristPlace.objects.all()
    serializer_class = TouristPlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'region__name', 'place_type']
    ordering_fields = ['rating', 'created_at', 'entrance_fee']

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        place = self.get_object()
        serializer = PlaceReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(place=place, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def nearby_places(self, request, pk=None):
        place = self.get_object()
        nearby = TouristPlace.objects.filter(
            region=place.region
        ).exclude(id=place.id)[:5]
        serializer = TouristPlaceSerializer(nearby, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def featured(self, request):
        featured_places = self.get_queryset().order_by('-rating')[:5]
        serializer = self.get_serializer(featured_places, many=True)
        return Response(serializer.data)

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def places(self, request, pk=None):
        region = self.get_object()
        places = TouristPlace.objects.filter(region=region)
        serializer = TouristPlaceSerializer(places, many=True)
        return Response(serializer.data)