from django.db import models

from users.models import Region

class City(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    region = models.ForeignKey(Region, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
