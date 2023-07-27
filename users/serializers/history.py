from rest_framework.serializers import ModelSerializer

from users.models import CoinHistory


class HistorySerializer(ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = "__all__"
