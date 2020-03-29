from rest_framework.viewsets import ModelViewSet
from .models import Community
from .serializers import CommunitySerializer


class CommunityViewSet(ModelViewSet):
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()