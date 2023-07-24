from rest_framework import serializers
from users.models import CoinHistory, Login, User, Payment

DOMAIN = 'https://i.gozle.com.tm'


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'first_name', 'last_name', 'birthday', 'balance',
                  'phone_number', 'region', 'theme', 'language', 'avatar', 'created_at', 'two_factor_auth',
                  'updated_at']

    @staticmethod
    def get_avatar(obj):
        if obj.avatar:
            return DOMAIN + obj.avatar.url
        return None


class ResourceUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', "phone_number", "email",
                  "theme", "language", "region"]

    @staticmethod
    def get_avatar(obj):
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

    @staticmethod
    def get_client_name(obj):
        return obj.client.name

    @staticmethod
    def get_client_type(obj):
        return obj.client.service_type
