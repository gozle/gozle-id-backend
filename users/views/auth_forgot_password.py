import random

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from config.swagger_parameters import PHONE_NUMBER, VERIFICATION_CODE
from users.models import Verification
from users.views.functions import check_user_exists, verify_and_delete


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@swagger_auto_schema(method='post', manual_parameters=[PHONE_NUMBER])
@csrf_exempt
def forgot_password_email(request):
    """
    Send a verification code to the user's email if forgot password

    Permissions:
        - Allow any user to sign up

    :param str phone_number: The user's phone number

    Responses:
        - 200: Success
        - 404: User Not Found
        - 403: Verification code already sent to user's email or email not found
    """
    # Get the user's phone number
    phone_number = request.POST.get('phone_number')

    # Check if the user exists
    user = check_user_exists(phone_number)
    if not user:
        return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has an email
    if not user.email:
        return Response({"message": "User's email not found"}, status=status.HTTP_403_FORBIDDEN)

    # Generate a verification code
    verification_number = random.randint(1000, 9999)

    # Check if the verification code already exists and delete it
    clean_verification = verify_and_delete(user=user, type="email")
    if not clean_verification:
        return Response({"message": "Verification code is sent. Please wait 1 minutes before try again!"},
                        status=status.HTTP_403_FORBIDDEN)

    # Save the verification code
    verification = Verification(
        code=verification_number, user=user, type="email").save()

    # Send the verification code to user's email
    send_mail(
        "Password Reset, Gozle",
        "Password Reset Code: " + str(verification_number),
        "reset@gozle.com.tm",
        [user.email],
        fail_silently=False,
    )

    return Response({"message": "Verification code sent to email"})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@swagger_auto_schema(method='post', manual_parameters=[PHONE_NUMBER, VERIFICATION_CODE])
@csrf_exempt
def forgot_password_change(request):
    """
    Change the user's password with verification code

    Permissions:
        - Allow any user to sign up

    Parameters:
        - phone_number (str): The user's phone number
        - verification-code (int): The user's verification code

    Responses:
        - 200: Success
        - 404: User Not Found
        - 401: Verification code incorrect
    """
    # Get data from request
    phone_number = request.POST.get('phone_number')
    code = int(request.POST.get('verification-code'))

    # Check if the user exists
    user = check_user_exists(phone_number)
    if not user:
        return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if verification code correct
    if user.verification and user.verification.type == "email" and user.verification.code == code:
        # Get and set the new password
        password = request.POST.get("password")
        user.set_password(password)
        user.save()

        return Response({"message": 'Password set successfully'})

    return Response({'status': False, 'Error': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)
