from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="icons", blank=True, null=True)
    merchant_username = models.CharField(max_length=255)
    merchant_password = models.CharField(max_length=255)
    register_url = models.TextField()
    status_url = models.TextField()
    currency = models.IntegerField(default=934, blank=True)
