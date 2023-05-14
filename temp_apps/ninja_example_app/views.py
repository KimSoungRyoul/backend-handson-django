import json
from datetime import date, datetime, time, timedelta
from typing import Any, Dict

from aggregate.stores.models import Store
from django.core.handlers.wsgi import WSGIRequest
from django.forms import model_to_dict
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja import Schema as NinjaSchema
from ninja.renderers import JSONRenderer
from ninja.responses import NinjaJSONEncoder
from pydantic.json import pydantic_encoder
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class CustomJSONEncoder(NinjaJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime(format=DATETIME_FORMAT)
        elif isinstance(o, date):
            ...
        elif isinstance(o, time):
            ...
        elif isinstance(o, timedelta):
            ...

        return pydantic_encoder(o)


class MyJsonRenderer(JSONRenderer):
    encoder_class = CustomJSONEncoder


ninja_api = NinjaAPI(title="django Ninja API 예시", renderer=MyJsonRenderer())


class HelloResponseSchema(NinjaSchema):
    aa_datetime: datetime

    class Config(NinjaSchema.Config):
        json_encoders = {
            datetime: lambda v: v.strftime(format="%Y-%m-%d %H:%M:%S"),
        }


@ninja_api.get("/aaa")
def api_aaa(request: WSGIRequest):
    return 200, HelloResponseSchema(aa_datetime=datetime.now())


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
