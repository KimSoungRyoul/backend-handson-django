REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "custom_oauth2.authentication.PyCon2023AppOAuthAuthentication",
        # "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        # "rest_framework.authentication.BasicAuthentication",
    ),
    # "DEFAULT_AUTHENTICATION_CLASSES": ("oauth2_provider.contrib.rest_framework.OAuth2Authentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
# TokenAuthentication
# OAuth2Authentication

OAUTH2_PROVIDER_APPLICATION_MODEL = "custom_oauth2.RegisteredApplication"
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = "custom_oauth2.JWTAccessToken"
OAUTH2_PROVIDER_GRANT_MODEL = "custom_oauth2.Grant"
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = "custom_oauth2.RedisRefreshToken"
OAUTH2_PROVIDER_ID_TOKEN_MODEL = "custom_oauth2.IDToken"


OAUTH2_PROVIDER = {
    # this is the list of available scopes
    "SCOPES": {"read": "Read scope", "write": "Write scope", "admin": "use admin page"},
    # OAuth2 Toolkit
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.JSONOAuthLibCore",
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 60,
    "ACCESS_TOKEN_MODEL": "custom_oauth2.JWTAccessToken",
    "REFRESH_TOKEN_MODEL": "custom_oauth2.RedisRefreshToken",
    "GRANT_MODEL": "custom_oauth2.Grant",
    "APPLICATION_MODEL": "custom_oauth2.RegisteredApplication",
    "ID_TOKEN_MODEL": "custom_oauth2.IDToken",
    "ACCESS_TOKEN_GENERATOR": "custom_oauth2.core.custom_token_generator",
    "ACCESS_TOKEN_ALGORITHM": "HS256",
    "ACCESS_TOKEN_SIGNING_KEY": "pf15cfiN1WuyyWzOJcjx2If26mkp6ig3tYElWgTvvfU",
    "ACCESS_TOKEN_EXPIRE_SECONDS": 36000,  # 1 hours
    "REFRESH_TOKEN_REDIS_KEY_PREFIX": "refresh_token",
    "REFRESH_TOKEN_GENERATOR": "custom_oauth2.core.custom_refresh_token_generator",
    "REFRESH_TOKEN_EXPIRE_SECONDS": 60 * 60 * 24 * 7,  # 1 week
    "REFRESH_TOKEN_GRACE_PERIOD_SECONDS": 0,
    "ROTATE_REFRESH_TOKEN": True,
    "ERROR_RESPONSE_WITH_SCOPES": False,
    "OAUTH2_SERVER_CLASS": "custom_oauth2.core.DRFOAuth2Server",
    "OAUTH2_VALIDATOR_CLASS": "custom_oauth2.oauth2_validators.PyCon2023AppOAuth2Validator",
    "ID_TOKEN_EXPIRE_SECONDS": 36000,
    "APPLICATION_ADMIN_CLASS": "custom_oauth2.admin.RegisteredApplicationAdmin",
}

SPECTACULAR_SETTINGS = {
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    "TITLE": "PYCON2023APPken Auth Server API Doc",
    "DESCRIPTION": "OAuth2 인증서버 JWT",
    # Optional: MAY contain "name", "url", "email"
    "CONTACT": {"name": "김성렬", "url": "http://www.example.com/support", "email": "KimSoungRyoul@gmail.com"},
    # Swagger UI를 좀더 편리하게 사용하기위해 기본옵션들을 수정한 값들입니다.
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,  # API를 클릭할때 마다 SwaggerUI의 url이 변경됩니다. (특정 API url 공유시 유용하기 때문에 True설정을 사용합니다)
        "persistAuthorization": True,  # True 이면 SwaggerUI상 Authorize에 입력된 정보가 새로고침을 하더라도 초기화되지 않습니다.
        "displayOperationId": True,  # True인 경우 API의 urlId 값을 노출합니다. 대체로 DRF api name둘과 일치하기때문에 api를 찾을때 유용합니다.
        "filter": True,  # True 이면 Swagger UI에서 'Filter by Tag' 검색이 가능합니다
    },
    # "SWAGGER_UI_OAUTH2_CONFIG": {
    #     "clientId": "your-client-id",
    #     "clientSecret": "your-client-secret-if-required",
    #     "appName": "your-app-name",
    #     "scopeSeparator": " ",
    #     "scopes": "read write groups",
    #     "useBasicAuthenticationWithAccessCodeGrant": True,
    # },
    # Optional: MUST contain "name", MAY contain URL
    "LICENSE": {
        "name": "MIT License",
        "url": "https://github.com/KimSoungRyoul",
    },
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # OAS3 Meta정보 API를 비노출 처리합니다.
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@4.10.3",  # Swagger UI 버전을 조절할 수 있습니다. https://www.npmjs.com/package/swagger-ui-dist 해당 링크에서 최신버전을 확인후 취향에 따라 version을 수정해서 사용하세요.
    "OAUTH2_FLOWS": ["password", "authorizationCode"],
    # "OAUTH2_AUTHORIZATION_URL": "/api/authorize/",
    "OAUTH2_TOKEN_URL": "/api/oauth/token",
    "OAUTH2_REFRESH_URL": "api/oauth/token",
    "OAUTH2_SCOPES": ["read:sdf", "write:sdf", "groups:dsf"],
}

# curl -X POST -d "grant_type=password&username=root&password=1234" -u"Vz4Smiq8mJFEPstbywoa0U3qrpjuQA5V6HfOFyl7:ZPT8qfoz1qdJPoSPlFQBblLYbeT5Vvs4sOL4YPLgQHpaF61PrzOYsnwtAEg0h5K85mkTVFrXF4n4phN7DyYZW6Vayf3bAt0wh0BbNJEIXBGfICXuj5LpyDHQsy1RrWmG" http://localhost:8080/o/token/
