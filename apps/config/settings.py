import os
from datetime import timedelta
from pathlib import Path
from typing import List

import django_stubs_ext

django_stubs_ext.monkeypatch()


try:
    import pymysql

    pymysql.version_info = (1, 4, 3, "final", 0)
    pymysql.install_as_MySQLdb()

except Exception:
    ...

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
    "rest_framework",
    "django_extensions",
    "drf_spectacular",
    "django_filters",
    "channels",
    # "daphne",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "ninja",
    # 내가 만든 django app list
    "authentication",
    "users",
    "stores",
    "orders",
    "products",
    "django_ninja_sample",
]

AUTH_USER_MODEL = "users.User"
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

REST_FRAMEWORK = {
    # 프로젝트내 DRF 관련 공통 Config 입니다.
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",  # DRF의 모든 DatetimeField(format="~~~~") 는 이 포맷으로 직렬화됩니다.
    # "DATE_FORMAT" : "%Y-%m-%d" # 위와 마찬가지로 DateField(format="~~~") 또한 공통 Config가 가능합니다.
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        # 'rest_framework.authentication.SessionAuthentication', session 인증 대신 jwt를 사용합니다.
    ],
}

SPECTACULAR_SETTINGS = {
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    "TITLE": "백엔드 개발을 위한 핸즈온 장고  학습예제 API 문서",
    "DESCRIPTION": "[한빛 미디어] 백엔드 개발을 위한 핸즈온 장고 실습예제 입니다.",
    # Optional: MAY contain "name", "url", "email"
    "CONTACT": {"name": "김성렬", "url": "http://www.example.com/support", "email": "KimSoungRyoul@gmail.com"},
    # Swagger UI를 좀더 편리하게 사용하기위해 기본옵션들을 수정한 값들입니다.
    "SWAGGER_UI_SETTINGS": {
        "dom_id": "#swagger-ui",  # required(default)
        "layout": "BaseLayout",  # required(default)
        "deepLinking": True,  # API를 클릭할때 마다 SwaggerUI의 url이 변경됩니다. (특정 API url 공유시 유용하기 때문에 True설정을 사용합니다)
        "persistAuthorization": True,  # True 이면 SwaggerUI상 Authorize에 입력된 정보가 새로고침을 하더라도 초기화되지 않습니다.
        "displayOperationId": True,  # True인 경우 API의 urlId 값을 노출합니다. 대체로 DRF api name둘과 일치하기때문에 api를 찾을때 유용합니다.
        "filter": True,  # True 이면 Swagger UI에서 'Filter by Tag' 검색이 가능합니다
    },
    # Optional: MUST contain "name", MAY contain URL
    "LICENSE": {
        "name": "MIT License",
        "url": "https://github.com/KimSoungRyoul/DjangoBackendProgramming/blob/main/LICENSE",
    },
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # OAS3 Meta정보 API를 비노출 처리합니다.
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@4.19.0",
    # Swagger UI 버전을 조절할 수 있습니다. https://www.npmjs.com/package/swagger-ui-dist 해당 링크에서 최신버전을 확인후 취향에 따라 version을 수정해서 사용하세요.
}

# Database
DATABASES = {
    # sqlite 를 DB로 사용하려면 주석처리를 해제하세요
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    },
    # postgres를 DB로 사용하려면 주석처리를 해제하세요
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "django_db",
    #     "USER": "postgres",
    #     "PASSWORD": "1234",
    #     "HOST": "127.0.0.1",
    #     "PORT": "5432",
    # },
    # mysql를 DB로 사용하려면 주석처리를 해제하세요.
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "django_db",
    #     "USER": "root",
    #     "PASSWORD": "password",
    #     "HOST": "127.0.0.1",
    #     "PORT": 3306,
    # },
}


# 현 프로젝트에서 session 방식은 사용하지 않습니다. 하지만 학습을 위해 주석처리상태로 남겨놓습니다.
# https://docs.djangoproject.com/en/4.2/ref/settings/#sessions 자세한 정보는 여기서 확인할 수 있습니다.
# SESSION_COOKIE_AGE = 60 * 60 * 24  # 로그인시 세션의 만료시간은 1day default

# 세션 저장소(SessionStore)로 공식문서에 5가지로 언급되어있지만 일반적인 상황에서는 2가지 중 하나를 선택하면 됩니다.
# (https://docs.djangoproject.com/en/4.2/ref/settings/#session-engine)
# SESSION_ENGINE = "django.contrib.sessions.backends.db" # 1. rdb(ex: mysql,postgres를 세션 저장소로 사용합니다)
# SESSION_ENGINE = "django.contrib.sessions.backends.cached_db" # 2. 메모리 DB (ex: redis)를 세션 저장소로 사용합니다. 실서버 운용시 가장 적절한 선택입니다.


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

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

AES256_ENCRYPTION_KEY = b"d40e150996e5e6c10f08ba4efab746a3"
SEED256_ENCRYPTION_KEY = b"bd9fc900714c1f94"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.AuthTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "authentication.serializers.AuthTokenBlacklistSerializer",
}
