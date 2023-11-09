import random

from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from sms import sms_sender
from users.models import User, Verification
from users.views.functions import check_user_exists, verify_and_delete
from users.models.functions import get_valid_phone_number


@swagger_auto_schema(method='post',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                         }
                     ),
                     responses={
                         200: "Successfully sent verification code",
                         403: "Invalid phone number or Verification code is sent already"
                     })
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def sign_up(request):
    """
    View to sign up a new user.

    Permissions:
        - Allow any user to sign up

    Parameters:
        - phone_number: phone number of the user

    Responses:
        200: Successfully sent verification code
        403: Invalid phone number
        403: Verification code is sent
    """
    phone_number = get_valid_phone_number(request.data.get('phone_number'))

    # Check if the phone number is valid
    if phone_number == '':
        return Response({"message": "Phone Number can't be blank"}, status=status.HTTP_403_FORBIDDEN)

    # Exception for guys at Google
    if phone_number == '+99312345678':
        return Response({'message': 'OK', 'status': 200})

    # Get existing user or create new
    user = check_user_exists(phone_number)
    if not user:
        user = User()
        random_username = random.randint(10000000, 1000000000)
        user.username = str(random_username)
        user.is_active = False
        user.phone_number = phone_number
        user.save()

    # Get phone number and create verification code
    phone_number = user.phone_number
    verification_number = random.randint(1000, 9999)

    # Delete old verification code
    clean_verification = verify_and_delete(user=user, type="phone")
    if not clean_verification:
        return Response({"message": "Verification code is sent. Please wait 1 minutes before try again!"},
                        status=status.HTTP_403_FORBIDDEN)

    Verification(code=verification_number, user=user, type="phone").save()

    # Send verification code to user
    sms_sender.send(phone_number, 'Gozle ID code: ' + str(verification_number))

    # Save user with new verification code
    user.verification_number = verification_number
    user.save()

    # Return success response
    return Response({'message': 'OK', 'status': 200})
