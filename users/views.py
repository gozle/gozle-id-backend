from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail

from users.models import Login, Order, Transfer, User, Verification, TempUser, get_valid_phone_number, TempToken
from users.serializers import LoginSerializer, UserSerializer

from .forms import CustomUserCreationForm

from sms import sms_sender

import xml.etree.ElementTree as ET

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import permissions
from rest_framework import views
from rest_framework.authtoken.models import Token

import random
import requests
# Create your views here.


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(request.eaders)
    print(x_forwarded_for)
    print(request.META.get('REMOTE_ADDR'))
    print(request.META.get('HTTP_X_REAL_IP'))
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

################# SIGN-UP ############################


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
        'birthday': openapi.Schema(type=openapi.TYPE_STRING, description='Birthday'),
        'ip_address': openapi.Schema(type=openapi.TYPE_STRING, description='IP Address'),
        'mac_address': openapi.Schema(type=openapi.TYPE_STRING, description='Mac Address'),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone Number'),
        'device_info': openapi.Schema(type=openapi.TYPE_STRING, description='Device Info'),
        'password1': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        'password2': openapi.Schema(type=openapi.TYPE_STRING, description='Password 2'),
        'avatar': openapi.Schema(type=openapi.TYPE_FILE, description='Avatar'),
    }
))
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def sign_up(request):
    #    form = CustomUserCreationForm(request.POST, request.FILES or None)
    #    if not form.is_valid():
    phone_number = get_valid_phone_number(request.POST.get('phone_number'))

    if phone_number != '':
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
#            return Response({'message': 'User with this phone number already exists'}, status=status.HTTP_403_FORBIDDEN)
        else:
            user = User()
            random_username = random.randint(10000000, 1000000000)
            user.username = str(random_username)
            user.is_active = False
            user.phone_number = phone_number
            user.save()

        phone_number = user.phone_number
        verification_number = random.randint(1000, 9999)
        if Verification.objects.filter(user=user, type="phone").exists():
            if Verification.objects.get(user=user, type='phone').created_at > timezone.now() - timezone.timedelta(minutes=1):
                return Response({"message": "Verification code is sent. Please wait 1 minutes before try again!"}, status=status.HTTP_403_FORBIDDEN)
            Verification.objects.filter(user=user, type='phone').delete()
        Verification.objects.filter(user=user).delete()
        verification = Verification(code=verification_number, user=user).save()

        sms_sender.send(phone_number, 'Gozle ID code: ' +
                        str(verification_number))

        user.verification_number = verification_number
        user.save()

        if not Token.objects.filter(user=user).exists():
            Token.objects.create(user=user)

        return Response({'message': 'OK', 'status': 200})
    else:
        return Response({"message": "Phone Number can't be blank"}, status=status.HTTP_403_FORBIDDEN)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'verification-code': openapi.Schema(type=openapi.TYPE_STRING, description='Verification Code'),
    }
))
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def verify_number(request):
    username = request.POST.get('phone_number')
    code = int(request.POST.get('verification-code'))
    if User.objects.filter(phone_number=get_valid_phone_number(username)).exists():
        user = User.objects.get(phone_number=get_valid_phone_number(username))
    else:
        return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if user.verification and user.verification.type == "phone" and user.verification.code == code:
        user.is_active = True
        user.save()
        Verification.objects.get(code=code).delete()
        if not user.two_factor_auth == "password":

            login = Login()
            login.user = user
            login.ip_address = get_client_ip(request)
            login.browser = request.user_agent.browser.family
            login.os = request.user_agent.os.family + \
                " " + request.user_agent.os.version_string
            login.device = request.user_agent.device.family
            login.save()

            return Response({'token': user.auth_token.key})
        else:
            if TempToken.objects.filter(user=user).exists():
                TempToken.objects.filter(user=user).delete()
            token = TempToken(user=user, token=get_random_string(32))
            token.save()
            return Response({'2fa': token.token})
    return Response({'status': False, 'Error': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def forgetPassword(request, action):
    if action == "email":
        phone_number = request.POST.get('phone_number')
        if User.objects.filter(phone_number=get_valid_phone_number(phone_number)).exists():
            user = User.objects.get(
                phone_number=get_valid_phone_number(phone_number))
        else:
            return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.email:
            return Response({"message": "User's email not found"}, status=status.HTTP_403_FORBIDDEN)

        verification_number = random.randint(1000, 9999)

        if Verification.objects.filter(user=user, type="email").exists():
            if Verification.objects.get(user=user, type="email").created_at > timezone.now() - timezone.timedelta(minutes=1):
                return Response({"message": "Verification code is sent. Please wait 1 minutes before try again!"}, status=status.HTTP_403_FORBIDDEN)
            Verification.objects.filter(user=user, type="email").delete()

        verification = Verification(
            code=verification_number, user=user, type="email").save()
        send_mail(
            "Password Reset, Gozle",
            "Password Reset Code: "+str(verification_number),
            "reset@gozle.com.tm",
            [user.email],
            fail_silently=False,
        )

        return Response({"Verification code sent to email"})
    elif action == "change":
        phone_number = request.POST.get('phone_number')
        code = int(request.POST.get('verification-code'))
        if User.objects.filter(phone_number=get_valid_phone_number(phone_number)).exists():
            user = User.objects.get(
                phone_number=get_valid_phone_number(phone_number))
        else:
            return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if user.verification and user.verification.type == "email" and user.verification.code == code:
            password = request.POST.get("password")
            user.set_password(password)
            user.save()
            return Response({"message": 'Password set successfully'})

        return Response({'status': False, 'Error': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    }
))
@api_view(["POST"])
@csrf_exempt
def update(request):
    if not request.user:
        return Response({'message': "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    user = User.objects.get(pk=request.user.id)
    if User.objects.filter(username=request.POST.get('username')).exists():
        return Response({'username': "Already exists"}, status=status.HTTP_409_CONFLICT)

    user.username = request.POST.get('username') if request.POST.get(
        'username') else user.username
    user.first_name = request.POST.get('first_name') if request.POST.get(
        'first_name') else user.first_name
    user.last_name = request.POST.get('last_name') if request.POST.get(
        'last_name') else user.last_name
    user.birthday = request.POST.get('birthday') if request.POST.get(
        'birthday') else user.birthday
    user.email = request.POST.get(
        'email') if request.POST.get('email') else user.email
    user.avatar = request.FILES.get(
        'avatar') if request.FILES.get('avatar') else user.avatar

    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["GET"])
@csrf_exempt
def get_user(request):
    if not request.user:
        return Response({'message': "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def get_user_server(request):
    user_id = request.POST.get('user_id')

    token = request.META.get('HTTP_AUTHORIZATION')
    if not token or token != settings.SERVER_TOKEN:
        return Response({'message': "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def tfa(request, action):
    """
    This view function updates the password and two factor auth status of a user
    based on the user id and password data from the POST request.
    It returns a JSON response with a success or error message.
    """

    if action == 'activate':
        # get the user and get the password from the request data
        if request.user.is_anonymous:
            return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        password = request.POST.get('password')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        user.two_factor_auth = "password"
        user.question = question
        user.answer = answer

        user.set_password(password)

        user.save()
        return Response({'message': 'Two Factor Authentication activated sucessfully'})

    elif action == 'deactivate':
        if request.user.is_anonymous:
            return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        user.two_factor_auth = "none"
        user.save()
        return Response({'message': 'Two Factor Authentication deactivated sucessfully'})

    elif action == 'check':
        #        print(request.user)
        if request.user.is_anonymous:
            return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        return Response({'2fa': user.two_factor_auth})

    elif action == 'get-token':
        token = request.POST.get('token')
        password = request.POST.get('password')

        if TempToken.objects.filter(token=token).exists():
            user = TempToken.objects.get(token=token).user
            auth = authenticate(username=user.username, password=password)
            if auth is not None:

                login = Login()
                login.user = user
                login.ip_address = request.META.get('HTTP_X_REAL_IP')
                login.browser = request.user_agent.browser.family
                login.os = request.user_agent.os.family + \
                    " " + request.user_agent.os.version_string
                login.device = request.user_agent.device.family
                login.save()

                response = {"token": user.auth_token.key}
                TempToken.objects.get(token=token).delete()
                return Response(response)
            else:
                return Response({'message': 'Password is wrong!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': "Token is noe correct"}, status=status.HTTP_403_FORBIDDEN)
    return Response({'success': 'User password and two factor auth updated'})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def register_order(request):
    if request.user.is_anonymous:
        return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    description = request.POST.get('description')
    amount = request.POST.get('amount')
    returnUrl = request.POST.get('returnUrl')
    failUrl = request.POST.get('failUrl')
    lang = request.POST.get('language')
    pageView = request.POST.get('pageView')

    order = Order(user=request.user, description=description, amount=amount)
    order.save()

    request_url = ""

    data = {
        'userName': settings.MERCHANT_USERNAME,
        'password': settings.MERCHANT_PASSWORD,
        'orderNumber': order.id,
        'amount': order.amount,
        'currency': order.currency,
        'returnUrl': returnUrl,
        'failUrl': failUrl,
        'description': description,
        'language': lang,
        'pageView': pageView
    }

    response = requests.post(request_url, data=data)

    response_data = response.json()
    order.order_id = response_data['orderId']
    return Response(response_data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def order_status(request):
    if request.user.is_anonymous:
        return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    orderId = request.POST.get('orderId')

    request_url = ""

    data = {
        'userName': settings.MERCHANT_USERNAME,
        'password': settings.MERCHANT_PASSWORD,
        'orderId': orderId
    }

    response = requests.post(request_url, data=data)

    response_data = response.json()

    return Response(response_data)


@api_view(["POST"])
@csrf_exempt
def transfer_request(request):
    if request.user.is_anonymous:
        return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    user = request.user
    send_to = request.POST.get('send_to')
    amount = int(request.POST.get('amount'))

    receiver = User.objects.filter(phone_number=send_to).first()
    if receiver is None:
        return Response({'message': 'Receiver not found'})

    if amount > user.balance:
        return Response({'message': "User's balance is smaller than amount"})

    verification_number = random.randint(10000, 99999)
    transfer = Transfer.objects.create(sender=user, receiver=receiver, amount=amount,
                                       completed=False, verification_code=verification_number)
    transfer.save()

    # Send SMS to sender
    sms_sender.send(user.phone_number, 'Transferring {} GC to {}. Verification code: {}'.format(
        amount, receiver.phone_number, verification_number))
    transfer.verification_code = verification_number
    transfer.save()
    # Save verification number

    return Response({'message': 'Waiting for varification...'})


@api_view(["POST"])
@csrf_exempt
def transfer_verify(request):
    if request.user.is_anonymous:
        return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    user = request.user
    verification_number = request.POST.get('verification-code')

    transfer = Transfer.objects.filter(
        sender=user, verification_code=verification_number, completed=False).first()
    if transfer is None:
        return Response({'message': 'Transfer request is not sent'})

    user.balance -= transfer.amount
    user.save()
    receiver = transfer.receiver
    receiver.balance += transfer.amount
    receiver.save()

    transfer.completed = True
    transfer.save()

    # Send SMS to sender
    # Save verification number

    return Response({'message': 'Transferred successfully'})


@api_view(["GET"])
@csrf_exempt
def logins(request):
    if request.user.is_anonymous:
        return Response({'detail': "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    objects = request.user.logins.all()

    serializer = LoginSerializer(objects, many=True)
    return Response(serializer.data)
