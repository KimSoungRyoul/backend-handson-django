from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "h^jz=pr_u0c&%b-@b9%=j93)t&mf_s&1h!w+mf*i$mm*ithp94"

DEBUG = True

ALLOWED_HOSTS: List[str] = []

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
    # 내가 만든 django app list
    "table_document_app",
    "aggregate.users",
    "aggregate.stores",
    "aggregate.orders",
    "aggregate.products",
    "user_management",
    "store_management",
    "django_app_name",
    # 교육용 snippet app
    "frontend_app",
    "study_example_app",
    "portfolio",
    "drf_example_app",
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
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        # 'rest_framework.authentication.SessionAuthentication',
    ],
}

SPECTACULAR_SETTINGS = {
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    "TITLE": "DjangoBackendProgramming 학습예제 API 문서",
    "DESCRIPTION": "[한빛 미디어] 주니어개발자를 위한 Django Backend Programming 실습예제 입니다.",
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
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@3.38.0",  # Swagger UI 버전을 조절할 수 있습니다. https://www.npmjs.com/package/swagger-ui-dist 해당 링크에서 최신버전을 확인후 취향에 따라 version을 수정해서 사용하세요.
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    # sqlite 를 DB로 사용하려면 주석처리를 해제하세요
    #  "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3",},
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
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django_db",
        "USER": "root",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": 3306,
    },
    "replica1": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django_db",
        "USER": "root",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": 3306,
    },
    "replica2": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django_db",
        "USER": "root",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": 3306,
    },
}
# DATABASE_ROUTERS = ['config.db_router.PrimaryReplicaRouter']

# https://docs.djangoproject.com/en/3.1/ref/settings/#sessions 자세한 정보는 여기서 확인할 수 있습니다. (공식문서를 잘 읽을줄 알아야 합니다.)
SESSION_COOKIE_AGE = 60 * 60 * 24  # 로그인시 세션의 만료시간은 1day default

# 세션 저장소(SessionStore)를 관계형 Database로 지정 Django의 default값
# 세션 저장소로 다음 3가지 값 중에 하나를 선택할 수 있습니다.
# 'django.contrib.sessions.backends.db'  # rdb(ex: mysql,postgres를 세션 저장소로 사용합니다)
# 'django.contrib.sessions.backends.file' # 임의 파일을 생성해서 세션 저장소로 사용합니다.
# 'django.contrib.sessions.backends.cache' # 메모리 DB (ex: redis)를 세션 저장소로 사용합니다. 실서버 운용시 가장 적절한 선택입니다.
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

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

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

# 이 세팅을 주석처리하면 console에 SQL 로그들이 출력되지 않습니다.
LOGGING = {
    "version": 1,
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {"console": {"level": "DEBUG", "filters": ["require_debug_true"], "class": "logging.StreamHandler"}},
    "loggers": {"django.db.backends": {"level": "DEBUG", "handlers": ["console"]}},
}

AES256_ENCRYPTION_KEY = b"d40e150996e5e6c10f08ba4efab746a3"
SEED256_ENCRYPTION_KEY = b"bd9fc900714c1f94"
