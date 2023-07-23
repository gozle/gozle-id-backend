from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Payment, Application
from users.serializers import PaymentSerializer


@api_view(['GET'])
@csrf_exempt
def get_payment(request):
    """
    Get payment details by id
    """
    # Get data from request
    payment_id = request.query_params.get('payment_id', '')
    client_id = request.query_params.get('client_id', '')

    # Check payment id
    if not Payment.objects.filter(id=payment_id).exists():
        return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check a client id
    if not Application.objects.filter(client_id=client_id).exists():
        return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get payment
    payment = Payment.objects.get(id=payment_id)

    # Return payment
    return Response(PaymentSerializer(payment).data)
