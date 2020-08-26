"""
Django settings for onlinecoursecoupons project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# if DEBUG:
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# else:
#     from unipath import Path
#     BASE_DIR = Path(__file__).ancestor(3)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f$5d&42-%=p33lwl2f-_-qy7a=yq7o@@27ykzfw$e=m1+954at'


# ALLOWED_HOSTS = ['prasant7878.pythonanywhere.com', '127.0.0.1','ec2-54-167-87-176.compute-1.amazonaws.com','54.162.84.174','freecoupons.ddns.net','ip-172-31-49-183.ec2.internal', 'coursehub.ddns.net', 'coursehub.prasant.tech', 'couponstown.me']
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',
    'multiselectfield',
    'mathfilters',
    'fcm_django',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    
] 
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onlinecoursecoupons.urls'

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

WSGI_APPLICATION = 'onlinecoursecoupons.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR

FCM_DJANGO_SETTINGS = {
        "APP_VERBOSE_NAME": "fcm_django",
         # default: _('FCM Django')
        "FCM_SERVER_KEY": "AAAAdzMBPA0:APA91bEFXiA9Nf48xhQppwxCKCTjtToUa6ohzF7klRc1lIBcakeBFrJHnAtSACgWbIL0T-P5J2PubjkyhPF71lHb0svd91XbshoSnt5dE4AEVXZ4afjovSdEG64m3sFX57hMEy5-NTPH",
         # true if you want to have only one active device per registered user at a time
         # default: False
        "ONE_DEVICE_PER_USER": False,
         # devices to which notifications cannot be sent,
         # are deleted upon receiving error response from FCM
         # default: False
        "DELETE_INACTIVE_DEVICES": False,
}

CSRF_COOKIE_DOMAIN = '.couponstown.me'
CSRF_TRUSTED_ORIGINS = ['couponstown.me', 'coursehub.ddns.net', 'couponstown.ddns.net']