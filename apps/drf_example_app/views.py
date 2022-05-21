from typing import Any

from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from drf_example_app.models import University
from drf_example_app.schemas import UNIVERSITY_SCHEMA_PARAMETERS
from drf_example_app.serializers import UniversitySchema


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySchema
    pagination_class = PageNumberPagination

    @extend_schema(tags=["대학교"], summary="리스트 조회 요약 description....", )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    @extend_schema(tags=["대학교"], summary="생성 요약 description....")
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(tags=["대학교"], summary="수정 요약 description ....")
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
