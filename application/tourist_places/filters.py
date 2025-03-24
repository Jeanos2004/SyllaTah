from django_filters import rest_framework as filters
from .models import TouristPlace

class TouristPlaceFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    region = filters.NumberFilter(field_name="region__id")
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr='lte')
    
    class Meta:
        model = TouristPlace
        fields = ['name', 'region', 'min_rating', 'max_rating']
