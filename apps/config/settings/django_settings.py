import os
from pathlib import Path

import django_stubs_ext
import pymysql

pymysql.install_as_MySQLdb()

django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", True)

ALLOWED_HOSTS: list[str] = ["www.example.com", "localhost", "127.0.0.1"]

INSTALLED_APPS = [
    # djanog 기본앱
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 데모용 & Admin 커스터마이징
    "frontend_demo",
    "django.contrib.admin",
    # django
    "django_extensions",
    "django_mysql",
    "django_redis",
    # django-cors-headers
    "corsheaders",
    "oauth2_provider",
    # drf
    "rest_framework",
    "drf_spectacular",
    "storages",
    # Custom App
    "users",
    "custom_oauth2",
]


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

# django-storage S3
AWS_S3_REGION_NAME = os.getenv("AWS_REGION")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
STORAGES = {
    "default": {"BACKEND": "custom_oauth2.s3_custom_storage.MediaStorage"},
    "staticfiles": {"BACKEND": "custom_oauth2.s3_custom_storage.StaticStorage"},
}
AWS_S3_CUSTOM_DOMAIN = "d19rgr1je33tf4.cloudfront.net"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # cors-headers
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    #  "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/admin/login/"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            f"{os.getenv('REDIS_URL')}/0",
            # f"{os.getenv('REDIS_URL')}2",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},  # 실서버 운용시 더 높아야 합니다.
        },
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:9000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB_NAME"),
        "USER": os.getenv("MYSQL_DB_USER"),
        "PASSWORD": os.getenv("MYSQL_DB_PASSWORD"),
        "HOST": os.getenv("MYSQL_DB_HOST"),
        "PORT": os.getenv("MYSQL_DB_PORT"),
        "options": {
            "charset": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
            # "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "auth_plugin": "mysql_native_password",
        },
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# s3에 static/ media/ 업로드함 aws_settings.py 참고
STATIC_URL = "static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", default=os.path.join(BASE_DIR, STATIC_URL))
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#
# ]
MEDIA_URL = "media/"
MEDIA_ROOT = os.getenv("STATIC_ROOT", default=os.path.join(BASE_DIR, MEDIA_URL))


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# for django https config
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
