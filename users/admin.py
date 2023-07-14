from django.contrib import admin

from .forms import CustomUserCreationForm, CustomUserChangeForm, GiftCardForm
from .models import GiftCard, Login, User, Verification


class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "first_name", "phone_number", "balance"]
    search_fields = ["username", "phone_number"]


class GiftCardAdmin(admin.ModelAdmin):
    form = GiftCardForm
    model = GiftCard
    list_filter = ["used", "image"]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Verification)
admin.site.register(GiftCard, GiftCardAdmin)
admin.site.register(Login)
