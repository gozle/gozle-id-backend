from django.urls import path
# from users.user_service import UserService

from users.views import enterCard, forgetPassword, history, sign_up, update, verify_number, get_user, tfa
from users.views import register_order, order_status, get_user_server
from users.views import transfer_request, transfer_verify

urlpatterns = [
    path('sign-up', sign_up),
    path('get-user', get_user),
    path('private/get-user', get_user_server),
    path('update', update),
    path('verify', verify_number),
    path('2fa/<str:action>', tfa),
    path('order/register', register_order),
    path('order/status', order_status),
    path('transfer/request', transfer_request),
    path('transfer/verify', transfer_verify),
    path('forget-password/<str:action>', forgetPassword),
    path('history/<str:action>', history),
    path("enter-card", enterCard),
    #    path('rpc/user_service/', UserService.as_view())
]
