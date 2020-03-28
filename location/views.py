from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
