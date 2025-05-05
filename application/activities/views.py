from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg

from src.pagination import CustomPagination
from .models import Activity, ActivityCategory, ActivityReview
from .serializers import ActivitySerializer, ActivityCategorySerializer, ActivityReviewSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'location', 'difficulty']
    ordering_fields = ['price', 'rating', 'created_at', 'duration']

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        activity = self.get_object()
        serializer = ActivityReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(activity=activity, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def reviews(self, request, pk=None):
        activity = self.get_object()
        reviews = activity.reviews.all()
        serializer = ActivityReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def similar_activities(self, request, pk=None):
        activity = self.get_object()
        similar = Activity.objects.filter(
            category=activity.category
        ).exclude(id=activity.id)[:5]
        serializer = ActivitySerializer(similar, many=True)
        return Response(serializer.data)

class ActivityCategoryViewSet(viewsets.ModelViewSet):
    queryset = ActivityCategory.objects.all()
    serializer_class = ActivityCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def activities(self, request, pk=None):
        category = self.get_object()
        activities = Activity.objects.filter(category=category)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)