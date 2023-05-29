from authentication.views import (
    AuthLoginAPIView,
    AuthRefreshAPIView,
    AuthTokenBlacklistView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django_ninja_sample.views import ninja_api
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)
from orders.views import OrderViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from stores.views import ContractViewSet, StoreViewSet
from users.views import UserViewSet

router = DefaultRouter()

router.register(prefix=r"users", viewset=UserViewSet, basename="user")
# router.register(prefix="products", viewset=ProductViewSet, basename="product")
router.register(prefix="stores", viewset=StoreViewSet, basename="store")
router.register(prefix="orders", viewset=OrderViewSet, basename="order")

store_nested_router = NestedDefaultRouter(router, "stores", lookup="store")
store_nested_router.register(prefix="contracts", viewset=ContractViewSet, basename="contract")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(store_nested_router.urls)),
    # authentication
    path("api/token/", AuthLoginAPIView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", AuthRefreshAPIView.as_view(), name="token_refresh"),
    path("api/token/blacklist/", AuthTokenBlacklistView.as_view(), name="token_blacklist"),
    path("admin/", admin.site.urls),
    # Open API 문서
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    # Open API Document with UI:
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui-default"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc"),
    # ninja sample
    path("ninja-api/", ninja_api.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
