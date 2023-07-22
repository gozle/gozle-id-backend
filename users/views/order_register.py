import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Order


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
    amount = request.POST.get('amount')
    return_url = request.POST.get('returnUrl')
    fail_url = request.POST.get('failUrl')
    lang = request.POST.get('language')
    page_view = request.POST.get('pageView')

    # Save the order
    order = Order(user=user, description=description, amount=amount)
    order.save()

    request_url = ""

    # Data to be sent to the server
    data = {
        'userName': settings.MERCHANT_USERNAME,
        'password': settings.MERCHANT_PASSWORD,
        'orderNumber': order.id,
        'amount': order.amount,
        'currency': order.currency,
        'returnUrl': return_url,
        'failUrl': fail_url,
        'description': description,
        'language': lang,
        'pageView': page_view
    }
    # Send the request
    response = requests.post(request_url, data=data)

    # Get the response
    response_data = response.json()
    order.order_id = response_data['orderId']
    order.save()

    return Response(response_data)
