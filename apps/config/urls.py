from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # type: ignore[arg-type]
