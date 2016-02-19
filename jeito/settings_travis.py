from .settings import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'jeito',
        'USER': 'postgres',
        'PASSWORD': '',
    }
}

SECRET_KEY = 'thisisjustatravistest'
DEBUG = False
