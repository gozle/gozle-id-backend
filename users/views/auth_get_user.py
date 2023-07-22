from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserSerializer


@api_view(["GET"])
@csrf_exempt
def get_user(request):
    """
    Returns the authenticated user.

    Permissions:
         - Is authenticated.
    Responses:
         - 200: The authenticated user.
         - 401: Unauthorized.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
