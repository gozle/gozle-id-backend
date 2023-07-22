from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Application, Payment


@api_view(['POST'])
@csrf_exempt
def register_payment(request):
    # Get data from request
    user = request.user
    client_id = request.POST.get('client_id')
    amount = request.POST.get('amount')
    description = request.POST.get('description')

    # Get a client or return 404
    try:
        client = Application.objects.get(client_id=client_id)
    except ObjectDoesNotExist:
        return Response({"message": "Can't find application"}, status=status.HTTP_404_NOT_FOUND)

    # Check the balance of user
    if not user.check_balance(amount):
        return Response({"message": "Hasapda ýeterlik GC tapylmady!"}, status=status.HTTP_400_BAD_REQUEST)

    payment = Payment.objects.create(user=user, client=client, amount=amount, description=description)
    payment.save()

    return Response({"code": payment.verification_code})
