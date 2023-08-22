import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import Order


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'orderId': openapi.Schema(type=openapi.TYPE_STRING,
                                                       description='Order id returned by bank'),
                             'language': openapi.Schema(type=openapi.TYPE_STRING, description='Response Language'),
                         }
                     ),
                     responses={
                         200: "Order accepted successfully",
                         202: "Order already accepted",
                         400: openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'ErrorCode': openapi.Schema(type=openapi.TYPE_STRING,
                                                       description='Error Code'),
                             'ErrorMessage': openapi.Schema(type=openapi.TYPE_STRING, description='Error message to show user'),
                         }
                     )
                     })
@api_view(["POST"])
@csrf_exempt
def order_status(request):
    """
    Check the status of an order.
    Parameters:
        orderId: The order ID.

    Responses:
        200: The order status.
    """
    order_id = request.data.get('orderId')
    language = request.data.get('language', 'en')

    request_url = "https://epg.senagatbank.com.tm/epg/rest/getOrderStatus.do"

    data = {
        'userName': settings.MERCHANT_USERNAME,
        'password': settings.MERCHANT_PASSWORD,
        'orderId': order_id,
        'language': language
    }

    response = requests.post(request_url, data=data)

    response_data = response.json()

    if response_data.get("errorCode", 0) != 0:
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    if response_data.get("OrderStatus", 0) == 2:
        try:
            order = Order.objects.get(order_id=order_id)
        except ObjectDoesNotExist:
            return Response({"message": "Order is not found"}, status=status.HTTP_404_NOT_FOUND)
        if order.status != "completed":
            order.status = "completed"
            user = request.user
            user.balance += order.amount / 100
            user.save()
            order.save()
            return Response({"message": "Order accepted successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Order already accepted"}, status=status.HTTP_202_ACCEPTED)
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
