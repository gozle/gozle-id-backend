import random

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sms import sms_sender
from users.models import User, Transfer


@api_view(["POST"])
@csrf_exempt
def transfer_request(request):
    """
    Transfer request endpoint
    Parameters:
         - send_to: phone number of receiver
         - amount: amount of GC to transfer
    Responses:
         - 200: Verification code sent
         - 404: Receiver not found
         - 409: User's balance is smaller than amount
    """
    # Get data from request
    user = request.user
    send_to = request.POST.get('send_to')
    amount = int(request.POST.get('amount'))

    # Check if the receiver exists
    receiver = User.objects.filter(phone_number=send_to).first()
    if receiver is None:
        return Response({'message': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the amount is valid
    if amount > user.balance:
        return Response({'message': "User's balance is smaller than amount"}, status=status.HTTP_409_CONFLICT)

    verification_number = random.randint(10000, 99999)
    # Create transfer
    transfer = Transfer.objects.create(sender=user, receiver=receiver, amount=amount,
                                       completed=False, verification_code=verification_number)
    transfer.save()

    # Send SMS to sender and save verification code
    sms_sender.send(user.phone_number, 'Transferring {} GC to {}. Verification code: {}'.format(
        amount, receiver.phone_number, verification_number))
    transfer.verification_code = verification_number
    transfer.save()

    return Response({'message': 'Verification code sent'})
