from django.contrib.auth.models import User

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from chapter1_app.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
