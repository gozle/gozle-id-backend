from datetime import datetime

from django.db import models

from config import RESERVE_NUMBER_MESSAGE_TEMPLATE, RESERVE_NUMBER_SUCCESS_TEMPLATE
from sms import sms_sender
from users.models.validators import validate_phone_number


class ReservePhoneNumber(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="reserve_phone_number")
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    verification_code = models.CharField(max_length=5, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

    def send_verification_code(self):
        message = RESERVE_NUMBER_MESSAGE_TEMPLATE.get(self.user.language, RESERVE_NUMBER_MESSAGE_TEMPLATE['tm'])
        message = message.format(code=self.verification_code)

        sms_sender.send(self.phone_number, message)

    def activate(self):
        self.activated_at = datetime.now()
        self.is_active = True
        self.save()
        message = RESERVE_NUMBER_SUCCESS_TEMPLATE.get(self.user.language, RESERVE_NUMBER_SUCCESS_TEMPLATE['tm'])
        message = message.format(phone_number=self.phone_number)

        sms_sender.send(self.phone_number, message)
