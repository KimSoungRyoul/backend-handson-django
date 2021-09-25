from __future__ import annotations

from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from study_example_app.models import DjangoModel
from study_example_app.serializers.fields import MaskingDRFField


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        depth = 1
        fields = "__all__"


class DjangoModelSerializer(serializers.ModelSerializer[DjangoModel]):
    class Meta:
        model = DjangoModel
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[UnicodeUsernameValidator, UniqueValidator])
