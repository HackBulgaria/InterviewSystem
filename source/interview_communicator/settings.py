from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'ckeditor',
    'post_office',

    'course_interviews'
)

# Post_Office settings:
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp-pulse.com'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'ivaylo@hackbulgaria.com'
EMAIL_HOST_PASSWORD = '76anmbCKrDWEYW'
DEFAULT_FROM_EMAIL = 'register@hackbulgaria.com'

# EMAIL_USE_TLS = True
# EMAIL_HOST = ''
# EMAIL_PORT = 123
# EMAIL_HOST_USER = 'hackbulgaria@gmail.com'
# EMAIL_HOST_PASSWORD = ''
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_BACKEND = 'post_office.EmailBackend'
POST_OFFICE = {
    'LOG_LEVEL': 2  # logs everything (both successful and failed delivery attempts)
}

# End of Post_Office settings

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'interview_communicator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'interview_communicator.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Admin',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True,  # Default True

    # menu
    # 'SEARCH_URL': '/admin/hack_fmi/competitor/',
    'MENU_ICONS': {
        'auth': 'icon-lock',
    },
    'MENU_OPEN_FIRST_CHILD': True,  # Default True
    'MENU_EXCLUDE': ('auth.group',),
    'MENU': (
        {'app': 'course_interviews', 'icon': 'icon-pencil'},
        {'app': 'post_office', 'icon': 'icon-envelope'},
    ),

    # misc
    'LIST_PER_PAGE': 100
}

AUTH_USER_MODEL = 'course_interviews.Teacher'

try:
    from .local_settings import *
except ImportError:
    exit("local_settings.py not found!")
