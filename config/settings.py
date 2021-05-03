import os
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "h^jz=pr_u0c&%b-@b9%=j93)t&mf_s&1h!w+mf*i$mm*ithp94"

DEBUG = True

ALLOWED_HOSTS: List[str] = []

# Application definition

INSTALLED_APPS = [
    "channels",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "rest_framework",
    "drf_yasg",
    "django_filters",
    "django_extensions",
    "drf_spectacular",
    "frontend_app",
    "study_example_app",
    "shopping_mall",
    "social_django",
]


AUTH_USER_MODEL = "shopping_mall.ShoppingMallUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    #'django.middleware.csrf.CsrfViewMiddleware', # api 방식개발에는 거의 사용되지 않는 django 기본 Middleware다.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M:%S",
}

SPECTACULAR_SETTINGS = {
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    "TITLE": "drf-spectacular API Document",
    "DESCRIPTION": "### i am description",
    # Optional: MAY contain "name", "url", "email"
    "CONTACT": {"name": "김성렬", "url": "http://www.example.com/support", "email": "KimSoungRyoul@gmail.com"},
    # Swagger UI를 좀더 편리하게 사용하기위해 기본옵션들을 수정한 값들입니다.
    "SWAGGER_UI_SETTINGS": {
        "dom_id": "#swagger-ui",  # required(default)
        "layout": "BaseLayout",  # required(default)
        "deepLinking": True,  # API를 클릭할때 마다 SwaggerUI의 url이 변경됩니다. (특정 API url 공유시 유용하기때문에 True설정을 사용합니다)
        "persistAuthorization": True,  # True 이면 SwaggerUI상 Authorize에 입력된 정보가 새로고침을 하더라도 초기화되지 않습니다.
        "displayOperationId": True,  # True이면 API의 urlId 값을 노출합니다. 대체로 DRF api name둘과 일치하기때문에 api를 찾을때 유용합니다.
        "filter": True,  # True 이면 Swagger UI에서 'Filter by Tag' 검색이 가능합니다
    },
    # Optional: MUST contain "name", MAY contain URL
    "LICENSE": {
        "name": "MIT License",
        "url": "https://github.com/KimSoungRyoul/DjangoBackendProgramming/blob/main/LICENSE",
    },
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # OAS3 Meta정보 API를 비노출 처리합니다.
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@3.38.0",  # Swagger UI 버전을 조절할수 있습니다.
    # https://www.npmjs.com/package/swagger-ui-dist 해당 링크에서 최신버전을 확인후 취향에 따라 version을 수정해서 사용하세요.
    "CAMELIZE_NAMES": True,
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3",},
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'django_db',
    #     'USER': 'postgres',
    #     'PASSWORD': '1234',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    # },
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "django_db",
    #     "USER": "root",
    #     "PASSWORD": "1234",
    #     "HOST": "127.0.0.1",
    #     "PORT": "3306",
    # },
}

# 공식문서를 잘 읽을줄 알아야합니다.
# https://docs.djangoproject.com/en/3.1/ref/settings/#sessions 자세한 정보는 여기서 확인할 수 있습니다.
SESSION_COOKIE_AGE = 60 * 60 * 24  # 로그인시 세션의 만료시간은 1day default
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # 세션 저장소를 관계형 Database로 지정 Django의 default값


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
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": {"hosts": [("127.0.0.1", 6379)]}},
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# 날짜 국제화 관련 옵션입니다.

# 해당 옵션에 따라 django가 제공하는 기본 언어가 변경됩니다.
# ex: 에러메시지와 django-admin가 기본언어로 한글을 사용함
LANGUAGE_CODE = "ko-kr"


# UTC TimeZone 옵션 자체를 사용할지 말지를 정합니다. False인경우 python datetime()객체의 사용이 자유로워지나, 서버의 물리적인 위치를 고려해야함
# ex: USE_TZ=False 상태에서 django App을 AWS EC2 미국에 배포한경우 datetime.now()는 미국의 현재시간을 저장한다.
USE_TZ = True

# DB에 저장된 UTC 시간 값을 django가 해당 지역의 시간으로 변환해서 보여줍니다.
TIME_ZONE = "Asia/Seoul"


USE_I18N = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# django에서 발생하는 모든 SQL들을 console에 로깅해줍니다. 주로 개발할때 사용하는 옵션입니다.
# LOGGING = {
#     "version": 1,
#     "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue",}},
#     "handlers": {"console": {"level": "DEBUG", "filters": ["require_debug_true"], "class": "logging.StreamHandler",}},
#     "loggers": {"django.db.backends": {"level": "DEBUG", "handlers": ["console"],}},
# }
