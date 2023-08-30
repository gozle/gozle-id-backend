import random

from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import ReservePhoneNumber, User
from users.models.functions import get_valid_phone_number


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'phone_number': openapi.Schema(type=openapi.TYPE_STRING,
                                                            description='The Reserve Phone Number'),
                         }
                     ),
                     responses={
                         200: "Successfully sent verification code",
                         409: "Phone number already registered",
                     })
@api_view(["POST"])
@csrf_exempt
def register_reserve_number(request):
    # Get the data from the request
    phone_number = get_valid_phone_number(request.data.get("phone_number"))

    # Check if the phone number is already registered
    if User.objects.filter(phone_number=phone_number).exists() or ReservePhoneNumber.objects.filter(
                                                                    phone_number=phone_number, is_active=True):
        return Response({"message": "Phone number already registered"}, status=status.HTTP_409_CONFLICT)

    # Create a new reserve phone number
    user = request.user

    if ReservePhoneNumber.objects.filter(user=user, is_active=False):
        ReservePhoneNumber.objects.filter(user=user, is_active=False).delete()
    elif ReservePhoneNumber.objects.filter(user=user, is_active=True):
        return Response({"This user already has reserve phone number. Deactivate it first"},
                        status=status.HTTP_400_BAD_REQUEST)

    verification_number = random.randint(1000, 9999)
    reserve_phone_number = ReservePhoneNumber.objects.create(user=user,
                                                             phone_number=phone_number,
                                                             verification_code=verification_number)

    # Send the verification code to the phone number
    reserve_phone_number.send_verification_code()

    return Response({"message": "Verification code sent"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'verification-code': openapi.Schema(type=openapi.TYPE_STRING,
                                                                 description='Verification code which sent to phone '
                                                                             'number'),
                         }
                     ),
                     responses={200: 'Activated Successfully',
                                400: 'Invalid Verification Code'}
                     )
@api_view(["POST"])
@csrf_exempt
def activate_reserve_number(request):
    # Get the data from the request
    verification_code = request.data.get("verification-code")
    user = request.user

    # Check if the verification code is valid
    if not ReservePhoneNumber.objects.filter(user=user, verification_code=verification_code).exists():
        return Response({"message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

    # Activate the reserve phone number
    ReservePhoneNumber.objects.get(user=user, verification_code=verification_code).activate()

    return Response({"message": "Activated successfully"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     responses={200: 'Deactivated Successfully',
                                401: 'Invalid Credentials'}
                     )
@api_view(["POST"])
@csrf_exempt
def deactivate_reserve_number(request):
    user = request.user
    if ReservePhoneNumber.objects.filter(user=user).exists():
        ReservePhoneNumber.objects.get(user=user).delete()

    return Response({"message": "Deactivated successfully"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get',
                     manual_parameters=[JWT_TOKEN],
                     responses={200: 'Reserve Phone Number',
                                404: 'Reserve phone number not found'}
                     )
@api_view(["GET"])
@csrf_exempt
def get_reserve_number(request):
    user = request.user
    if not ReservePhoneNumber.objects.filter(user=user).exists():
        return Response({"message": "Reserve phone number not found"}, status=status.HTTP_404_NOT_FOUND)

    reserve_phone_number = ReservePhoneNumber.objects.get(user=user)
    return Response({"reserve_phone_number": reserve_phone_number.phone_number,
                     "activated_at": reserve_phone_number.activated_at})
