from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import Application, Payment, User


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_payment(request):
    # Get data from request
    user_id = request.POST.get('user_id')
    client_id = request.POST.get('client_id')
    amount = request.POST.get('amount')
    description = request.POST.get('description')

    # Check the user
    if not User.objects.filter(user_id).exists():
        return Response({"message": "Can't find user"}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(id=user_id)

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

    return Response({"payment_id": payment.id}, status=status.HTTP_201_CREATED)
