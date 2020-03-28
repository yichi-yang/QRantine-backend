from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import generics, status
from .serializers import PhoneVerificationSerializer, SMSTokenObtainPairSerializer
from authy.api import AuthyApiClient
from django.conf import settings
from rest_framework.response import Response

authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


class PhoneVerificationView(generics.GenericAPIView):

    serializer_class = PhoneVerificationSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        authy_api.phones.verification_start(
            validated_data['phone_number'],
            validated_data['country_code'],
            code_length=6
        )

        return Response(validated_data, status=status.HTTP_200_OK)


class SMSTokenObtainPairView(TokenViewBase):
    
    serializer_class = SMSTokenObtainPairSerializer
