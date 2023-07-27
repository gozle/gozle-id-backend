import random

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import ReservePhoneNumber, User


@api_view(["POST"])
@csrf_exempt
def register_reserve_number(request):
    # Get the data from the request
    phone_number = request.POST.get("phone_number")

    # Check if the phone number is already registered
    if User.objects.filter(phone_number=phone_number).exists():
        return Response({"message": "Phone number already registered"}, status=status.HTTP_409_CONFLICT)

    # Create a new reserve phone number
    user = request.user
    verification_number = random.randint(1000, 9999)
    reserve_phone_number = ReservePhoneNumber.objects.create(user=user,
                                                             phone_number=phone_number,
                                                             verification_code=verification_number)

    # Send the verification code to the phone number
    reserve_phone_number.send_verification_code()

    return Response({"message": "Verification code sent"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def activate_reserve_number(request):
    # Get the data from the request
    verification_code = request.GET.get("verification-code")
    user = request.user

    # Check if the verification code is valid
    if not ReservePhoneNumber.objects.filter(user=user, verification_code=verification_code).exists():
        return Response({"message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

    # Activate the reserve phone number
    ReservePhoneNumber.objects.get(user=user, verification_code=verification_code).activate()

    return Response({"message": "Activated successfully"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def deactivate_reserve_number(request):
    user = request.user
    ReservePhoneNumber.objects.filter(user=user).delete()

    return Response({"message": "Deactivated successfully"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def get_reserve_number(request):
    user = request.user
    if not ReservePhoneNumber.objects.filter(user=user).exists():
        return Response({"message": "Reserve phone number not found"}, status=status.HTTP_404_NOT_FOUND)

    reserve_phone_number = ReservePhoneNumber.objects.get(user=user)
    return Response({"reserve_phone_number": reserve_phone_number.phone_number,
                     "activated_at": reserve_phone_number.activated_at})
