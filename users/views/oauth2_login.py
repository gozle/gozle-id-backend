from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from users.views.functions import get_url_from_dict


@api_view(["GET"])
@csrf_exempt
def oauth_login(request):
    """
    This function is used to log in the user with JWT Token and redirect to the oauth provider. Because oauth
    provider is using LoginRequiredMixin class of django. And That class is not accepting JWT Token, this function is
    used to log in the user to make accessible with session authentication in oauth provider.
    """
    user = request.user

    # Collect GET parameters
    get_parameters = {}
    for key, value in request.GET.items():
        get_parameters[key] = value

    # Login user and redirect to the oauth provider
    login(request, user)
    return redirect(get_url_from_dict(get_parameters))
