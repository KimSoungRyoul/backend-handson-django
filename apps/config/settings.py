import os
from datetime import timedelta
from pathlib import Path
from typing import List

import django_stubs_ext

django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "h^jz=pr_u0c&%b-@b9%=j93)t&mf_s&1h!w+mf*i$mm*ithp94"

DEBUG = True

ALLOWED_HOSTS: List[str] = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "channels",
    # "daphne",
    "django_extensions",

    # 커스텀 djagno DB 구현체
    "django_dynamodb",

    # 사용하는 예시 django App
    "sample_app",
]
# AUTH_USER_MODEL = "django.contrib.auth.models.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    #  "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # "ENGINE": "psqlextra.backend", django-postgres-extra 라이브러리 사용시 교체
        "NAME": "django_db",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    },
    "dynamodb": {
        "ENGINE": "django_dynamodb.backends.dynamodb",
        # "ENGINE": "psqlextra.backend", django-postgres-extra 라이브러리 사용시 교체
        "NAME": "django_db",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    },
}

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

# 현 프로젝트에서 session 방식은 사용하지 않습니다. 하지만 학습을 위해 주석처리상태로 남겨놓습니다.
# https://docs.djangoproject.com/en/4.2/ref/settings/#sessions 자세한 정보는 여기서 확인할 수 있습니다.
# SESSION_COOKIE_AGE = 60 * 60 * 24  # 로그인시 세션의 만료시간은 1day default

# 세션 저장소(SessionStore)로 공식문서에 5가지로 언급되어있지만 일반적인 상황에서는 2가지 중 하나를 선택하면 됩니다.
# (https://docs.djangoproject.com/en/4.2/ref/settings/#session-engine)
# SESSION_ENGINE = "django.contrib.sessions.backends.db" # 1. rdb(ex: mysql,postgres를 세션 저장소로 사용합니다)
# SESSION_ENGINE = "django.contrib.sessions.backends.cached_db" # 2. 메모리 DB (ex: redis)를 세션 저장소로 사용합니다. 실서버 운용시 가장 적절한 선택입니다.


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# CHANNEL 은 입문용이 아니라서 주석처리
# CHANNEL_LAYERS = {
#     "default": {"BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": {"hosts": [("127.0.0.1", 6379)]}},
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images) (swagger, redoc static file)
STATIC_URL = "static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", default=os.path.join(BASE_DIR.parent, STATIC_URL))

# LOGGING 전체를 주석처리하면 django가 제공하는 기본(default) logging 정책을 사용합니다.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # 학습 목적으로 제가 임의로 정의한 log 포맷입니다.
        "common": {
            "format": "{levelname} {asctime} 로그 찍은 곳: {name} pid: {process:d} thread-id: {thread:d} \n  --> {message}\n",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "common",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        # ---sql 로그를 보고싶지 않다면 "django.db.backends" 항목을 주석처리하세요---
        # "django.db.backends": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        # },
        # --------------------------------------------------------------
    },
}
