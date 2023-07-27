from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.models import Verification, TempToken, Login
from users.views.functions import get_tokens_for_user, check_user_exists


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def verify_number(request):
    """
    Verify phone number

    Permissions:
         - Allow any user to sign up

    Parameters:
         - phone_number: phone number to verify
         - verification-code: verification code

    Responses:
        200: Success
        401: Invalid Code
        404: User Not Found
    """
    # Get data from request
    phone_number = request.POST.get('phone_number')
    code = int(request.POST.get('verification-code'))

    # Check if the phone number is valid and user exists with that phone number
    user = check_user_exists(phone_number)
    if not user:
        return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the verification code is valid
    if not user.verification or user.verification.type != "phone" or user.verification.code != code:
        return Response({'status': False, 'Error': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)

    # Activate user
    user.is_active = True
    user.save()

    # Delete verification code
    Verification.objects.get(code=code).delete()

    # Check if 2FA is enabled
    if user.two_factor_auth == "password":
        # Delete temp token and create new one
        if TempToken.objects.filter(user=user).exists():
            TempToken.objects.filter(user=user).delete()
        token = TempToken(user=user, token=get_random_string(32))
        token.save()

        # Return created 2FA token
        return Response({'2fa': token.token})

    else:
        # Create a login object to store login history
        login_object = Login()
        login_object.user = user
        login_object.ip_address = request.META.get('HTTP_X_REAL_IP')
        login_object.browser = request.user_agent.browser.family
        login_object.os = request.user_agent.os.family + " " + request.user_agent.os.version_string
        login_object.device = request.user_agent.device.family
        login_object.save()

        # Get tokens for user and return them
        tokens = get_tokens_for_user(user)
        return Response(tokens)
