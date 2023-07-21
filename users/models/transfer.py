from django.db import models

from users.models.user import User


class Transfer(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.IntegerField()

    verification_code = models.IntegerField()

    completed = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} sent {self.amount} to {self.receiver.username} at {self.timestamp}'
