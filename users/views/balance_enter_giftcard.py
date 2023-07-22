from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import GiftCard, CoinHistory


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
    code = request.POST.get("code")

    # Check if the code is valid
    if not GiftCard.objects.filter(code=code, used=False).exists():
        return Response({"message": "Invalid Code"}, status=status.HTTP_403_FORBIDDEN)

    card = GiftCard.objects.get(code=code, used=False)

    # Update user balance
    user = request.user
    user.balance += card.value
    card.used = True
    card.save()
    user.save()

    # Add coin history
    coin_history = CoinHistory()
    coin_history.user = user
    coin_history.amount = card.value
    coin_history.source = "GiftCard"
    coin_history.save()

    return Response({"amount": card.value})
