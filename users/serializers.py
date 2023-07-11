from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User

DOMAIN = 'https://i.gozle.com.tm'


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'first_name', 'last_name', 'birthday', 'balance', 'phone_number',
                  'avatar', 'created_at', 'two_factor_auth', 'updated_at']

    def get_avatar(self, obj):
        if obj.avatar:
            return DOMAIN + obj.avatar.url
        return None
