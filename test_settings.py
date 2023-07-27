from GozleUsers.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dbbbb.sqlite3'),
    }
}

OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'  # 'users.Application'
