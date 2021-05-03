from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularYAMLAPIView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from frontend_app.views import MainPageTemplateView
from study_example_app.views import DjangoModelViewSet, UserViewSet, hello_django_fbv, hello_drf_fbv

router = DefaultRouter()
router.register(prefix="users", viewset=UserViewSet, basename="users")
router.register(prefix="django-model", viewset=DjangoModelViewSet, basename="django-model")


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path("api/", include(router.urls)),
    path('study-example-app/', include('study_example_app.urls')),
    path("admin/", admin.site.urls),
    # Open API 문서 소스코드 형태
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    path("", MainPageTemplateView.as_view(), name="frontend_main_page"),
    # Open API Document UI 형태:
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui",),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc",),
    path("django-fbv/", view=hello_django_fbv, name="hello-django-fbv"),
    path("drf-fbv/", view=hello_drf_fbv, name="hello-drf-fbv"),



    # drf-yasg
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
