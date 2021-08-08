from __future__ import annotations

from django.contrib.auth.models import User
from rest_framework import serializers

from study_example_app.models import DjangoModel
from study_example_app.serializers.fields import MaskingDRFField


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        depth = 1
        fields = '__all__'


class DjangoModelSerializer(serializers.ModelSerializer[DjangoModel]):
    class Meta:
        model = DjangoModel
        fields = '__all__'
