import os


DATABASES = {
    'default': {
        'ENGINE': os.getenv('POSTGRES_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('POSTGRES_DB', default='postgres'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': os.getenv('POSTGRES_PORT', default=5432),
        'OPTIONS': {
            'options': '-c search_path=public,content',
        },
    },
}
