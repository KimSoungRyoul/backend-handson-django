from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class MainPageTemplateView(TemplateView):
    template_name = "pages/dashboard/dashboard.html"
