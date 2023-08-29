from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from jwcrypto.jwt import JWT
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import Order, Bank


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'amount': openapi.Schema(type=openapi.TYPE_STRING, description='The amount of order'),
                             "returnUrl": openapi.Schema(type=openapi.TYPE_STRING,
                                                         description="Return url if payment is successfull"),
                             "language": openapi.Schema(type=openapi.TYPE_STRING, description="Language. en|ru"),
                             "bank": openapi.Schema(type=openapi.TYPE_STRING, description="Bank id")
                         }
                     ),
                     responses={
                         200: openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                             'orderId': openapi.Schema(type=openapi.TYPE_STRING, description='Order ID in bank system'),
                             "formUrl": openapi.Schema(type=openapi.TYPE_STRING,
                                                         description="The Form url you need to redirect user to this form url"),
                            }
                         ),
                         400: openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                             'errorCode': openapi.Schema(type=openapi.TYPE_STRING, description='Error Code'),
                             "errorMessage": openapi.Schema(type=openapi.TYPE_STRING,
                                                         description="Error msesage to show user"),
                            }
                         )
                     })
@api_view(["POST"])
@csrf_exempt
def register_order(request):
    """
    Register an order

    Parameters:
         - amount: The amount of the order
         - returnUrl: The url to redirect to after the order is completed
         - failUrl: The url to redirect to if the order fails
         - language: The language of the order
         - pageView: The page view of the order
    Responses:
         - 200: Success
    """
    # Get data from the request
    user = request.user
    description = ""
    amount = int(request.data.get('amount')) * 100
    return_url = request.data.get('returnUrl')
    fail_url = request.data.get('failUrl', None)
    lang = request.data.get('language', "ru")
    page_view = "desktop"
    bank_id = request.data.get("bank")

    try:
        bank = Bank.objects.get(id=bank_id)
    except ObjectDoesNotExist:
        return Response({"message": "Bank not found"}, status=status.HTTP_404_NOT_FOUND)

    if Order.objects.filter(user=user, completed="pending").exists():
        if Order.objects.get(user=user, completed="pending").created_at > datetime.now() - timedelta(minutes=5):
            return Response({"message": "Order register requested recently, please wait 5 minutes"})

        Order.objects.get(user=user, completed="pending").delete()

    # Save the order
    order = Order(user=user, description=description, amount=amount, bank=bank)
    order.save()

    # Data to be sent to the server
    data = {
        'userName': bank.merchant_username,
        'password': bank.merchant_password,
        'orderNumber': order.get_order_id(),
        'amount': order.amount,
        'currency': order.bank.currency,
        'returnUrl': return_url,
        'failUrl': fail_url,
        'description': description,
        'language': lang,
        'pageView': page_view,
    }
    # Send the request
    response = requests.post(bank.register_url, data=data)

    # Get the response
    response_data = response.json()

    if int(response_data.get("errorCode")):
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    order.order_id = response_data.get('orderId')
    order.save()

    return Response(response_data)
