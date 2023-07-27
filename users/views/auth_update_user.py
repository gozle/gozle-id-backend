from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


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
    user.update_user(request)

    # Return updated user
    serializer = UserSerializer(user)
    return Response(serializer.data)
