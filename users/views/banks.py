from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import Bank
from users.serializers import BankSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def get_banks(request):
    banks = Bank.objects.all()

    serializer = BankSerializer(banks, many=True, context={"request": request})
    return Response(serializer.data)
