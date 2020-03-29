from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import action
from .serializers import (PhoneVerificationSerializer, SMSTokenObtainPairSerializer,
                          RecordSerialier, SendMessageSerializer, RecordDetailSerialier)
from authy.api import AuthyApiClient
from django.conf import settings
from rest_framework.response import Response
from .models import Record
from .permissions import RecordOwnerOnly
from twilio.rest import Client
from django.conf import settings
from location.models import Location

# Your Account SID from twilio.com/console
account_sid = settings.TWILIO_SID
# Your Auth Token from twilio.com/console
auth_token = settings.TWILIO_TOKEN
from_number = settings.TWILIO_FROM

client = Client(account_sid, auth_token)

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


class RecordViewSet(viewsets.ModelViewSet):

    serializer_class = RecordSerialier

    def get_serializer_class(self):
        if self.action == 'create':
            return RecordSerialier
        return RecordDetailSerialier

    def get_queryset(self):
        user_pk = self.request.user.pk if self.request.user.is_authenticated else None
        if self.action == 'list':
            queryset = Record.objects.filter(user=user_pk)
        else:
            queryset = Record.objects.all()
        return queryset

    permission_classes = [permissions.IsAuthenticated, RecordOwnerOnly]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        community_cases = None
        location = serializer.validated_data["location"]
        if location.community is not None:
            community_cases = location.community.cases

        serializer.save(user=request.user, community_cases=community_cases)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def message(self, request, pk=None):

        record = self.get_object()

        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        records = Record.objects.all().filter(
            location=record.location)
        phone_numbers = set((record.user.username for record in records))

        for number in phone_numbers:
            message = client.messages.create(
                to=number,
                from_=from_number,
                body=validated_data["message"])
            print(message.sid)

        return Response(status=status.HTTP_204_NO_CONTENT)
