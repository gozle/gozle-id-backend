from rest_framework_simplejwt.views import TokenRefreshView
from ..serializers import CustomTokenRefreshSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh token generator view.
    """
    serializer_class = CustomTokenRefreshSerializer
