"""GozleUsers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
import oauth2_provider.views as oauth2_views

schema_view = get_schema_view(
    openapi.Info(
        title="Users",
        default_version='v1',
        description="User API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
                  # Add media urls here
                  re_path(r'^api/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

                  # OAuth 2.0 urls here
                  path('o/authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
                  path('o/token/', oauth2_views.TokenView.as_view(), name="token"),
                  path('o/revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),

                  # OAuth 2.0 admin urls here
                  path('o/admin/applications/', oauth2_views.ApplicationList.as_view(), name="list"),
                  path('o/admin/applications/register/', oauth2_views.ApplicationRegistration.as_view(),
                       name="register"),
                  path('o/admin/applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
                  path('o/admin/applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
                  path('o/admin/applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
                  # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

                  # My urls here
                  path('api/', include('users.urls')),

                  # Simple JWT urls here
                  path('api/token/refresh/', TokenRefreshView.as_view()),
                  path('api/token/verify/', TokenVerifyView.as_view()),

                  # Django Admin urls here
                  path('api/admin/', admin.site.urls),

                  # Swagger urls here
                  path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
