import os
from pathlib import Path

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.environ['SECRET_KEY']
DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'debug_toolbar',
    'corsheaders',
    'crispy_forms',
    "crispy_bootstrap5",
    'import_export',
    'multiselectfield',
    'rest_framework',
    'rosetta',
    'tinymce',
]
LOCAL_APPS = [
    'apps.accounts',
    'apps.analytics',
    'apps.celebrations',
    'apps.competitions',
    'apps.core',
    'apps.files',
    'apps.geoposition',
    'apps.jurisdictions',
    'apps.payments',
    'apps.projects',
    'apps.registrations',
    'apps.training',
    'apps.youth_programme',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ROOT_URLCONF = 'Project.urls'
WSGI_APPLICATION = 'Project.wsgi.application'

SITE_ID = 1
AUTH_USER_MODEL = 'accounts.User'

ADMINS = [('Charles', 'ngangaricharles@gmail.com'), ]
# SERVER_EMAIL = 'KSA Portal @ksa-portal.kenyascouts.org'
# DEFAULT_FROM_EMAIL = 'app@kenyascouts.org <noreply@app@kenyascouts.org>'
EMAIL_SUBJECT_PREFIX = ' '

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'myproject.custom': {
#             'handlers': ['console', 'mail_admins'],
#             'level': 'INFO',
#         }
#     }
# }

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'add'
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'view'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

GEOPOSITION_GOOGLE_MAPS_API_KEY = os.environ['GEOPOSITION_GOOGLE_MAPS_API_KEY']
GEOPOSITION_MAP_OPTIONS = {'minZoom': 1, 'maxZoom': 25, }
GEOPOSITION_MARKER_OPTIONS = {'cursor': 'move'}
GEOPOSITION_MAP_WIDGET_HEIGHT = 500

TINYMCE_DEFAULT_CONFIG = {
    "branding": False,
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": '''advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code
                fullscreen insertdatetime media table paste code help wordcount spellchecker''',
    "toolbar": '''fullscreen undo redo | bold italic underline strikethrough | fontselect fontsizeselect
            formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist
            checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak |
            charmap emoticons |  preview save print | insertfile image media pageembed template link anchor
            codesample |  a11ycheck ltr rtl | showcomments addcomment code''',
    "custom_undo_redo_levels": 50,
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ]
}


LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('sw', _('Swahili')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
