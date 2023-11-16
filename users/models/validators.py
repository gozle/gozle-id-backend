import re
import emoji
from django.core.exceptions import ValidationError


# Function to validate name
def validate_names(value):
    pattern = r'^[\w\s]+$'
    print(emoji.emoji_count(value))
    if emoji.emoji_count(value):
        raise ValidationError('Name cannot contain emojis')
    if not re.match(pattern, value):
        raise ValidationError('Name can contain only letters and space')
    if re.search(r'\d', value):
        raise ValidationError("Name can't contain any numbers")


# Function to validate phone number
def validate_phone_number(value):
    pattern = r'^(\+9936|9936|6|86)\d{7}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number')
