from django.db import models


# email model class for user
class Email(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="email")
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
