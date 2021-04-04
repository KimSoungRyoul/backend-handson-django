from django.contrib.auth.models import User
from django.http import HttpResponse
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from study_example_app.models import AModel
from study_example_app.models import DjangoModel
from study_example_app.serializers import AModelSerializer
from study_example_app.serializers import DjangoModelSerializer
from study_example_app.serializers import UserSerializer


@extend_schema(tags=["A모델"])
class AModelViewSet(ModelViewSet):
    queryset = AModel.objects.all()
    serializer_class = AModelSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        summary="asdfsadff",
        examples=[
            OpenApiExample(
                request_only=True,
                name="success_example",
                value={
                    "username": "root",
                    "password": "django_1234",
                    "last_login": "2021-01-02T14:24:44.160Z",
                    "is_superuser": True,
                    "first_name": "성렬",
                    "last_name": "김",
                    "email": "user@example.com",
                    "is_staff": True,
                    "is_active": True,
                    "date_joined": "2021-01-02T14:24:44.160Z",
                    "groups": [0],
                    "user_permissions": [0],
                },
            ),
        ],
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        response: HttpResponse = super().create(request, *args, **kwargs)

        return response


class DjangoModelViewSet(ModelViewSet):
    queryset = DjangoModel.objects.all()
    serializer_class = DjangoModelSerializer
