import uuid

from django.db import models

from users.models.user import User

STATUS_CHOICES = (
    ('pending', "Pending"),
    ('error', "Error"),
    ('completed', "Completed"),
)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order_id = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)

    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default="TMT", blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
