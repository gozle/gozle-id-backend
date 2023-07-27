from rest_framework import serializers


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class PhoneNumberAndVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    verification_code = serializers.CharField(max_length=4)
