from django.db import models

from users.models.user import User


class TempToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='temptoken')
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
