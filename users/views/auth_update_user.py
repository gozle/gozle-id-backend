from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import User
from users.serializers import UserSerializer


@swagger_auto_schema(method='post',
                     manual_parameters=[JWT_TOKEN],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                             'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                             'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
                             'birthday': openapi.Schema(type=openapi.TYPE_STRING, description='Birthday'),
                             'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                             'region': openapi.Schema(type=openapi.TYPE_STRING, description='Region'),
                             'theme': openapi.Schema(type=openapi.TYPE_STRING, description='Theme'),
                             'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender'),
                             'language': openapi.Schema(type=openapi.TYPE_STRING, description='Language'),
                             'avatar': openapi.Schema(type=openapi.TYPE_FILE, description="Avatar"),

                         }
                     ),
                     responses={
                         200: UserSerializer(),
                         409: "Username already exists",
                     })
@api_view(["POST"])
@csrf_exempt
def update(request):
    """
    Update user data

    Permissions:
         - Only authenticated users can update their data

    Parameters (optional):
        - username
        - first_name
        - last_name
        - birthday
        - email
        - reserve_phone_number
        - avatar

    Responses:
         - 200: Updated user data
         - 409: Username already exists
    """
    user = request.user

    # Check if user with this username already exists
    if User.objects.exclude(id=user.id).filter(username=request.data.get('username')).exists():
        return Response({'username': "Already exists"}, status=status.HTTP_409_CONFLICT)

    # TODO: Reserve phone number

    # Update user with new data
    user.update(request)

    # Return updated user
    serializer = UserSerializer(user)
    return Response(serializer.data)
