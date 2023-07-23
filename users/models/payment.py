import random
import string
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from sms import sms_sender
from users.models import User, Application


def generate_verification_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=40))


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    client = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='payments')
    description = models.TextField(blank=True, null=True)
    verification_code = models.CharField(max_length=40, blank=True)

    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set verification code if it is not set on save
        if not self.verification_code:
            self.verification_code = generate_verification_code()
        super(Payment, self).save(*args, **kwargs)

    def perform_payment(self):
        # Perform payment
        self.user.balance -= self.amount
        self.user.save()
        self.completed = True
        self.save()
        self.send_info_to_user()
        return True

    def send_info_to_user(self):
        # Send info about payment to user
        phone_number = self.user.phone_number
        message = f"Siziň Gozle ID hasabyňyzdan {self.client.name} serwisine {self.amount} GC tölendi.\n" + \
                  "Eger siz däl bolsaňyz Gozle ID goldaw bölümine ýüz tutuň!"
        sms_sender.send(phone_number, message)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.client.name}"

    @classmethod
    def get_object(cls, client, verification_code):
        """
        Get a payment object by client and verification code
        :param client:
        :param verification_code:
        :return:Object or False
        """
        try:
            return cls.objects.get(client=client, verification_code=verification_code)
        except ObjectDoesNotExist:
            return False
