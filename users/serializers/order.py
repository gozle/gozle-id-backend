from rest_framework import serializers

from users.models import Order


class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField("get_amount")

    class Meta:
        model = Order
        fields = "__all__"

    def get_amount(self, obj):
        return obj.amount / 100
