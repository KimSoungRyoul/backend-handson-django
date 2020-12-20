from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)
from rest_framework.routers import DefaultRouter

from chapter1_app.views import UserViewSet

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    # Open API 문서 소스코드 형태
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    # Open API Document UI 형태:
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger-ui",
    ),
    path(
        "docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema-json"),
        name="redoc",
    ),
]
