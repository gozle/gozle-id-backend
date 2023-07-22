import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


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
    order_id = request.POST.get('orderId')

    request_url = ""

    data = {
        'userName': settings.MERCHANT_USERNAME,
        'password': settings.MERCHANT_PASSWORD,
        'orderId': order_id
    }

    response = requests.post(request_url, data=data)

    response_data = response.json()

    return Response(response_data)
