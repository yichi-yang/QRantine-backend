from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ("id", "plus_code", "name", "thumbnail", "community")
        read_only_fields = ("id",)
