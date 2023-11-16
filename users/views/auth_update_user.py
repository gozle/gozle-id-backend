from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import User, City, Language, Region
from users.models.validators import validate_names
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
                             'region': openapi.Schema(type=openapi.TYPE_STRING, description='Id of Region object'),
                             'city': openapi.Schema(type=openapi.TYPE_STRING, description='Id of City object'),
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
    if User.objects.exclude(id=user.id).filter(username=request.POST.get('username')).exists():
        return Response({'username': "Already exists"}, status=status.HTTP_409_CONFLICT)

    # TODO: Reserve phone number

    # Update user with new data
    user.username = request.data.get('username', user.username)
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.birthday = request.data.get('birthday', user.birthday)

    # validate user first_name and last_name
    err_resp = {}
    try:
        validate_names(user.first_name)
    except ValidationError as err:
        err_resp['first_name'] = str(err)
    try:
        validate_names(user.last_name)
    except ValidationError as err:
        err_resp['last_name'] = str(err)
    if err_resp:
        return Response(err_resp, status=status.HTTP_400_BAD_REQUEST)

    # check if email is given and send email verification
    if request.data.get("email"):
        user.email = request.data.get('email')
        user.save()
        user.add_email()

    if request.data.get("region"):
        try:
            region = Region.objects.get(id=request.data.get("region"))
            user.region = region
        except ObjectDoesNotExist:
            pass
    if request.data.get("city"):
        try:
            city = City.objects.get(id=request.data.get("city"))
            user.city = city
        except ObjectDoesNotExist:
            pass
    user.theme = request.data.get("theme", user.theme)
    user.gender = request.data.get("gender", user.gender)
    if request.data.get("language"):
        try:
            language = Language.objects.get(id=request.data.get("language"))
            user.language = language
        except ObjectDoesNotExist:
            pass
    user.avatar = request.FILES.get('avatar', user.avatar)

    user.save()

    # Return updated user
    serializer = UserSerializer(user)
    return Response(serializer.data)
