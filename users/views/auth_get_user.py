from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.serializers import UserSerializer


@swagger_auto_schema(method='get',
                     manual_parameters=[JWT_TOKEN],
                     responses={200: UserSerializer(),
                                401: 'Unauthorized'}
                     )
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
