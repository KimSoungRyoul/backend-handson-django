from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)
from rest_framework.routers import DefaultRouter
from sample_app.views import ContractViewSet, StoreViewSet
from sample_app.views.authentication import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(prefix="stores", viewset=StoreViewSet, basename="store")
router.register(prefix="contracts", viewset=ContractViewSet, basename="contract")
# router.register(prefix="others", ...)


urlpatterns = [
    # authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # REST
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    # API Document
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="schema-yaml"),
    # Open API Document with UI:
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema-yaml"), name="swagger-ui-default"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-yaml"), name="redoc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
