import os
import string
import tempfile

from django.conf import settings
from django.core.files import File
from django.db import models
from django.utils.crypto import get_random_string
from PIL import Image as PILImage, ImageDraw, ImageFont

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

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(
                16, string.ascii_uppercase + string.digits)

        pil_image = PILImage.open(CARD_TEMPLATE)
        width, height = pil_image.size
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype(FONT, 64)
        draw.text((width / 4, height / 2), hyphenate(self.code),
                  fill='black', font=font)
        temp_file = tempfile.NamedTemporaryFile()
        pil_image.save(temp_file, 'jpeg')

        if not self.image:
            self.image.save(self.code + '.jpg', File(temp_file))

        super().save(*args, **kwargs)
