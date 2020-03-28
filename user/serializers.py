from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import phonenumbers
from phonenumbers import NumberParseException
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from authy.api import AuthyApiClient
from django.conf import settings
from .models import User, Record

authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


class PhoneVerificationSerializer(serializers.Serializer):
    country_code = serializers.CharField()
    phone_number = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs['country_code'].startswith("+"):
            attrs['country_code'] = "+" + attrs['country_code']
        phone_number = attrs['country_code'] + attrs['phone_number']
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                raise serializers.ValidationError(_("Invalid phone number"))
        except NumberParseException as e:
            raise serializers.ValidationError(_("Invalid phone number"))
        return attrs


class SMSTokenObtainPairSerializer(serializers.Serializer):

    country_code = serializers.CharField()
    phone_number = serializers.CharField()
    token = PasswordField()

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        verification = authy_api.phones.verification_check(
            attrs['phone_number'],
            attrs['country_code'],
            attrs['token']
        )
        if not verification.ok():
            raise AuthenticationFailed(
                code='invalid_verification_code'
            )

        username = attrs['country_code'] + attrs['phone_number']

        user = None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            user = User.objects.create_user(username)

        if user is None or not user.is_active:
            raise AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        refresh = RefreshToken.for_user(user)

        tokens = {}

        tokens['refresh'] = str(refresh)
        tokens['access'] = str(refresh.access_token)

        return tokens


class RecordSerialier(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ("id", "user", "location", "visited_at")
        read_only_fields = ("id", "user", "visited_at")


class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)
