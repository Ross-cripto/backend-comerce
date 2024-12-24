from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("NAME", default='Inventory'),
        'USER': env("USER", default='postgres'),
        'PASSWORD': env("PASSWORD", default='root'),
        'HOST': env("HOST", default='localhost'),
        'PORT': env("PORT", default='5432'),
    }
}