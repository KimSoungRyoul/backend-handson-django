from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import views
from rest_framework.response import Response


class BBAPIView(views.APIView):

    def get(self, request, format=None):
        return Response(data={"get":"sdfsdf"})

    def post(self, request, format=None):
        return Response(data={"qqq":"sdfsdf"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("room/", view=BBAPIView.as_view())
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # type: ignore[arg-type]
