from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccommodationViewSet, CategoryAccommodationViewSet, RoomTypeViewSets

router = DefaultRouter()
router.register(r'accommodation', AccommodationViewSet)
router.register(r'type', CategoryAccommodationViewSet)
router.register(r'roomtype', RoomTypeViewSets)

urlpatterns = [
    path('', include(router.urls)),

]