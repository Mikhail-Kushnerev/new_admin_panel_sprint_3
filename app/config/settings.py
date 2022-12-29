import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from split_settings.tools import include
from dotenv import load_dotenv

secret_key = get_random_secret_key()
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default=secret_key)

DEBUG = os.getenv('DEBUG', default=False) == 'True'

ALLOWED_HOSTS = (os.getenv('HOST'),)

include(
    'components/authentication.py',
    'components/database.py',
    'components/middleware.py',
    'components/templates.py',
    'components/apps.py',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LOCALE_PATHS = ('movies/locale',)

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
