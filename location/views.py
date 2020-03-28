from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer
from rest_framework.decorators import action


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    @action(detail=True)
    def plus_code(self, request, plus_code=None):

        location = self.filter_queryset(self.get_queryset())\
            .get(plus_code=plus_code)

        self.check_object_permissions(self.request, location)

        serializer = self.get_serializer(location)

        return Response(serializer.data, status=status.HTTP_200_OK)
