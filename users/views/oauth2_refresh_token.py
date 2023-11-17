from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User


@api_view(['POST'])
@csrf_exempt
def refresh_token(request):
    try:
         user_id = RefreshToken.objects.get(request.POST.get('refresh')).user
         print('USER ID', user_id)
    except:
        return Response({'error': 'refresh token not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user = User.objects.get(pk=user_id)
        print('USER', user)
    except User.DoesNotExist:
        print('USER NOT FOUND HAHAHAHAH')
        return Response({'error': 'invalid refresh token'}, status=status.HTTP_404_NOT_FOUND)

    return redirect('refresh-token')
