from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularYAMLAPIView
from rest_framework.routers import DefaultRouter

from chapter1_app.views import UserViewSet
from frontend_app.views import MainPageTemplateView

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    # Open API 문서 소스코드 형태
    path('docs/json/', SpectacularJSONAPIView.as_view(), name='schema-json'),
    path('docs/yaml/', SpectacularYAMLAPIView.as_view(), name='swagger-yaml'),
    path('', MainPageTemplateView.as_view(), name='frontend_main_page'),
    # Open API Document UI 형태:
    path(
        'docs/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema-json'),
        name='swagger-ui',
    ),
    path(
        'docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema-json'),
        name='redoc',
    ),
]
