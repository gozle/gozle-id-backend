from django.db import models

from users.models.user import User


class TempUser(models.Model):
    user_id = models.IntegerField()
    password = models.CharField(max_length=100)
    code = models.IntegerField()

    def __str__(self):
        return self.user_id


class TempToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='temptoken')
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
