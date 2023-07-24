from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Application


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
