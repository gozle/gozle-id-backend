from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import City
from users.serializers import CitySerializer

@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def get_cities(request):
    regions = City.objects.all()
    serializer = CitySerializer(regions, many=True)
    return Response(serializer.data)
