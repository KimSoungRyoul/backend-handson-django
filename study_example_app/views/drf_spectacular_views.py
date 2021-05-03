from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from  rest_framework import viewsets


class AppointmentViewSet(viewsets.ModelViewSet):
    print(settings.ROOT_URLCONF)
    pass




@extend_schema_view(
    notes=extend_schema(tags=["Doctor Appointments"], summary="Get appointment notes"),

)
class AppointmentViewSet(AppointmentViewSet):
    pass