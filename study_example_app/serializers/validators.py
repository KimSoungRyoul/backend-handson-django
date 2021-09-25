import re

from rest_framework import serializers


class KoreanOnlyValidator:
    message = "{attr_name} 은 한글만 사용가능합니다."

    def __init__(self, message=None):
        if message:
            self.message = message

    def __call__(self, value: str, serializer_field):
        if not re.match(r"^[가-힣]+$", value):
            raise serializers.ValidationError(detail=self.message.format(attr_name=serializer_field.name))


class EnglishOnlyValidator:
    message = "{attr_name} 은 한글,숫자,특수문자가 포함되면 안됩니다."

    def __init__(self, message=None):
        if message:
            self.message = message

    def __call__(self, value: str, serializer_field):
        if value.isalpha():
            raise serializers.ValidationError(detail=self.message.format(attr_name=serializer_field.name))
