"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f9rq7$d%mf-9gxp%3=pf!)ytsjcjzq+-46*cfpb)u_s9cu58^a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # package untuk rest api
    'rest_framework',
    # package untuk filtering
    'django_filters',
    # package untuk JWT
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # package reset password
    'django_rest_passwordreset',
    # nama aplikasi
    'bookstore.apps.BookstoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',
                 BASE_DIR / 'bookstore/templates',
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',      # Ganti dengan nama database Anda
        'USER': '',      # Ganti dengan username PostgreSQL Anda
        'PASSWORD': '',     # Ganti dengan password Anda
        'HOST': 'localhost',          # Ganti dengan host jika diperlukan
        'PORT': '5432',               # Ganti dengan port jika diperlukan
        'OPTIONS': {
            'options': '-c search_path=myschema,bookstore'  # Ganti dengan schema Anda
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True

# rubah model authentikasi 

AUTH_USER_MODEL = 'bookstore.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# setting untuk package rest_framemork, menambahkan pagination
# dan filter

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS':['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'bookstore.authentication.CustomJWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),  # Masa berlaku access token (default 5 menit)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Masa berlaku refresh token (default 7 hari)
    'ROTATE_REFRESH_TOKENS': True,                   # Set False jika tidak ingin refresh token diperbarui
    'BLACKLIST_AFTER_ROTATION': True,                 # Set True untuk mem-blacklist refresh token yang sudah diganti
    'UPDATE_LAST_LOGIN': False,                       # Set True jika ingin memperbarui last login saat login berhasil
    'ALGORITHM': 'HS256',                             # Algoritma yang digunakan untuk menandatangani token (default: HS256)
    'SIGNING_KEY': SECRET_KEY,                        # Kunci untuk menandatangani JWT, pastikan ini cukup kuat
    'VERIFYING_KEY': None,                            # Verifikasi kunci publik (misalnya jika kamu menggunakan RS256)
    'AUTH_HEADER_TYPES': ('Bearer',),                 # Tipe header untuk autentikasi JWT
    'USER_ID_FIELD': 'id',                            # ID field yang digunakan untuk mengambil informasi pengguna
    'USER_ID_CLAIM': 'user_id',                      # Klaim yang akan digunakan untuk menampilkan ID pengguna
}

# Email setting configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'a98da65b27c258'  # Email Anda
EMAIL_HOST_PASSWORD = '56daef68e5e3b0'  # Password Email Anda
