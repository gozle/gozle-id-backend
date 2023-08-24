from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.models import Region
from users.serializers import CitySerializer


@swagger_auto_schema(method='get',
                     manual_parameters=[
                         openapi.Parameter("region", openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                                           description="Id of Region object"),
                     ],
                     responses={200: "Cities"}
                     )
@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def get_cities(request):
    # Get data
    region_id = request.GET.get("region")
    lang = request.GET.get("lang")

    try:
        region = Region.objects.get(id=region_id)
    except:
        return Response({"message": "Region not found"}, status=status.HTTP_404_NOT_FOUND)
    cities = region.cities.all()
    serializer = CitySerializer(cities, many=True, context={"lang": lang})
    return Response(serializer.data)
