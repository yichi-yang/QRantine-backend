from django.urls import path, include
from rest_framework import routers
from .views import LocationViewSet

router = routers.DefaultRouter()
router.register(r'location', LocationViewSet)

urlpatterns = [
    path("location/plus_code/<plus_code>/",
         LocationViewSet.as_view({'get': 'plus_code'})),
    path("", include(router.urls)),
]
