from Project.settings.base import *

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration


# sentry_sdk.init(
#     dsn="https://bbb5beae48224be9a2841ba21ea41308@o383171.ingest.sentry.io/5213105",
#     integrations=[DjangoIntegration()],
#     send_default_pii=True
# )

DEBUG = (os.environ.get('DEBUG') == 'True')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASS'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': '5432',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    # 'path.to.custom.Loader',
                ]), ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.project_requirements.context_processors.site_defaults',
                'apps.geoposition.context_processors.google_map_key',
            ],
        },
    },
]

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
# EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = os.environ['EMAIL_USER']
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASS']
# EMAIL_PORT = 587


# CORS_REPLACE_HTTPS_REFERER = True
# HOST_SCHEME = "https://"
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 1000000
# SECURE_FRAME_DENY = True


# from Portal.aws.conf import *
