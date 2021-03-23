from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from study_example_app.models import DjangoModel
from study_example_app.serializers.fields import MaskingDRFField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = '__all__'


class DjangoModelSerializer(ModelSerializer):
    class Meta:
        model = DjangoModel
        fields = '__all__'
