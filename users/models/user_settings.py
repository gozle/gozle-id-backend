from django.db import models


class UserSetting(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="settings")

    region = models.ForeignKey('users.Region', blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('users.City', blank=True, null=True, on_delete=models.SET_NULL)
    theme = models.CharField(max_length=10, default="light", blank=True)
    language = models.ForeignKey('users.Language', on_delete=models.SET_NULL, null=True, blank=True)

    two_factor_auth = models.CharField(max_length=20, default='default', blank=True)
