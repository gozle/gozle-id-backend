from django.urls import path
from users.new.views import signup, verify_number

urlpatterns = [
    path('auth/sign-up', signup),
    path('auth/verify-number', verify_number),
]