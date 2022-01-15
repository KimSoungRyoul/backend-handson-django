from typing import Any

from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from requests import Response
from rest_framework import viewsets
from rest_framework.request import Request

from study_example_app.models import Employee
from study_example_app.serializers.serializer_structure_analysis import EmployeeWithCustomDepartmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    print(settings.ROOT_URLCONF)
    pass


@extend_schema_view(
    notes=extend_schema(tags=["Doctor Appointments"], summary="Get appointment notes"),
)
class AppointmentViewSet(AppointmentViewSet):
    pass


@extend_schema_view(
    list=extend_schema(tags=["CustomDepartmentSerializer 예제"], summary=" 커스텀Serializer 구현 예제입니다."),
    retrieve=extend_schema(tags=["CustomDepartmentSerializer 예제"], summary=" 커스텀Serializer 구현 예제입니다."),
    create=extend_schema(tags=["CustomDepartmentSerializer 예제"], summary=" 커스텀Serializer 구현 예제입니다."),
    parital_update=extend_schema(tags=["CustomDepartmentSerializer 예제"], summary=" 커스텀Serializer 구현 예제입니다."),
    update=extend_schema(tags=["CustomDepartmentSerializer 예제"], summary=" 커스텀Serializer 구현 예제입니다."),
    destroy=extend_schema(tags=["CustomDepartmentSerializer 예제"], summary=" 커스텀Serializer 구현 예제입니다."),
)
class EmployeeWithCustomDepartmentViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeWithCustomDepartmentSerializer
