from django.urls import path
# from users.user_service import UserService

from users.views import enterCard, forgetPassword, history, sign_up, update, verify_number, get_user, tfa, resource, \
    get_client, oauth_login
from users.views import register_order, order_status, get_user_server
from users.views import transfer_request, transfer_verify


urlpatterns = [
    path('auth/sign-up', sign_up),
    path('auth/get-user', get_user),
    # path('private/get-user', get_user_server),
    path('auth/update', update),
    path('auth/verify', verify_number),
    path('2fa/<str:action>', tfa),
    path('order/register', register_order),
    path('order/status', order_status),
    path('transfer/request', transfer_request),
    path('transfer/verify', transfer_verify),
    path('auth/forget-password/<str:action>', forgetPassword),
    path('history/<str:action>', history),
    path("enter-card", enterCard),
    path('resource', resource),
    path('get/client/', get_client),
    path('login/', oauth_login),
    #    path('rpc/user_service/', UserService.as_view())
]
