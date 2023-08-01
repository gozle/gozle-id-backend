from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=100)
    sortname = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
