from rest_framework import serializers

from drf_example_app.models import University


class UniversitySchema(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"
