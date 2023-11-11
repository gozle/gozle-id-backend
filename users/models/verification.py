from django.db import models


class Verification(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name='verification')
    type = models.CharField(max_length=10, default="phone", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user", "type"]]

    def __str__(self):
        return str(self.code)
