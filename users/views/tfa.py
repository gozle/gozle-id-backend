import pytz
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import TempToken, Login
from users.views.functions import get_tokens_for_user


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'password': openapi.Schema(type=openapi.TYPE_STRING,
                                                        description='The New password'),
                             'question': openapi.Schema(type=openapi.TYPE_STRING,
                                                        description='The question key'),
                             'answer': openapi.Schema(type=openapi.TYPE_STRING,
                                                      description='The answer key'),
                         }
                     ),
                     responses={200: 'Activated Successfully',
                                400: 'Invalid Verification Code'}
                     )
@api_view(["POST"])
@csrf_exempt
def activate_tfa(request):
    # Get data from request
    user = request.user
    password = request.data.get('password')
    question = request.data.get('question')
    answer = request.data.get('answer')

    # Set two-factor authentication activated
    user.two_factor_auth = "password"
    user.question = question
    user.answer = answer
    user.set_password(password)
    user.save()

    return Response({'message': 'Two Factor Authentication activated successfully'})


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     responses={200: 'Two Factor Authentication deactivated successfully',
                                401: 'Unauthorized'}
                     )
@api_view(["POST"])
@csrf_exempt
def deactivate_tfa(request):
    # Set two-factor authentication deactivated
    user = request.user
    password = request.data.get('password')

    authenticated = authenticate(username=user.username, password=password)

    if authenticated is not None:
        user.two_factor_auth = "none"
        user.save()

        return Response({'message': 'Two Factor Authentication deactivated successfully'})
    return Response({'message': 'Password is wrong!'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     responses={200: '2fa Boolean',
                                401: 'Unauthorized'}
                     )
@api_view(["POST"])
@csrf_exempt
def check_tfa(request):
    user = request.user
    # Return 2fa of user
    return Response({'2fa': user.two_factor_auth})


@swagger_auto_schema(method='post',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'password': openapi.Schema(type=openapi.TYPE_STRING,
                                                        description='The password'),
                             'token': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description='2fa token'),
                         }
                     ),
                     responses={200: 'Activated Successfully',
                                400: 'Invalid Verification Code'}
                     )
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def get_token_tfa(request):
    # Get data from request
    token = request.data.get('token')
    password = request.data.get('password')

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
