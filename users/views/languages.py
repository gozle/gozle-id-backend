from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config.swagger_parameters import JWT_TOKEN
from users.models import Language
from users.serializers import LanguageSerializer


@swagger_auto_schema(method='get',
                     responses={200: "Languages"}
                     )
@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def get_languages(request):
    """
    Function to get languages.
    """
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True)
    return Response(serializer.data)
