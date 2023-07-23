from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import OneTimeToken


@api_view(['GET'])
@csrf_exempt
def get_token(request):
    user = request.user
    ott = OneTimeToken.create_for_user(user)
    return Response({'token': ott.token})
