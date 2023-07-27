from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from config.swagger_parameters import OAUTH_TOKEN
from users.serializers import ResourceUserSerializer


@swagger_auto_schema(method='get',
                     manual_parameters=[OAUTH_TOKEN],
                     responses={200: ResourceUserSerializer()}
                     )
@api_view(["GET"])
@authentication_classes([OAuth2Authentication])
@csrf_exempt
def resource(request):
    """
    Returns the authenticated user's resource.
    """
    user = request.user
    serializer = ResourceUserSerializer(user)
    return Response(serializer.data)
