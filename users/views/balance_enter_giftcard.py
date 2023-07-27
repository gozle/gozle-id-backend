from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import GiftCard, CoinHistory


@swagger_auto_schema(method='post',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'code': openapi.Schema(type=openapi.TYPE_STRING, description='The Code of GiftCard'),
                         }
                     ),
                     manual_parameters=[JWT_TOKEN],
                     responses={200: 'Amount of giftcard',
                                403: 'Invalid Code'}
                     )
@api_view(["POST"])
@transaction.atomic
@csrf_exempt
def enterCard(request):
    """
    View to enter a gift card.

    Params:
        code (str): The gift card code to use.
    Responses:
        200: Gift card successfully entered.
        403: Invalid code.
    """
    # Get data from request
    code = request.data.get("code")

    # Check if the code is valid
    if not GiftCard.objects.filter(code=code, used=False).exists():
        return Response({"message": "Invalid Code"}, status=status.HTTP_403_FORBIDDEN)

    card = GiftCard.objects.get(code=code, used=False)

    # Use Card
    user = request.user
    card.use(user)

    return Response({"amount": card.value})
