from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import Application, Payment


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def perform_payment(request):
    # Get data from request
    client_id = request.POST.get('client_id')
    client_secret = request.POST.get('client_secret')
    verification_code = request.POST.get('verification_code')

    # Authorize client credentials
    client = Application.authorize(client_id, client_secret)
    if not client:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if payment is valid
    payment = Payment.get_object(client, verification_code)
    if not payment:
        return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

    # Perform payment
    payment.perform_payment()
    return Response({'success': True, "user_id": payment.user.id})
