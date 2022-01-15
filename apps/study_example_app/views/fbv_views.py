import json
from typing import Any
from typing import Dict

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from aggregate.orders.models import Order
from study_example_app.serializers.serializer_structure_analysis import EmployeeSerializer
from study_example_app.serializers.serializer_structure_analysis import OrderWriteOnlySerializer
from study_example_app.serializers.serializer_structure_analysis import SignUpSerializer


@require_http_methods(request_method_list=["GET", "POST"])
@csrf_exempt
def hello_django_fbv(request: WSGIRequest):
    request.GET["a_param"]  # "aa"
    request.GET["b_param"]  # "bb"
    request.method  # "POST"
    request.path  # "/django-fbv/"
    request.headers["Content-Type"]  # "application/json"
    request.body  # b'{\n"message":"hello Django FBV"\n}'
    dict_data: Dict[Any, Any] = json.loads(request.body)

    return HttpResponse(content="<h1> Hello Django FBV </h1>")


from rest_framework.request import Request
from rest_framework.response import Response


@api_view(http_method_names=["GET", "POST"])
def hello_drf_fbv(request: Request):
    request.query_params["a_param"]  # "aa"
    request.query_params["b_param"]  # "bb"
    request.path  # "/drf-fbv/"
    request.headers["Content-Type"]  # "application/json"
    request.data  # {"message":"Hello DRF FBV"}
    return Response(data={"message": "Bye DRF FBV"})


@extend_schema(
    tags=["학습용 예제 APIs"],
    summary="Serializer 학습용 회원가입 API",
    request=SignUpSerializer,
    examples=[
        OpenApiExample(
            name="일반적인 패킷 예시",
            value={
                "username": "hello_django2020",
                "password": "qwer1234!",
                "first_name": "Pointer",
                "last_name": "Kim",
                "name_kor": "김점순",
                "phone": "010-1234-5555",
            },
        ),
        OpenApiExample(
            name="잘못된 패킷 예시1",
            value={
                "username": "hello_django2020",
                "password": "qwer1234!",
                "first_name": "Pointer",
                "last_name": "Kim",
                "name_kor": "김점순",
                "phone": "01012345555",
            },
        ),
    ],
)
@api_view(http_method_names=["POST"])
def signup_function_view_to_learn_serializer(request: Request):
    request_body: dict[str, Any] = request.data

    signup_serializer = SignUpSerializer(data=request_body)
    signup_serializer.is_valid(raise_exception=True)
    signup_serializer.save()

    return Response(data={"detail": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["학습용 예제 APIs"],
    summary="Serializer 학습용 주문 생성 API",
    request=OrderWriteOnlySerializer,
    examples=[
        OpenApiExample(
            name="일반예제1",
            value={"store_id": 1, "orderedproduct_set": [{"count": 2, "product": 1}, {"count": 3, "product": 2}]},
        ),
    ],
)
@api_view(http_method_names=["POST"])
def create_order_function_view_to_learn_serializer(request: Request):
    serializer = OrderWriteOnlySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(data={"detail": "주문접수가 완료됐습니다.", "order": serializer.data}, status=status.HTTP_201_CREATED)

    # from rest_framework.generics import get_object_or_404
    # 이 함수는 찾는 instance가 존재하지 않는경우 알아서 ValidationError를 일으켜준다.
    # try:
    #    order = Order.objects.get(pk=pk)
    # except Order.DoesNotExist:
    #    return Response(data={"detail":"존재하지 않는 주문번호입니다"}, status=status.HTTP_404_NOT_FOUND)
    # 이렇게 작성해야하는 4줄을 단 한줄로 줄일수있는 편리한 함수이기때문에 활용 빈도가 매우 높다.


@extend_schema(
    tags=["학습용 예제 APIs"],
    summary="Serializer 학습용 주문 수락 거절 API",
    request=OrderWriteOnlySerializer,
    examples=[
        OpenApiExample(name="주문 수락", value={"status": "accepted"}),
        OpenApiExample(name="주문 거절", value={"status": "rejected"}),
    ],
)
@api_view(http_method_names=["PATCH"])
def modify_order_function_view_to_learn_serializer(request: Request, pk):

    instance: Order = get_object_or_404(queryset=Order.objects.all(), pk=pk)
    before_status = instance.status
    serializer = OrderWriteOnlySerializer(data=request.data, instance=instance, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        data={"detail": f"주문 상태값이 {before_status}->{serializer.data['status']}로 변경됐습니다."},
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["학습용 예제 APIs"],
    summary="Serializer 학습용 asdfsdff",
    request=EmployeeSerializer,
)
@api_view(http_method_names=["POST"])
def asdf(request):
    e = EmployeeSerializer(data=request.data)
    e.is_valid(raise_exception=True)
    e.save()
    return Response(data={})
