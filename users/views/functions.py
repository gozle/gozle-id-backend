from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Verification
from users.models.functions import get_valid_phone_number


# Function to get tokens for user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Function to get valid phone number


def check_user_exists(phone_number):
    try:
        user = User.objects.get(phone_number=get_valid_phone_number(phone_number))
        return user
    except ObjectDoesNotExist:
        return None


# Function to delete old verification codes if passed 1 minute
def verify_and_delete(user, type):
    try:
        verification = Verification.objects.get(user=user, type=type)
        if verification.created_at > (timezone.now() - timezone.timedelta(minutes=1)):
            return False
        print('BEFORE DELETE:', Verification.objects.filter(user=user, type=type).count())
        Verification.objects.filter(user=user, type=type).delete()
        print('AFTER DELETE:', Verification.objects.filter(user=user, type=type).count())
        return True
    except ObjectDoesNotExist:
        return True


# Function to get url from dict
def get_url_from_dict(dict):
    url = '/o/authorize/?'
    for key, value in dict.items():
        url += key + "=" + value + "&"
    return url[:-1]
