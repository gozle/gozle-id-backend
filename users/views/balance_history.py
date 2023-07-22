from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import LoginSerializer, HistorySerializer


@api_view(["POST"])
@csrf_exempt
def history(request, action):
    # Select action
    if action == "login":
        # Return all login history of user
        objects = request.user.logins.all()

        serializer = LoginSerializer(objects, many=True)
        return Response(serializer.data)
    elif action == "received":
        # Return all received history of user
        objects = request.user.history.all()

        serializer = HistorySerializer(objects, many=True)
        return Response(serializer.data)
