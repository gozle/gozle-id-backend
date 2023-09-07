import os
from django.conf import settings

ORDER_SUCCESS_MESSAGE_TEMPLATE = {
    "en": 'Your Gozle ID balance has been topped up with {value}GC.',
    "ru": "Ваш баланс Gozle ID пополнен на сумму {value}GC.",
    "tm": "Siziň Gozle ID balansyňyz {value}GC köpeldi."
}

RESERVE_NUMBER_DELETION_TEMPLATE = {
    'en': "Your number has been deleted as a backup number in Gozle ID if you have not deleted the number, "
          "contact technical support",
    "ru": "Ваш номер удален как резервный номер в Gozle ID если вы не удаляли номер, обратитесь в техническую поддержку",
    "tm": "Gozle ID -de ätiýaçlyk belgisi hökmünde siziň belgiňiz öçürildi, öçürmedik bolsaňyz, tehniki goldaw bilen "
          "habarlaşmagyňyzy haýyş edýäris",
}

RESERVE_NUMBER_SUCCESS_TEMPLATE = {
    'en': "Your backup number has been successfully registered as a backup phone number for Gozle ID . Please save "
          "this number: {phone_number}",
    "ru": "Ваш резервный номер успешно зарегистрирован как резеврный номер телефона для Gozle ID . Пожалуйста, "
          "сохраните этот номер: {phone_number}",
    "tm": "Siziň belgiňiz Gozle ID-iň ätiýaçlyk telefon belgisi hökmünde üstünlikli hasaba alyndy. Bu belgini ýatda "
          "saklamagyňyzy haýyş edýäris: {phone_number}",
}

RESERVE_NUMBER_MESSAGE_TEMPLATE = {
    'en':
        """Your number is registered as a reserve number for Gozle ID.

Verification code {code}

If it's not you, ignore the message.""",

    # RU
    'ru':
        """Ваш номер зарегистрирован как резервный номер для Gozle ID .

Код для потверждения {code}

Если это не вы проигнорируйте сообщение""",

    # TM
    'tm':
        """Siziň belgiňiz Gozle ID-iň ätiýaçlyk belgisi hökmünde hasaba alyndy.

Barlag kody {code}

Eger siz däl bolsaňyz, habara üns bermäň."""
}

GIFTCARD_MESSAGE_TEMPLATE = {
    "en": "Your account has been topped up with {value} GC using a gift card.",
    "ru": "Ваш счет Gozle ID был пополнен на {value} GC с помощью подарочной карты.",
    "tm": "Siziň Gozle ID hasabyňyza GiftCard üsti bilen {value} GC geçirildi."
}

LOGIN_MESSAGE_TEMPLATE = {
    "en":
        """Your account has Gozle ID login {day}/{month}/{year} in {hour}:{minute}.

Device: {device}
IP Address: {ip}

If this is not you, log in to your Gozle ID and change the password.""",

    # Ru

    "ru":
        """В ваш аккаунт Gozle ID выполнен вход  {day}/{month}/{year} в {hour}:{minute}.

Устройство: {device}
IP-адрес: {ip}

Если это были не вы, войдите в свою учетную запись Gozle ID и измените пароль.""",

    # Tm

    "tm":
        """{day}/{month}/{year} sagat {hour}:{minute}-da "Gozle ID" hasabyňyza girildi.

Enjam: {device}
IP: {ip}

Eger siz däl bolsaňyz, Gozle ID hasabyňyza giriň we parolyňyzy üýtgediň"""
}

DOMAIN = 'https://i.gozle.com.tm'

SERVICE_TYPE_CHOICES = (
    ('service', 'Service'),
    ('commerce', 'Commerce'),
    ('social', 'Social'),
)

CARD_TEMPLATE = os.path.join(settings.STATIC_ROOT, "card-template.jpg")
FONT = os.path.join(settings.STATIC_ROOT, "Roboto-Regular.ttf")
