import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '14u_t_2p+*4r6jyj(!zg48h1ifbqga+q00szndh4rx-ce47yhb3'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.path.join(BASE_DIR, 'testdb'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media/')

confirm_interview_url = ""
choose_interview_url = ""

EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 123
EMAIL_HOST_USER = 'hackbulgaria@gmail.com'
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

f6s_address = "https://api.f6s.com/"
f6s_application_name = ""
f6s_api_key = ""
f6s_page_count = 100
f6s_page = 1
