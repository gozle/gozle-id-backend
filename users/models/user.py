import re
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


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
        return '+993' + number[1:]
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
    reserve_phone_number = models.CharField(max_length=30, validators=[validate_phone_number])
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
