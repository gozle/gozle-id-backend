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

    # Update user with new data
    user.username = request.POST.get('username') if request.POST.get(
        'username') else user.username
    user.first_name = request.POST.get('first_name') if request.POST.get(
        'first_name') else user.first_name
    user.last_name = request.POST.get('last_name') if request.POST.get(
        'last_name') else user.last_name
    user.birthday = request.POST.get('birthday') if request.POST.get(
        'birthday') else user.birthday
    user.email = request.POST.get(
        'email') if request.POST.get('email') else user.email
    user.reserve_phone_number = request.POST.get("reserve_phone_number") if request.POST.get(
        "reserve_phone_number") else user.reserve_phone_number
    user.avatar = request.FILES.get(
        'avatar') if request.FILES.get('avatar') else user.avatar
    user.save()

    # Return updated user
    serializer = UserSerializer(user)
    return Response(serializer.data)
