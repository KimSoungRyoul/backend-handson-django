from typing import Any, Final

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, serializers, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import User

USER_TAG: Final[str] = "회원"


class UserSchema(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


@extend_schema_view(
    list=extend_schema(tags=[USER_TAG]),
    retrieve=extend_schema(tags=[USER_TAG]),
    create=extend_schema(tags=[USER_TAG]),
    update=extend_schema(tags=[USER_TAG]),
    destroy=extend_schema(tags=[USER_TAG]),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSchema
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response(data=[{"qqq": "qqq"}])

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response(data={"": ""})
