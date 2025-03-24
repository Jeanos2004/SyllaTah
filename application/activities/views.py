from django.shortcuts import render
from rest_framework import viewsets
from .models import Activity
from .serializers import ActivitySerializer
from .permissions import ActivityPermissions

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [ActivityPermissions]