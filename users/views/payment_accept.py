from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN, PAYMENT_ID
from users.models import Payment


@swagger_auto_schema(method='get',
                     manual_parameters=[JWT_TOKEN, PAYMENT_ID],
                     responses={200: "Verification code of payment"}
                     )
@api_view(['GET'])
@csrf_exempt
def accept_payment(request):
    # Get data from request
    payment_id = request.GET.get('payment_id')

    # Check payment
    if not Payment.objects.filter(id=payment_id, user=request.user).exists():
        return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

    payment = Payment.objects.get(id=payment_id, user=request.user)
    payment.accepted = True
    payment.save()

    return Response({"code": payment.verification_code}, status=status.HTTP_200_OK)
