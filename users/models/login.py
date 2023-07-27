import pytz
from django.db import models

from config import LOGIN_MESSAGE_TEMPLATE
from sms import sms_sender
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

    def send_info_about_login(self):
        date = self.created_at.astimezone(pytz.timezone("Asia/Ashgabat")).date()
        time = self.created_at.astimezone(pytz.timezone("Asia/Ashgabat")).time()

        message = LOGIN_MESSAGE_TEMPLATE.get(self.user.language, LOGIN_MESSAGE_TEMPLATE['tm'])
        message = message.format(year=date.year, month=date.month, day=date.day, hour=time.hour,
                                 minute=time.minute, device=self.os, ip=self.ip_address)

        sms_sender.send(self.user.phone_number, message)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_info_about_login()
