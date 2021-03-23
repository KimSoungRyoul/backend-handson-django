from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


@api_view(http_method_names=['GET', 'POST'])
def function_based_view_with_drf(request: Request):
    if request.method == 'GET':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'FBV GET 응답입니다.'})
    elif request.method == 'POST':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'FBV POST 응답입니다.'})


class ClassBasedView(APIView):
    def get(self, request: Request, *args, **kwargs):
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'CBV GET응답입니다.'})

    def post(self, request: Request, *args, **kwargs):
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'CBV POST응답입니다.'})


@api_view(http_method_names=['GET', 'POST'])
def users_api(request):
    if request.method == 'GET':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'User GET 응답입니다.'})
    elif request.method == 'POST':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'User POST 응답입니다.'})


@api_view(http_method_names=['GET', 'PATCH', 'PUT', 'DELETE'])
def users_detail_api(request):
    if request.method == 'GET':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'User GET 응답입니다.'})
    elif request.method == 'PATCH':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'User PATCH 응답입니다.'})
    elif request.method == 'PUT':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'User PUT 응답입니다.'})
    elif request.method == 'DELETE':
        # API 동작에 필요한 로직 작성....
        return Response(data={'message': 'User DELETE 응답입니다.'})


class UserAPIView(APIView):
    authentication_classes = ...
    permission_classes = ...


class OrderAPIView(APIView):
    authentication_classes = ...
    permission_classes = ...
