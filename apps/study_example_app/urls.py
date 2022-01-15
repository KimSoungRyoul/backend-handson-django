from django.urls import include
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

# from study_example_app.views.example_views import OrderViewSet
# from study_example_app.views.example_views import StoreViewSet
# from study_example_app.views.example_views import UserClassBasedViewSet

router = DefaultRouter()
# router.register(prefix=r"users", viewset=UserClassBasedViewSet, basename="user")
# router.register(prefix="stores", viewset=StoreViewSet, basename="store")
# router.register(prefix="orders", viewset=OrderViewSet, basename="order")


# views.py
@api_view(http_method_names=["GET"])
def user_show_list_function_view(request, *args, **kwargs):
    ...
    # Function View에 원하는 로직 작성
    return Response(data={"": "sdf"})


@api_view(http_method_names=["GET"])
def user_show_detail_function_view22(request: Request, user_pk: int, *args, **kwargs):
    print("이 View Function이 매핑되어있는 http URL입니다: ", request.path)
    print("user_pk: ", user_pk, type(user_pk))
    return Response(data="success")


# urls.py
from django.urls import path

#  path(route="", view=.., name="")
#  router :  http url을 정의하는 곳이다.


urlpatterns = [
    path(
        route="users/detail/<slug:user_pk>/", view=user_show_detail_function_view22, name="user-detail-api"
    ),  # 회원 상세 조회
]

# urls.py
# urlpatterns = [
#
#     path("fbv-drf/", function_based_view_with_drf, name="drf-fbv-example"),
#     path("cbv-drf/", ClassBasedView.as_view()),
#     path("store/<int:pk>/", StoreGenericViews.as_view(), name="store-retrieve"),
#     # FBV의 단점을 보여주는 예시
#     # path('users/',users_api),
#     # learning api
#     path("drf-api-examples/", include(router.urls)),
#
#     path("signup/", signup_function_view_to_learn_serializer, name="signup-api"),
#     path("order/", create_order_function_view_to_learn_serializer, name="create-order-api"),
#     path("order/<int:pk>/", modify_order_function_view_to_learn_serializer, name="modify-order-api"),
#
#     path("osdf/", asdf, name="mosdf"),
#
# ]
