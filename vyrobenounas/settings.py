# coding: utf-8
import os
import operator
from decimal import Decimal
from django.urls import reverse_lazy

DEBUG = True
# Make this unique, and don't share it with anybody.
SECRET_KEY = r'dummy-secret-key'
COMPRESS_OFFLINE = True


# http://www.i18nguy.com/unicode/language-identifiers.html
LANG = "cs_CZ.UTF-8"
LANGUAGE = 'czech'
LANGUAGE_CODE = 'cs'  # controls gettext translation

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Prague'
USE_TZ = True
USE_I18N = True
USE_L10N = True


SITE_ID = 1
SITES = {
    'root': "localhost:8000",
}

ADMINS = (
    ('Tomáš Peterka', 'tomas@peterka.me'),
)

MANAGERS = ADMINS


# paths
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
RUNTIME_ROOT = os.path.normpath(os.path.join(APP_ROOT, "..", "var"))

MEDIA_ROOT = os.path.join(RUNTIME_ROOT, "media")
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(RUNTIME_ROOT, "static")
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_ROOT, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
            )
        },
    },
]

ROOT_URLCONF = 'market.urls'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'stats.middleware.StatsMiddleware',
    # 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

LOGIN_URL = reverse_lazy("account_login")
LOGOUT_URL = reverse_lazy("account_logout")
LOGIN_REDIRECT_URL = "/"


CACHE_PREFIX = ""
CACHE_TIMEOUT = 0
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211'
#    }
#}

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/var/mail/market/inbox'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = "ahoj@vyrobenounas.cz"
EMAIL_USE_LOCALTIME = True

TWITTER_CONSUMER_KEY = 'w0RCO8VOFTvEJNDK0Mxg'
TWITTER_CONSUMER_SECRET = 'h0hzHZn7nCiSpathxidf2SjMccvj9ybGsm5y7IChGU'

FACEBOOK_APP_ID = '102903073208172'
FACEBOOK_API_SECRET = '96d3a153e765743e739e4d9c65d75d21'

GOOGLE_OAUTH2_CLIENT_ID = '970941544914.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '7sFq7WljvQ4Qd-571xcLPilf'

ANALYTICS_ID = None

RECAPTCHA_PUBLIC_KEY = '6Lf01ykTAAAAAIRK_wojH0VU-7ur1tSoGRFY6mfG'
RECAPTCHA_PRIVATE_KEY = '6Lf01ykTAAAAACSl9YD_7TJUiBkq4LcdyrQpLph2'
NOCAPTCHA = False  # whether to use the new style reCaptcha
RECAPTCHA_USE_SSL = False


# APPS SPECIFIC SETTINGS

TAX = Decimal(21)

AUTH_USER_MODEL = "market.User"

MARKET_UID_LENGTH = 8
MARKET_PAY_ON_DELIVERY = True

ACCOUNT_ADAPTER = 'market.core.adapters.UserAdapter'
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "admin-email-confirmed"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "admin-email-confirmed"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_PASSWORD_MIN_LENGTH = 4
ACCOUNT_SIGNUP_FORM_CLASS = 'market.core.forms.BaseSignupForm'  # base class for account.forms.SignupForm
ACCOUNT_USER_DISPLAY = operator.attrgetter("name")
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_USERNAME_REQUIRED = False


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INVOICE_ADDRESS_MODEL = 'market.Address'
INVOICE_BANK_ACCOUNT_MODEL = 'market.BankAccount'
INVOICE_EXPORT = 'pdf'


ADDRESS_TEMPLATE = r"""{{name}}
{{street}}
{{zip_code}} {{city}}{% if business_id %}
{{business_id}}{% endif %}
"""


DATABASES = {
    'default': {
        # Engines: 'sqlite3', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',     # Or path to database file if using sqlite3.
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {},
    }
}

CACHE_PREFIX = ""
CACHE_TIMEOUT = 0
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # 'django.contrib.gis',
    'django_comments',
    'compressor',
    'captcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.openid',
    'rest_framework',

    'auditlog',
    # LIB dir
    'stats',
    'dbmail',
    'autocomplete_light',
    'stdimage',
    'bitcategory',
    'ratings',
    'invoice',
    'ckeditor',

    # market dir
    'market',  # because of static files and templates
    'market.core',
    'market.checkout',
    'market.tariff',
    'market.utils',
    # 'market.search',  # not ready yet
]

MB = 10**6
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debug_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(RUNTIME_ROOT, "log", 'market.error.log'),
            'maxBytes': 5 * MB,
            'backupCount': 2,
            'filters': ['require_debug_false', ]
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins', 'debug_file', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'django.db': {
            'handlers': ['console', 'debug_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'debug_file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

if DEBUG:
    INSTALLED_APPS.extend([
        "django_extensions",
        "debug_toolbar",
    ])

    MIDDLEWARE_CLASSES.append(
        'debug_toolbar.middleware.DebugToolbarMiddleware')

    # catcha field passes by default (has to have value "PASSED")
    os.environ['RECAPTCHA_TESTING'] = 'True'
