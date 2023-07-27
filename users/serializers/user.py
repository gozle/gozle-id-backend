from django.conf import settings
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    avatar = SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'first_name', 'last_name', 'birthday', 'balance',
                  'phone_number', 'reserve_phone_number', 'gender', 'region', 'theme', 'language', 'avatar',
                  'created_at', 'two_factor_auth', 'updated_at']

    @staticmethod
    def get_avatar(obj):
        if obj.avatar:
            return settings.DOMAIN + obj.avatar.url
        return None
