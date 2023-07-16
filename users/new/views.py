import random

import pytz
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone

from sms import sms_sender
from users.models import User, get_valid_phone_number, Verification, Login, TempToken
from rest_framework.response import Response
from django.contrib.auth import authenticate, login


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def signup(request):
    phone_number = get_valid_phone_number(request.POST.get('phone_number'))

    if phone_number != '':
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
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
            if Verification.objects.get(user=user, type='phone').created_at > timezone.now() - timezone.timedelta(
                    minutes=1):
                return Response({"message": "Verification code is sent. Please wait 1 minutes before try again!"},
                                status=status.HTTP_403_FORBIDDEN)
            Verification.objects.filter(user=user, type='phone').delete()
        Verification.objects.filter(user=user).delete()
        verification = Verification(code=verification_number, user=user).save()

        sms_sender.send(phone_number, 'Gozle ID code: ' +
                        str(verification_number))

        user.verification_number = verification_number
        user.save()

        # if not Token.objects.filter(user=user).exists():
        #     Token.objects.create(user=user)

        return Response({'message': 'OK', 'status': 200})
    else:
        return Response({"message": "Phone Number can't be blank"}, status=status.HTTP_403_FORBIDDEN)


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
            loginModel = Login()
            loginModel.user = user
            loginModel.ip_address = request.META.get('HTTP_X_REAL_IP')
            loginModel.browser = request.user_agent.browser.family
            loginModel.os = request.user_agent.os.family + \
                            " " + request.user_agent.os.version_string
            loginModel.device = request.user_agent.device.family
            loginModel.save()

            date = loginModel.created_at.astimezone(
                pytz.timezone("Asia/Ashgabat")).date()
            time = loginModel.created_at.astimezone(
                pytz.timezone("Asia/Ashgabat")).time()

            sms_sender.send(user.phone_number, """
{}/{}/{} sagat {}:{}-da "Gozle ID" hasabyňyza girildi.

Enjam: {}
IP: {}

Eger siz däl bolsaňyz, Gozle ID hasabyňyza giriň we parolyňyzy üýtgediň
                            """.format(date.day, date.month, date.year, time.hour, time.minute, loginModel.os,
                                       loginModel.ip_address))
            login(request, user)
            return Response({"message": 'Login Successfull'})
        else:
            if TempToken.objects.filter(user=user).exists():
                TempToken.objects.filter(user=user).delete()
            token = TempToken(user=user, token=get_random_string(32))
            token.save()
            return Response({'2fa': token.token})
    return Response({'status': False, 'Error': 'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)
