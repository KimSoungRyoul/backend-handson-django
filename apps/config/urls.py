from django.contrib import admin
from django.urls import include, path
from drf_example_app.views import UniversityViewSet, example_api, login_example_api
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)
from frontend_app.views import MainPageTemplateView
from ninja_example_app.views import ninja_api
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from store_management.views import AGenericView, ProductViewSet, StoreViewSet, drf_fbv
from study_example_app.views.drf_spectacular_views import (
    EmployeeWithCustomDepartmentViewSet,
)
from study_example_app.views.example_views import OrderViewSet
from table_document_app.views import db_schema_docs_template_view
from user_management.views import StaffViewSet, UserViewSet

router = DefaultRouter()

# router.register(r'users', UserViewSet, basename='users')
router.register(prefix=r"users", viewset=UserViewSet, basename="user")
router.register(
    prefix=r"employees-with-custom-department",
    viewset=EmployeeWithCustomDepartmentViewSet,
    basename="employee-with-custom-department",
)
router.register(prefix="universites", viewset=UniversityViewSet, basename="university")
router.register(prefix="products", viewset=ProductViewSet, basename="product")
# router.register(prefix="stores", viewset=StoreViewSet, basename="store")
# router.register(prefix="orders", viewset=OrderViewSet, basename="order")
router.register(prefix="staffs", viewset=StaffViewSet, basename="staff")


@api_view(http_method_names=["GET"])
def asdf(request: Request, username, *args, **kwargs):
    return Response(data={"sdfsdf": username})


urlpatterns = [
    path("ninja-api/", ninja_api.urls),
    path("asdf/<slug:username>/", view=asdf, name="asdf-api"),
    path("api/", include(router.urls)),
    path("api-example/login/", view=login_example_api, name="login-example-api"),
    path("api/exception-handler-example/", view=example_api, name="exception-handler-examplei"),
    path("store11/", view=AGenericView.as_view(), name="generic_api_view1"),
    path("store22/", view=drf_fbv, name="generic_api_view2"),
    path("study-example-app/", include("study_example_app.urls")),
    path("admin/", admin.site.urls),
    # Open API 문서
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    path("", MainPageTemplateView.as_view(), name="frontend_main_page"),
    # Open API Document with UI:
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc"),
    # asdf
    path("docs/db-schema/", view=db_schema_docs_template_view, name="db-schema-docs-template-view"),
]
