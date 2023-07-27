from django.conf import settings
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Login


class LoginSerializer(ModelSerializer):
    icon = SerializerMethodField('get_icon')

    class Meta:
        model = Login
        fields = ['id', "ip_address", "browser", "icon", "os", "device", "created_at"]

    @staticmethod
    def get_icon(obj):
        icons = {
            "Chrome Mobile": "browser_icons/chrome.png",
            "Chrome": "browser_icons/chrome.png",
            "Edge": "browser_icons/edge.png",
            "Yandex Browser": "browser_icons/yandex.png",
            "Mobile Safari": "browser_icons/safari.png",
        }
        return settings.DOMAIN + settings.STATIC_URL + icons.get(obj.browser, "browser_icons/default.png")
