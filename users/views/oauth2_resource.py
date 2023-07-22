from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from users.serializers import ResourceUserSerializer


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
