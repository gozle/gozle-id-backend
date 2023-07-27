from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import OneTimeToken


@swagger_auto_schema(method='get',
                     manual_parameters=[JWT_TOKEN],
                     responses={200: "One Time Token"}
                     )
@api_view(['GET'])
@csrf_exempt
def get_token(request):
    user = request.user
    ott = OneTimeToken.create_for_user(user)
    return Response({'token': ott.token})
