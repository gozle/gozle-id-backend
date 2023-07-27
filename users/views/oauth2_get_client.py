from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN, CLIENT_ID
from users.models import Application


@swagger_auto_schema(method='get',
                     manual_parameters=[JWT_TOKEN, CLIENT_ID],
                     responses={200: "Name of the client",
                                401: 'Unauthorized',
                                404: "Client not found"}
                     )
@api_view(["GET"])
@csrf_exempt
def get_client(request):
    """
    Get a client by client_id
    """
    try:
        client = Application.objects.get(client_id=request.GET.get('client_id'))
    except ObjectDoesNotExist:
        return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"name": client.name})
