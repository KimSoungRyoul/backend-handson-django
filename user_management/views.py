from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from aggregate.users.models import User
from aggregate.users.serializers import UserSerializer
from user_management.serializers import UserQueryParamSerializer
# Create your views here.


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request:Request, *args, **kwargs):
        qp_serializer = UserQueryParamSerializer(data=request.query_params)
        qp_serializer.is_valid(raise_exception=True)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
