from drf_spectacular.contrib.rest_framework_jwt import JWTScheme as _JWTScheme
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView as _TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as _TokenRefreshView

AUTH_TAG = ["Authentication"]


@extend_schema_view(
    post=extend_schema(
        tags=[AUTH_TAG],
        examples=[
            OpenApiExample(
                "Login Sample",
                description="""
            you would create user first
            python apps/manage.py createsuperuser --username=root --email=kimsoungryoul@gmail.com
            """,
                value={
                    "username": "root",
                    "password": "1234",
                },
            ),
        ],
        summary="Login API (get JWT Token)",
    ),
)
class TokenObtainPairView(_TokenObtainPairView):
    ...


@extend_schema_view(
    post=extend_schema(tags=[AUTH_TAG], summary="Refresh Token API"),
)
class TokenRefreshView(_TokenRefreshView):
    ...
