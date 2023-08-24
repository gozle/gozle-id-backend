from rest_framework import serializers

from users.models import City


class CitySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("get_name")

    class Meta:
        model = City
        fields = ["id", "slug", "name"]

    def get_name(self, obj):
        lang = self.context.get("lang")
        if lang == "ru":
            return obj.name_ru
        elif lang == "tk":
            return obj.name_tk
        return obj.name
