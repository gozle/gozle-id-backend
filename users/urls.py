from django.urls import path
#from users.user_service import UserService

from users.views import sign_up, update, LoginView, verify_number, change_password, change_password_verify, get_user, tfa
from users.views import register_order, order_status, get_user_server

urlpatterns = [
    path('sign-up', sign_up),
    path('get-user', get_user),
    path('private/get-user', get_user_server),
    path('login', LoginView.as_view()),
    path('update', update),
    path('verify', verify_number),
    path('change-password', change_password),
    path('change-password-verify', change_password_verify),
    path('2fa/<str:action>', tfa),
    path('order/register', register_order),
    path('order/status', order_status)
#    path('rpc/user_service/', UserService.as_view())
]
