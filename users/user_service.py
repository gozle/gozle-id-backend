from users.models import User
from users.serializers import UserSerializer

from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from modernrpc.core import rpc_method

#@csrf_exempt
@rpc_method(name='users.get')
def get_user(token):
    try:
        token = Token.objects.get(key=token)
    except:
        return {'message': 'Token is invalid'}

    user = token.user

    if not user.is_active:
        return None
    user = User.objects.get(pk=user.id)
    
    return {
        'id': str(user.id),
        'username': user.username
    }
    
