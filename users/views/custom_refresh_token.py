from rest_framework_simplejwt.views import TokenRefreshView
from users.serializers import CustomTokenRefreshSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh token generator view.
    """
    serializer_class = CustomTokenRefreshSerializer
