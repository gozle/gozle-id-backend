import os
import string
import tempfile

from django.conf import settings
from django.core.files import File
from django.db import models
from django.utils.crypto import get_random_string
from PIL import Image as PILImage, ImageDraw, ImageFont

from sms import sms_sender
from users.models import CoinHistory

CARD_TEMPLATE = os.path.join(settings.STATIC_ROOT, "card-template.jpg")
FONT = os.path.join(settings.STATIC_ROOT, "Roboto-Regular.ttf")


def hyphenate(s):
    return "-".join([s[i:i + 4] for i in range(0, len(s), 4)])


class GiftCard(models.Model):
    value = models.IntegerField()
    code = models.CharField(max_length=16, blank=True)
    image = models.ImageField(upload_to="cards/%d", blank=True)
    used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def use(self, user):
        # This function will be called when the user uses the gift card.
        # It will add the user's balance to the user's balance and save history.
        # And send a message to the user's phone number.
        user.balance += self.value
        self.used = True
        self.save()
        user.save()

        # Add coin history
        coin_history = CoinHistory.objects.create(user=user, amount=self.value, source="GiftCard")
        coin_history.save()

        self.send_info_to_user(user)

    def send_info_to_user(self, user):
        # Function to send a message to the user's phone number.
        phone_number = user.phone_number
        message = f"Siziň Gozle ID hasabyňyza GiftCard üsti bilen {self.value} GC geçirildi."
        sms_sender.send(phone_number, message)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(
                16, string.ascii_uppercase + string.digits)

        if not self.image:
            pil_image = PILImage.open(CARD_TEMPLATE)
            width, height = pil_image.size
            draw = ImageDraw.Draw(pil_image)
            font = ImageFont.truetype(FONT, 64)
            draw.text((width / 4, height / 2), hyphenate(self.code),
                      fill='black', font=font)
            temp_file = tempfile.NamedTemporaryFile()
            pil_image.save(temp_file, 'jpeg')

            self.image.save(self.code + '.jpg', File(temp_file))

        super().save(*args, **kwargs)
