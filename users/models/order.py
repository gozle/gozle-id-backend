import datetime
import random

from django.db import models

from users.models import Bank
from users.models.user import User

STATUS_CHOICES = (
    ('pending', "Pending"),
    ('error', "Error"),
    ('completed', "Completed"),
)


class Order(models.Model):
    order_id = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)

    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, related_name="orders")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_order_id(self):
        today = datetime.date.today()
        year = today.year
        month = today.month
        day = today.day

        order_id = "%02d%02d%02d" % (year, month, day)
        order_id += "{:03d}".format(self.id)
        return order_id
