from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Transfer, CoinHistory


@api_view(["POST"])
@csrf_exempt
def transfer_verify(request):
    """
    Verify transfer request

    Params:
        - verification-code (string)
    Responses:
        - 200: Transferred successfully
        - 400: Transfer request is not sent
    """
    # Get data from request
    user = request.user
    verification_number = request.POST.get('verification-code')

    # Check if the verification number is correct
    transfer = Transfer.objects.filter(
        sender=user, verification_code=verification_number, completed=False).first()
    if transfer is None:
        return Response({'message': 'Transfer request is not sent'}, status=status.HTTP_400_BAD_REQUEST)

    # Transfer coins
    user.balance -= transfer.amount
    user.save()
    receiver = transfer.receiver
    receiver.balance += transfer.amount
    receiver.save()

    # Save coin history
    coin_history = CoinHistory()
    coin_history.user = receiver
    coin_history.amount = transfer.amount
    coin_history.source = user.phone_number
    coin_history.save()

    # Mark transfer as completed
    transfer.completed = True
    transfer.save()

    return Response({'message': 'Transferred successfully'})
