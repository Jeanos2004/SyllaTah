from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccommodationViewSet, CategoryAccommodationViewSet, RoomTypeViewSets

router = DefaultRouter()
router.register(r'', AccommodationViewSet, basename='accommodation')
router.register(r'categories', CategoryAccommodationViewSet, basename='accommodation-category')
router.register(r'room-types', RoomTypeViewSets, basename='room-type')

urlpatterns = [
    path('', include(router.urls)),

]