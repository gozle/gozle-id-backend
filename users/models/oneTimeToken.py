import random
import string

from django.db import models


def generate_token():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))


class OneTimeToken(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_for_user(cls, user):
        obj = cls.objects.create(user=user, token=generate_token())
        obj.save()

        return obj
