from django.contrib.auth.models import User
from django.views.generic import ListView


class UserListView(ListView):
    queryset = User.objects.all()
