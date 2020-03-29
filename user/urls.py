from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import PhoneVerificationView, SMSTokenObtainPairView, RecordViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("", RecordViewSet, basename="record")

urlpatterns = [
    path('token/', SMSTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('verify/', PhoneVerificationView.as_view(), name='phone_verify'),
    path("record/", include(router.urls))
]
