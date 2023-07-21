from oauth2_provider.models import AbstractApplication

from django.db import models

TYPE_CHOICES = (
    ('service', 'Service'),
    ('commerce', 'Commerce'),
    ('social', 'Social'),
)


# Extends AbstractApplication to add a logo field and service type.
class Application(AbstractApplication):
    logo = models.ImageField(upload_to='icons', blank=True, null=True)
    service_type = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True, default='service')
    skip_authorization = models.BooleanField(default=True, blank=True)
