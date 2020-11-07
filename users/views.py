from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
