import pytz
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.models import TempToken, Login
from users.views.functions import get_tokens_for_user


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def tfa(request, action):
    """
    Two-Factor Authentication view

    action:
         - activate: To activate two-factor authentication
         - deactivate: To deactivate two-factor authentication
         - check: To check if two-factor authentication is activated
         - get-token: To get the token of user by password
    """
    if action == 'activate':
        # Return 403 if user is not authenticated
        if request.user.is_anonymous:
            return Response({'detail': "Authentication credentials were not provided."},
                            status=status.HTTP_403_FORBIDDEN)

        # Get data from request
        user = request.user
        password = request.POST.get('password')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        # Set two-factor authentication activated
        user.two_factor_auth = "password"
        user.question = question
        user.answer = answer
        user.set_password(password)
        user.save()

        return Response({'message': 'Two Factor Authentication activated successfully'})

    elif action == 'deactivate':
        # Return 403 if user is not authenticated
        if request.user.is_anonymous:
            return Response({'detail': "Authentication credentials were not provided."},
                            status=status.HTTP_403_FORBIDDEN)

        # Set two-factor authentication deactivated
        user = request.user
        user.two_factor_auth = "none"
        user.save()

        return Response({'message': 'Two Factor Authentication deactivated successfully'})

    elif action == 'check':
        # Return 403 if user is not authenticated
        if request.user.is_anonymous:
            return Response({'detail': "Authentication credentials were not provided."},
                            status=status.HTTP_403_FORBIDDEN)
        user = request.user
        # Return 2fa of user
        return Response({'2fa': user.two_factor_auth})

    elif action == 'get-token':
        # Get data from request
        token = request.POST.get('token')
        password = request.POST.get('password')

        # Check if 2fa token is correct
        if not TempToken.objects.filter(token=token).exists():
            return Response({'detail': "Token is not correct"}, status=status.HTTP_403_FORBIDDEN)

        user = TempToken.objects.get(token=token).user
        # Check if the password is correct
        auth = authenticate(username=user.username, password=password)
        if auth is not None:
            # Create a Login object if the password is correct
            login_object = Login()
            login_object.user = user
            login_object.ip_address = request.META.get('HTTP_X_REAL_IP')
            login_object.browser = request.user_agent.browser.family
            login_object.os = request.user_agent.os.family + " " + request.user_agent.os.version_string
            login_object.device = request.user_agent.device.family
            login_object.save()

            # Delete token
            TempToken.objects.get(token=token).delete()
            # Get tokens for user and return them
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        else:
            return Response({'message': 'Password is wrong!'}, status=status.HTTP_401_UNAUTHORIZED)
