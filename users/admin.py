from django.contrib import admin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Verification


class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "first_name", "last_name", "email"]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Verification)
