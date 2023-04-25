from drf_example_app.models import University
from rest_framework import serializers


class UniversitySchema(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"
