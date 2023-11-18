from django.conf import settings
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import User


class ResourceUserSerializer(ModelSerializer):
    avatar = SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', "phone_number", "email",
                  "theme", "language", "region", "updated_at"]

    @staticmethod
    def get_avatar(obj):
        if obj.avatar:
            return settings.DOMAIN + obj.avatar.url
        return None
