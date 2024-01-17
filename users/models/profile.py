# Profile class that stores username first name last name etc and connected to User model
from django.db import models

from users.models.validators import validate_names


class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, validators=[validate_names])
    last_name = models.CharField(max_length=100, validators=[validate_names])
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    avatar = models.ImageField(
        upload_to='avatars/%d', default='default/default_avatar.jpg', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
