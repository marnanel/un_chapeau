import os
from .localsettings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'oauth2_provider',
    'corsheaders',
    'django_fields',

    'trilby_api',
    'kepi_activity',
    'buckethat_salmon',
    'tophat_ui',
]

MIDDLEWARE = [

    'oauth2_provider.middleware.OAuth2TokenMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'un_chapeau.middleware.middleware',
]

ROOT_URLCONF = 'un_chapeau.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'un_chapeau.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
        'oauth2_provider.backends.OAuth2Backend',
        'django.contrib.auth.backends.ModelBackend',
)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

STATIC_ROOT = '/var/www/ucstatic/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/var/www/ucmedia/'
MEDIA_URL = '/media/'

APPEND_SLASH = False

OAUTH2_PROVIDER = {

        'SCOPES': {
            'read': 'Read toots',
            'write': 'Post toots',
            'follow': 'Follow other users',
            },

        'ALLOWED_REDIRECT_URI_SCHEMES': ['urn', 'http', 'https'],

        }

REST_FRAMEWORK = {

        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
            ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            ),
        }

AUTH_USER_MODEL = 'trilby_api.User'

########################

UN_CHAPEAU = {
        'HOSTNAME': 'unchapeau-dev.marnanel.org', # XXX there has to be a better way
        'INSTANCE_NAME': 'un_chapeau test',
        'INSTANCE_DESCRIPTION': 'this is a test',
        'CONTACT_ACCOUNT': 'marnanel',
        'CONTACT_EMAIL': 'marnanel@example.com',
        'LANGUAGES': ['en'],

        'STATUS_URLS': 'https://{hostname}/users/{username}/{id}',
        'STATUS_FEED_URLS': 'https://{hostname}/users/{username}/feed/{id}',
        'STATUS_ACTIVITY_URLS': 'https://{hostname}/users/{username}/{id}/json',
        'USER_URLS': 'https://{hostname}/users/{username}',
        'USER_FEED_URLS': 'https://{hostname}/users/{username}/feed',
        'USER_SALMON_URLS': 'https://{hostname}/users/{username}/salmon',
        'USER_WEBFINGER_URLS': 'https://{hostname}/.well-known/webfinger?resource=acct:{acct}',
        'USER_FOLLOWING_URLS': 'https://{hostname}/users/{username}/following',
        'USER_FOLLOWERS_URLS': 'https://{hostname}/users/{username}/followers',
        'USER_INBOX_URLS': 'https://{hostname}/users/{username}/inbox',
        'USER_OUTBOX_URLS': 'https://{hostname}/users/{username}/outbox',
        'SHARED_INBOX_URL': 'https://{hostname}/inbox',

        'HUB': 'https://switchboard.p3k.io/', # or whatever

        # the "{uri}" in AUTHORIZE_FOLLOW_TEMPLATE is for the client to
        # fill in, not us. We pass it out as is.
        'AUTHORIZE_FOLLOW_TEMPLATE': 'https://%(hostname)s/authorize_follow?acct={{uri}}',
        }

######################################


######################################
