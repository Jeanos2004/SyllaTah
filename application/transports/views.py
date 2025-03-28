from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg
from .models import Transport, TransportCategory, TransportReview
from .serializers import TransportSerializer, TransportCategorySerializer, TransportReviewSerializer

class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'transport_type', 'vehicle_type', 'description']
    ordering_fields = ['price', 'rating', 'created_at']

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        transport = self.get_object()
        serializer = TransportReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(transport=transport, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def reviews(self, request, pk=None):
        transport = self.get_object()
        reviews = transport.reviews.all()
        serializer = TransportReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def availability(self, request, pk=None):
        transport = self.get_object()
        return Response({
            'status': transport.status,
            'schedule': transport.schedule
        })

class TransportCategoryViewSet(viewsets.ModelViewSet):
    queryset = TransportCategory.objects.all()
    serializer_class = TransportCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def transports(self, request, pk=None):
        category = self.get_object()
        transports = Transport.objects.filter(category=category)
        serializer = TransportSerializer(transports, many=True)
        return Response(serializer.data)