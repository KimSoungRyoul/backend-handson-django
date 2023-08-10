from custom_oauth2.views.origin_auth_views import (
    DRFIntrospectTokenViewSet,
    DRFRevokeTokenView,
    DRFTokenViewSet,
)
from custom_oauth2.views.social_auth_views import SocialAuthCallBackViewSet
from django import get_version
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.views.i18n import JavaScriptCatalog
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)
from frontend_demo.views import SignUpDemoTemplateView
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet

router = SimpleRouter(trailing_slash=False)
# router.register(prefix="oauth", viewset=TokenViewSet, basename="oauth")
router.register(prefix="users", viewset=UserViewSet, basename="users")
router.register(prefix="callback", viewset=SocialAuthCallBackViewSet, basename="callback")

# pycon2023App 자체 인증
custom_auth2_router = SimpleRouter(trailing_slash=False)
custom_auth2_router.register(prefix="token", viewset=DRFTokenViewSet, basename="token")
custom_auth2_router.register(prefix="revoke", viewset=DRFRevokeTokenView, basename="revoke")
custom_auth2_router.register(prefix="introspect", viewset=DRFIntrospectTokenViewSet, basename="introspection")

auth_url_patterns = [
    path("api/", include(router.urls), name="api"),
    path("api/oauth/", include(custom_auth2_router.urls), name="custom_oauth2"),
    path("demo-template/signup/", view=SignUpDemoTemplateView.as_view(), name="demo-signup")
    # re_path(r"^authorize/$", AuthorizationView.as_view(), name="authorize"),
    # re_path(r"^token/$", TokenView.as_view(), name="token"),
    # re_path(r"^revoke_token/$", RevokeTokenView.as_view(), name="revoke-token"),
    # re_path(r"^introspect/$", IntrospectTokenView.as_view(), name="introspect"),
    # re_path(
    #     r"^\.well-known/openid-configuration/$",
    #     ConnectDiscoveryInfoView.as_view(),
    #     name="oidc-connect-discovery-info",
    # ),
    # re_path(r"^\.well-known/jwks.json$", JwksInfoView.as_view(), name="jwks-info"),
    # re_path(r"^userinfo/$", UserInfoView.as_view(), name="user-info"),
]

admin_urlpatterns = [
    # User Admin
    path(
        "jsi18n/",
        cache_page(86400, key_prefix="jsi18n-%s" % get_version())(JavaScriptCatalog.as_view()),
        name="javascript-catalog",
    ),
    path("admin/", admin.site.urls),
    # path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    #  re_path(r"oauth-admin/$", ApplicationList.as_view(), name="list"),
    #  re_path(r"oauth-admin/applications/register/$", ApplicationRegistration.as_view(), name="register"),
    #  re_path(r"oauth-admin/applications/(?P<pk>[\w-]+)/$", ApplicationDetail.as_view(), name="detail"),
    #  re_path(r"oauth-admin/applications/(?P<pk>[\w-]+)/delete/$", ApplicationDelete.as_view(), name="delete"),
    #  re_path(r"oauth-admin/applications/(?P<pk>[\w-]+)/update/$", ApplicationUpdate.as_view(), name="update"),
    #  # Token management views
    #  re_path(r"oauth-admin/authorized-tokens/$", AuthorizedTokensListView.as_view(), name="authorized-token-list"),
    #  re_path(
    #      r"oauth-admin/authorized_tokens/(?P<pk>[\w-]+)/delete/$",
    #      AuthorizedTokenDeleteView.as_view(),
    #      name="authorized-token-delete",
    #  ),
]  # (OAuthProvider Admin)

docs_urlpatterns = [
    # Open API 문서
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    # Open API Document with UI:
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui"),
]

# path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
urlpatterns = auth_url_patterns + admin_urlpatterns
urlpatterns += docs_urlpatterns
# if settings.DEBUG:
#     urlpatterns += docs_urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
