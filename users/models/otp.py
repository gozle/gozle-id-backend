from django.db import models


TRANSPORT_CHOICES = (
    ('email', 'Email'),
    ('sms', 'sms'),
)


class OTP(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=40)
    is_used = models.BooleanField(default=False)
    purpose = models.CharField(max_length=50)
    transport = models.CharField(max_length=40)

    sent_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
