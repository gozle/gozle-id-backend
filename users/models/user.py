import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.models.validators import validate_names, validate_phone_number
from users.models.functions import get_valid_phone_number


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

    region = models.CharField(max_length=100, blank=True, null=True)
    theme = models.CharField(max_length=10, default="light", blank=True)
    language = models.CharField(max_length=10, default="en", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to='avatars/%d', default='default/default_avatar.jpg', blank=True, null=True)
    two_factor_auth = models.CharField(
        max_length=20, default='default', blank=True)

    def __str__(self):
        return str(self.username)

    def check_balance(self, amount):
        if int(amount) > self.balance:
            return False
        return True

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        self.phone_number = get_valid_phone_number(self.phone_number)
        self.validate_unique()
        super(User, self).save(*args, **kwargs)
