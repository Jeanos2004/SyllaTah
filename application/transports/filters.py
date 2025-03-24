from django_filters import rest_framework as filters
from .models import Transport

class TransportFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    type = filters.CharFilter(field_name="type", lookup_expr='iexact')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    class Meta:
        model = Transport
        fields = ['name', 'type', 'min_price', 'max_price']
