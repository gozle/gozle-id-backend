from django.urls import path

from users.views import *

urlpatterns = [
    path('auth/sign-up', sign_up),
    path('auth/get-user', get_user),
    path('auth/forget-password/change', forgot_password_change),
    path('auth/forget-password/email', forgot_password_email),
    # path('private/get-user', get_user_server),
    path('auth/update', update),
    path('auth/verify', verify_number),

    path('2fa/activate', activate_tfa),
    path('2fa/deactivate', deactivate_tfa),
    path('2fa/check', check_tfa),
    path('2fa/get-token', get_token_tfa),

    path('order/register', register_order),
    path('order/status', order_status),

    path('transfer/request', transfer_request),
    path('transfer/verify', transfer_verify),

    path("email/verify", verify_email),

    path('history/<str:action>', history),
    path("enter-card", enterCard),

    path('resource', resource),
    path('get/client/', get_client),
    path('login/', oauth_login),
    path('logout/', oauth_logout),
    path('get-oauth-token', get_token),

    path('payment/register', register_payment),
    path('payment/perform', perform_payment),
    path('payment/get', get_payment),
    path('payment/accept', accept_payment),

    path('reserve-number/register', register_reserve_number),
    path('reserve-number/activate', activate_reserve_number),
    path('reserve-number/deactivate', deactivate_reserve_number),
    path('reserve-number/get', get_reserve_number),

    path("languages", get_languages),
    path('regions', get_regions),
    path('cities', get_cities),
    path('banks', get_banks),
]
