from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import GiftCard, User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "birthday", "ip_address",
                  "mac_address", "phone_number", "device_info", "email", "avatar")


class GiftCardForm(forms.ModelForm):
    class Meta:
        model = GiftCard
        fields = ("value", "image")
