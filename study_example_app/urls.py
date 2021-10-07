from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from study_example_app.views.chapter_05_views_example_views import StoreGenericViews
from study_example_app.views.example_views import ClassBasedView
from study_example_app.views.example_views import function_based_view_with_drf
from study_example_app.views.example_views import ninja_api
from study_example_app.views.example_views import OrderViewSet
from study_example_app.views.example_views import StoreViewSet
from study_example_app.views.example_views import UserClassBasedViewSet
from study_example_app.views.fbv_views import asdf
from study_example_app.views.fbv_views import create_order_function_view_to_learn_serializer
from study_example_app.views.fbv_views import modify_order_function_view_to_learn_serializer
from study_example_app.views.fbv_views import signup_function_view_to_learn_serializer


router = DefaultRouter()
router.register(prefix=r"users", viewset=UserClassBasedViewSet, basename="user")
router.register(prefix="stores", viewset=StoreViewSet, basename="store")
router.register(prefix="orders", viewset=OrderViewSet, basename="order")


urlpatterns = [
    path("fbv-drf/", function_based_view_with_drf, name="drf-fbv-example"),
    path("cbv-drf/", ClassBasedView.as_view()),
    path("store/<int:pk>/", StoreGenericViews.as_view(), name="store-retrieve"),
    # FBV의 단점을 보여주는 예시
    # path('users/',users_api),
    # learning api
    path("drf-api-examples/", include(router.urls)),
    path("ninja-api-examples/", ninja_api.urls),
    path("signup/", signup_function_view_to_learn_serializer, name="signup-api"),
    path("order/", create_order_function_view_to_learn_serializer, name="create-order-api"),
    path("order/<int:pk>/", modify_order_function_view_to_learn_serializer, name="modify-order-api"),

path("osdf/", asdf, name="mosdf"),

]
