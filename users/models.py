import tempfile
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
import os
from django.core.files import File
from PIL import Image as PILImage, ImageDraw, ImageFont

from django.core.exceptions import ValidationError
import re
import string
import uuid
# Create your models here.

CARD_TEMPLATE = os.path.join(settings.STATIC_ROOT, "card-template.jpg")
FONT = os.path.join(settings.STATIC_ROOT, "Roboto-Regular.ttf")


def validate_phone_number(value):
    pattern = r'^(\+9936|9936|6|86)\d{7}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number')


def validate_names(value):
    pattern = r'^[\w\s]+$'
    if not re.match(pattern, value):
        raise ValidationError('Name can contain only letters and space')
    if re.search(r'\d', value):
        raise ValidationError("Name can't contain any numbers")


def get_valid_phone_number(number):
    if len(number) == 11:
        return '+' + number
    elif len(number) == 8:
        return '+993' + number
    elif len(number) == 9:
        return '+993'+number[1:]
    return number


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=30, unique=True, validators=[RegexValidator(
        regex='^[a-zA-Z0-9_]*$',
        message="Username must be alphanumeric and can only contain underscores",
        code='invalid_username'
    )])
    first_name = models.CharField(max_length=100, validators=[validate_names])
    last_name = models.CharField(max_length=100, validators=[validate_names])
    birthday = models.DateField(null=True, blank=True)
    balance = models.IntegerField(default=0, blank=True)

    ip_address = models.CharField(max_length=400, blank=True, null=True)
    mac_address = models.CharField(max_length=400, blank=True, null=True)

    phone_number = models.CharField(
        max_length=30, unique=True, validators=[validate_phone_number])
    email = models.TextField(blank=True, null=True)
    device_info = models.CharField(max_length=400, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to='avatars/%d', default='default/default_avatar.jpg', blank=True, null=True)
    two_factor_auth = models.CharField(
        max_length=20, default='none', blank=True)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        self.phone_number = get_valid_phone_number(self.phone_number)
        self.validate_unique()
        super(User, self).save(*args, **kwargs)


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


class Verification(models.Model):
    code = models.IntegerField()
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='verification')
    type = models.CharField(max_length=10, default="phone", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)


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


STATUS_CHOICES = (
    ('pending', "Pending"),
    ('error', "Error"),
    ('completed', "Completed"),
)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order_id = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)

    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default="TMT", blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transfer(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.IntegerField()

    verification_code = models.IntegerField()

    completed = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} sent {self.amount} to {self.receiver.username} at {self.timestamp}'


def hyphenate(s):
    return "-".join([s[i:i+4] for i in range(0, len(s), 4)])


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
        draw.text((width/4, height/2), hyphenate(self.code),
                  fill='black', font=font)
        temp_file = tempfile.NamedTemporaryFile()
        pil_image.save(temp_file, 'jpeg')

        if not self.image:
            self.image.save(self.code+'.jpg', File(temp_file))

        super().save(*args, **kwargs)


class CoinHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="history")
    amount = models.IntegerField()
    source = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
