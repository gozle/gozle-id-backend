from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payment


class PaymentSerializer(ModelSerializer):
    client_name = SerializerMethodField('get_client_name')
    client_type = SerializerMethodField('get_client_type')

    class Meta:
        model = Payment
        fields = ["amount", "client_name", "client_type", "description", "created_at"]

    @staticmethod
    def get_client_name(obj):
        return obj.client.name

    @staticmethod
    def get_client_type(obj):
        return obj.client.service_type
