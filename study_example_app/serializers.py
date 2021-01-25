from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from study_example_app.models import AModel
from study_example_app.models import Bmodel
from study_example_app.models import DjangoModel


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = '__all__'


class DjangoModelSerializer(ModelSerializer):
    class Meta:
        model = DjangoModel
        fields = '__all__'

class BModelSerializer(ModelSerializer):
    class Meta:
        model = Bmodel
        fields = '__all__'

class AModelSerializer(ModelSerializer):

   # b_set = BModelSerializer(many=True)

    class Meta:
        model = AModel
        depth=1
        fields = ('id','a_field','b_set')
