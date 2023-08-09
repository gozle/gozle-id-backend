import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models

from .language import Language
from users.models.reservePhoneNumber import ReservePhoneNumber
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
    email = models.TextField(blank=True, null=True)
    device_info = models.CharField(max_length=400, null=True, blank=True)

    region = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    theme = models.CharField(max_length=10, default="light", blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)

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

    def update(self, request):
        self.username = request.data.get('username', self.username)
        self.first_name = request.data.get('first_name', self.first_name)
        self.last_name = request.data.get('last_name', self.last_name)
        self.birthday = request.data.get('birthday', self.birthday)
        self.email = request.data.get('email', self.email)
        self.region = request.data.get("region", self.region)
        self.theme = request.data.get("theme", self.theme)
        self.gender = request.data.get("gender", self.gender)
        if request.data.get("language"):
            try:
                language = Language.objects.get(id=request.data.get("language"))
                self.language = language
            except ObjectDoesNotExist:
                pass
        self.avatar = request.FILES.get('avatar', self.avatar)
        self.save()

    @classmethod
    def check_if_in_reserve(cls, phone_number):
        if ReservePhoneNumber.objects.filter(phone_number=phone_number).exists():
            return True
        return False

    # def register_reserve_phone_number(self, phone_number):
    #     rph = ReservePhoneNumber.objects

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        if not self.language:
            try:
                lang = Language.objects.get(sortname="tk")
                self.language = lang
            except ObjectDoesNotExist:
                pass
        self.phone_number = get_valid_phone_number(self.phone_number)
        self.validate_unique()
        super(User, self).save(*args, **kwargs)
