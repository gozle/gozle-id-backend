from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from oauth2_provider.models import AbstractApplication
from django.contrib.auth.hashers import check_password

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
    is_active = models.BooleanField(default=True, blank=True)

    @classmethod
    def authorize(cls, client_id, client_secret):
        """
        Authorize an application with the given client_id and client_secret and return if exists.
        :param client_id:
        :param client_secret:
        :return:Object or False
        """
        try:
            application = cls.objects.get(client_id=client_id)
            if check_password(client_secret, application.client_secret):
                return application
            else:
                return False
        except ObjectDoesNotExist:
            return False
