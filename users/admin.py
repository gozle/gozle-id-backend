from django.contrib import admin

from users.models import Region, City, Bank

from .forms import CustomUserChangeForm, GiftCardForm
from .models import GiftCard, Login, User, Verification, Language
from modeltranslation.admin import TranslationAdmin


class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "first_name", "phone_number", "balance"]
    search_fields = ["username", "phone_number"]


class GiftCardAdmin(admin.ModelAdmin):
    form = GiftCardForm
    model = GiftCard
    list_filter = ["used", "image"]


class RegionAdmin(TranslationAdmin):
    pass


class CityAdmin(TranslationAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(Verification)
admin.site.register(GiftCard, GiftCardAdmin)
admin.site.register(Login)
admin.site.register(Language)
# admin.site.register(Application)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Bank)