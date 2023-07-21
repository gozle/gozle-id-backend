from django.db import models

from users.models.user import User


class Verification(models.Model):
    code = models.IntegerField()
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='verification')
    type = models.CharField(max_length=10, default="phone", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)
