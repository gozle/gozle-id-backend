from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Inherit from `TokenRefreshSerializer` and touch the database
    before re-issuing a new access token and ensure that the user
    exists and is active.
    """

    error_msg = 'No active account found with the given credentials'

    def validate(self, attrs):
        print('GELLOOOOOO')
        token_payload = token_backend.decode(attrs['refresh'])
        try:
            user = get_user_model().objects.get(pk=token_payload['user_id'])
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        if not user.is_active or user.email != token_payload['user_email']:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        return super().validate(attrs)
