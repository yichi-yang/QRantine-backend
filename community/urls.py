from django.urls import path, include
from rest_framework import routers
from .views import CommunityViewSet

router = routers.DefaultRouter()
router.register(r'community', CommunityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
