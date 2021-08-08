from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularYAMLAPIView
from rest_framework.routers import DefaultRouter

from frontend_app.views import MainPageTemplateView
from study_example_app.views import DjangoModelViewSet
from user_management.views import UserViewSet

router = DefaultRouter()

# router.register(r'users', UserViewSet, basename='user')
router.register(r'djang-models', DjangoModelViewSet, basename='django_model')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('study-example-app/', include('study_example_app.urls')),
    path('admin/', admin.site.urls),
    # Open API 문서 소스코드 형태
    path('docs/json/', SpectacularJSONAPIView.as_view(), name='schema-json'),
    path('docs/yaml/', SpectacularYAMLAPIView.as_view(), name='swagger-yaml'),
    path('', MainPageTemplateView.as_view(), name='frontend_main_page'),
    # Open API Document UI 형태:
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema-json'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema-json'), name='redoc'),
]
