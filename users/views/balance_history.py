from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.serializers import LoginSerializer, HistorySerializer, OrderSerializer


@swagger_auto_schema(method='get',
                     manual_parameters=[JWT_TOKEN],
                     responses={200: LoginSerializer(),
                                401: 'Unauthorized'}
                     )
@api_view(["GET"])
@csrf_exempt
def history(request, action):
    # Select action
    if action == "login":
        # Return all login history of user
        objects = request.user.logins.all().order_by("-pk")

        serializer = LoginSerializer(objects, many=True)
        return Response(serializer.data)
    elif action == "balance":
        # Return all received history of user
        objects = request.user.orders.all()

        serializer = OrderSerializer(objects, many=True)
        return Response(serializer.data)
