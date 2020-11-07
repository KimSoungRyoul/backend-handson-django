from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView, SpectacularSwaggerView, SpectacularYAMLAPIView
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user")


urlpatterns = [

    path("", include(router.urls)),

    path("admin/", admin.site.urls),

    # YOUR PATTERNS
    path("api/docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("api/docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    # Optional UI:
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger-ui",
    ),

    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema-json"),
        name="redoc",
    ),

]
