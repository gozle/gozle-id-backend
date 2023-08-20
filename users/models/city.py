from django.db import models

class City(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    region = models.ForeignKey("users.Region", related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
