from django.db import models

from users.models.user import User


class CoinHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="history")
    amount = models.IntegerField()
    source = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
