from django.urls import path

from study_example_app.views.chapter_05_views_example_views import StoreGenericViews
from study_example_app.views.drf_views import ClassBasedView
from study_example_app.views.drf_views import function_based_view_with_drf

urlpatterns = [
    path("fbv-drf/", function_based_view_with_drf),
    path("cbv-drf/", ClassBasedView.as_view()),
    path("store/<int:pk>/", StoreGenericViews.as_view(), name="store-retrieve"),
    # FBV의 단점을 보여주는 예시
    # path('users/',users_api),
]
