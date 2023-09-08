from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Verification


@api_view(["POST"])
@csrf_exempt
def verify_email(request):
    user = request.user
    verification_code = request.data.get("verification-code")

    if not Verification.objects.filter(code=verification_code, user=user, type="email").exists():
        return Response({"message": "Verification code is wrong or hasn't requested verify email"},
                        status=status.HTTP_400_BAD_REQUEST)

    user.email_verified = True
    Verification.objects.filter(code=verification_code, user=user, type="email").delete()

    return Response({"message": "Email verified"})
