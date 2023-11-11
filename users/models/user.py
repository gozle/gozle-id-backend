import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models

from sms import sms_sender
from users.models.city import City

from users.models.region import Region
from .verification import Verification

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
    email_verified = models.BooleanField(default=False, blank=True)

    device_info = models.CharField(max_length=400, null=True, blank=True)

    region = models.ForeignKey('users.Region', blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('users.City', blank=True, null=True, on_delete=models.SET_NULL)
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

        if request.data.get("email"):
            self.email = request.data.get('email')
            self.save()
            self.add_email()

        if request.data.get("region"):
            try:
                region = Region.objects.get(id=request.data.get("region"))
                self.region = region
            except ObjectDoesNotExist:
                pass
        if request.data.get("city"):
            try:
                city = City.objects.get(id=request.data.get("city"))
                self.city = city
            except ObjectDoesNotExist:
                pass
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

    # def register_reserve_phone_number(self, phone_number):
    #     rph = ReservePhoneNumber.objects

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        if not self.language:
            try:
                lang = Language.objects.get(short_name="tk")
                self.language = lang
            except ObjectDoesNotExist:
                pass
        self.phone_number = get_valid_phone_number(self.phone_number)
        self.validate_unique()
        super(User, self).save(*args, **kwargs)

    def add_email(self):
        verification_number = random.randint(10000, 99999)
        try:
            verification = self.verifications.get(type="email")
            verification.delete()
        except ObjectDoesNotExist:
            pass
        verification = Verification(code=verification_number, user=self, type="email")

        self.send_email("verification@gozle.com.tm",
                        "Your Gozle ID email verification code is: " + str(verification_number))
        verification.save()

    def send_email(self, from_email, message):
        send_mail(
            "Gozle ID",
            str(message),
            from_email,
            [self.email],
            fail_silently=False,
        )

    def send_message(self, message):
        sms_sender.send(self.phone_number, message)
