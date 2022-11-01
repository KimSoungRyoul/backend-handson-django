from typing import Any

from aggregate.orders.models import Order
from aggregate.products.serializers import OrderSerializer
from aggregate.stores.models import Store
from aggregate.stores.serializers import StoreSerializer
from aggregate.users.models import User
from aggregate.users.serializers import UserSerializer
from django.db import transaction
from django.forms import model_to_dict
from drf_spectacular.utils import extend_schema, extend_schema_view
from ninja import NinjaAPI
from rest_framework import generics, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

ninja_api = NinjaAPI()


@ninja_api.get("/stores")
def store_list_api(request):
    # 상점 목록을 조회하는 코드 개발자가 직접구현
    return 200, list(Store.objects.all())


@ninja_api.get("stores/{pk}")
def store_retrieve_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    store = Store.objects.get(id=pk)
    return 200, model_to_dict(store)


@ninja_api.post("/stores")
def store_create_api(request):
    # 상점을 생성하는 코드 개발자가 직접 구현
    return 200, {"detail": "상점 생성이 완료됐습니다."}


@ninja_api.put("stores/{pk}")
def store_partial_update_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    return 200, {"detail": "상점 일부정보 수정이 완료됐습니다."}


@ninja_api.patch("stores/{pk}")
def store_partial_update_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    return 200, {"detail": "상점정보 수정이 완료됐습니다."}


@ninja_api.delete("stores/{pk}")
def store_partial_update_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    return 200, {"detail": "상점 삭제가 완료됐습니다."}


@api_view(http_method_names=["GET"])
def function_based_view_with_drf(request: Request) -> Response:
    request.query_params["a_param"]  # "aa"
    request.query_params["b_param"]  # "bb"
    request.path  # "/drf-fbv"
    request.headers["Content-Type"]  # "application/json"
    request.content_type  # "application/json"
    request.data  # {"message": "hello DRF FBV"}

    if request.method == "GET":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "FBV GET 응답입니다."})
    elif request.method == "POST":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "FBV POST 응답입니다."})

    return Response(data={"message": "그 이외 http method 입니다."})


class ClassBasedView(APIView):
    def get(self, request: Request, *args, **kwargs):
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "CBV GET응답입니다."})

    def post(self, request: Request, *args, **kwargs):
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "CBV POST응답입니다."})


from rest_framework import mixins, viewsets


@extend_schema_view(
    list=extend_schema(tags=["학습용 예제 APIs"], summary="회원 목록 조회"),
    create=extend_schema(tags=["학습용 예제 APIs"], summary="회원 가입"),
    partial_update=extend_schema(tags=["학습용 예제 APIs"], summary="회원 정보 수정"),
    update=extend_schema(tags=["학습용 예제 APIs"], summary="회원 정보 일괄 수정"),
)
class UserClassBasedViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 회원 정보 관련 모든 API들은 로그인하지 않으면 사용할수 없도록 권한 제약을 부여
    # permission_classes = [
    #     IsAuthenticated,
    # ]


class StoreViewSet(viewsets.GenericViewSet):
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ...
        return Response({"detail": "상점 생성이 완료됐습니다."})

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ...

        return Response({"detail": "상점 생성이 완료됐습니다."})

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ...

        return Response({"detail": "상점 생성이 완료됐습니다."})

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ...

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ...

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ...


class GenericAPIViewExampleView(generics.GenericAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def list(self, request: Request, *args, **kwargs) -> Response:

        return Response(data={"message": "GenericAPIView GET응답입니다."})


@api_view(http_method_names=["GET", "POST"])
def users_api(request):
    if request.method == "GET":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "User GET 응답입니다."})
    elif request.method == "POST":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "User POST 응답입니다."})

    return Response(data={"message": "그 이외 http method 입니다."})


@api_view(http_method_names=["GET", "PATCH", "PUT", "DELETE"])
def users_detail_api(request: Request):

    if request.method == "GET":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "User GET 응답입니다."})
    elif request.method == "PATCH":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "User PATCH 응답입니다."})
    elif request.method == "PUT":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "User PUT 응답입니다."})
    elif request.method == "DELETE":
        # API 동작에 필요한 로직 작성....
        return Response(data={"message": "User DELETE 응답입니다."})

    return Response(data={"message": "그 이외 http method 입니다."})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("product_set").all()
    serializer_class = OrderSerializer

    @extend_schema(summary="주문 상세 조회 API", tags=["주문"])
    # @transaction.atomic(using="replica1")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(summary="주문 생성 API", tags=["주문"])
    @transaction.atomic(using="default")
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(url_path="approval", detail=True, methods=["PATCH"])
    def approval(self, request: Request, *args, **kwargs):
        ...

    @action(url_path="delivery-platform", detail=True, methods=["PATCH"])
    def delivery_platform(self, request: Request, *args, **kwargs):
        ...

    @action(url_path="delivery", detail=True, methods=["POST"])
    def delivery(self, request: Request, *args, **kwargs):
        ...


#
# class UserAPIView(APIView):
#     authentication_classes = ...
#     permission_classes = ...
#
#
# class OrderAPIView(APIView):
#     authentication_classes = ...
#     permission_classes = ...
