from django.contrib.auth.models import User
from django.db import models
from rest_framework.fields import (
    BooleanField, CharField, DateField, DateTimeField, DecimalField, DurationField, EmailField, FileField, FilePathField, FloatField, IPAddressField, ImageField, IntegerField, ModelField, SlugField,
    TimeField, URLField, UUIDField,
)
from rest_framework.serializers import ModelSerializer

from study_example_app.models import AModel, MaskingField
from study_example_app.models import Bmodel
from study_example_app.models import DjangoModel
from study_example_app.serializers.fields import MaskingDRFField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = "__all__"


class DjangoModelSerializer(ModelSerializer):
    class Meta:
        model = DjangoModel
        fields = "__all__"


class BModelSerializer(ModelSerializer):
    class Meta:
        model = Bmodel
        fields = "__all__"


class VMSModelSerializer(ModelSerializer):
    serializer_field_mapping = {
        models.AutoField: IntegerField,
        models.BigIntegerField: IntegerField,
        models.BooleanField: BooleanField,
        models.CharField: CharField,
        models.CommaSeparatedIntegerField: CharField,
        models.DateField: DateField,
        models.DateTimeField: DateTimeField,
        models.DecimalField: DecimalField,
        models.DurationField: DurationField,
        models.EmailField: EmailField,
        models.Field: ModelField,
        models.FileField: FileField,
        models.FloatField: FloatField,
        models.ImageField: ImageField,
        models.IntegerField: IntegerField,
        models.NullBooleanField: BooleanField,
        models.PositiveIntegerField: IntegerField,
        models.PositiveSmallIntegerField: IntegerField,
        models.SlugField: SlugField,
        models.SmallIntegerField: IntegerField,
        models.TextField: CharField,
        models.TimeField: TimeField,
        models.URLField: URLField,
        models.UUIDField: UUIDField,
        models.GenericIPAddressField: IPAddressField,
        models.FilePathField: FilePathField,
        MaskingField: MaskingDRFField
    }



class AModelSerializer(VMSModelSerializer):

    # b_set = BModelSerializer(many=True)

    class Meta:
        model = AModel
        depth = 1
        fields = ("id", "a_field", "a_masking_field", "b_set")
