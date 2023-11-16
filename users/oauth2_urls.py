from django.urls import path
import oauth2_provider.views as oauth2_views

urlpatterns = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    path('admin/applications/', oauth2_views.ApplicationList.as_view(), name="list"),
    path('admin/applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
    path('admin/applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
    path('admin/applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
    path('admin/applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
]
