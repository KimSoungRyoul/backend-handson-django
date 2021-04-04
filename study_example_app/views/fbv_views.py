import json
from typing import Any, Dict

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework.decorators import api_view


@require_http_methods(request_method_list=["GET", "POST"])
@csrf_exempt
def hello_django_fbv(request: WSGIRequest):
    request.GET["a_param"]  # "aa"
    request.GET["b_param"]  # "bb"
    request.method # "POST"
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
