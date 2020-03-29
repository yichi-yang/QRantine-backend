from rest_framework import serializers
from .models import Location
from community.serializers import CommunitySerializer


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ("id", "plus_code", "name", "thumbnail", "community")
        read_only_fields = ("id",)


class LocationDetailSerializer(serializers.ModelSerializer):

    community = CommunitySerializer()

    class Meta:
        model = Location
        fields = ("id", "plus_code", "name", "thumbnail", "community")
        read_only_fields = ("id", "community")
