from django.urls import path

from study_example_app.views.drf_views import ClassBasedView
from study_example_app.views.drf_views import function_based_view_with_drf

urlpatterns = [
    path('fbv-drf/', function_based_view_with_drf),

    path('cbv-drf/', ClassBasedView.as_view()),

    # FBV의 단점을 보여주는 예시
    path('users/',users_api),
]
