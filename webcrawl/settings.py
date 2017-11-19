from __future__ import absolute_import
"""
Django settings for webcrawl project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from os.path import join, abspath, normpath, dirname

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_DIR = normpath(os.environ.get('DATA_DIR', join(BASE_DIR, '__data__')))
DATA_DIR = normpath(os.environ.get('DATA_DIR', join(BASE_DIR)))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7_sr97nric#y#!wg=*b3x-rxqhfp#vn*m(lx7s#lkkh%1%+12i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_mongoengine',
    'djcelery',
    # '''core'''
    'core.crawling',
    
    # '''api'''
    'api.crawlingManage',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webcrawl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'webcrawl.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# import os
# import mongoengine
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.dummy'
#     }
# }
# AUTHENTICATION_BACKENDS = (
#     'mongoengine.django.auth.MongoEngineBackend',
# )

# MONGODB_HOST = os.environ.get('localhost', '127.0.0.1')
# mongoengine.connect(host="db2")


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Redis
REDIS_HOST = 'redis'
REDIS_DB = os.environ.get('REDIS_DB', 0)

# Celery
# BROKER_URL = 'redis://127.0.0.1:6379/0'




# Celery

BROKER_TRANSPORT = 'redis'
CELERY_BROKER_TRANSPORT = BROKER_URL = 'redis://%s:6379/0' % REDIS_HOST
CELERY_RESULT_BACKEND = 'redis://%s:6379/0' % REDIS_HOST
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']  # Ignore other content
CELERY_RESULT_SERIALIZER = 'json'
# CELERYBEAT_SCHEDULE_FILENAME = join(DATA_DIR, 'celerybeat.db')
CELERYBEAT_SCHEDULE_FILENAME = join(BASE_DIR, 'celerybeat.db')
# CELERY_BEAT_SCHEDULE_FILENAME = join(DATA_DIR, 'celerybeat.db')
CELERYBEAT_SCHEDULE = {}
# CELERY_BEAT_SCHEDULE = {}



import djcelery
djcelery.setup_loader()
from datetime import timedelta
from celery.schedules import crontab

# Other Celery settings
# CELERY_BEAT_SCHEDULE = {
#     'task-number-one': {
#         'task': 'api.crawlingManage.tasks.task_number_one',
#         # 'schedule': crontab(),
#         'schedule': crontab(),
#         # 'args': (*args)
#     }
# }

CELERYBEAT_SCHEDULE = {
    # 'task-number-one': {
    #     'task': 'api.crawlingManage.tasks.task_number_one',
    #     # 'schedule': crontab(),
    #     'schedule': timedelta(seconds=60),
    #     # 'args': (*args)
    # },
    'task-craw-feed': {
            'task': 'api.crawlingManage.tasks.crawl_feed',
            # 'schedule': crontab(),
            'schedule': timedelta(seconds=300),
            # 'args': (*args)
        },
    'task-crawl-data': {
            'task': 'api.crawlingManage.tasks.crawl_data',
            # 'schedule': crontab(),
            'schedule': timedelta(seconds=600),
            # 'args': (*args)
        }
}

if __name__ == "__main__":
    print (DATA_DIR)