from django.db import models

from users.models.user import User


class Login(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="logins")
    ip_address = models.CharField(max_length=40, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
