from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import Region
from users.serializers import RegionSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def get_regions(request):
    lang = request.GET.get("lang")

    regions = Region.objects.all()
    serializer = RegionSerializer(regions, many=True, context={"lang": lang})
    return Response(serializer.data)
