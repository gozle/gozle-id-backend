from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import CoinHistory, Login, User, Payment

DOMAIN = 'https://i.gozle.com.tm'


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'first_name', 'last_name', 'birthday', 'balance',
                  'phone_number',
                  'avatar', 'created_at', 'two_factor_auth', 'updated_at']

    def get_avatar(self, obj):
        if obj.avatar:
            return DOMAIN + obj.avatar.url
        return None


class ResourceUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', "phone_number", "email"]

    def get_avatar(self, obj):
        if obj.avatar:
            return DOMAIN + obj.avatar.url
        return None


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['id', "ip_address", "browser", "os", "device", "created_at"]


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField('get_client_name')
    client_type = serializers.SerializerMethodField('get_client_type')

    class Meta:
        model = Payment
        fields = ["amount", "client_name", "client_type", "description", "created_at"]

    def get_client_name(self, obj):
        return obj.client.name

    def get_client_type(self, obj):
        return obj.client.service_type
