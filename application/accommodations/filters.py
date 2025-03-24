from django_filters import rest_framework as filters
from .models import Accommodation

class AccommodationFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')
    location = filters.CharFilter(field_name="location", lookup_expr='icontains')

    class Meta:
        model = Accommodation
        fields = ['min_price', 'max_price', 'location']