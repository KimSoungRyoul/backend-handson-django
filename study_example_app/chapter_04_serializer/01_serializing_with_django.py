""""
순수 Python3.7미만 버전을  사용해서 직렬화 하는 로직 작성하기
"""
from __future__ import annotations

import dataclasses
import json
from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms import model_to_dict
from rest_framework.renderers import JSONRenderer


class Organization(models.Model):
    class OrganizationType(models.TextChoices):
        BUSINESS = "business", "경영"
        MANAGEMENT_SUPPORT = "management_support", "경영지원"
        TECHNOLOGY_RESEARCH = "technology_research", "기술개발"

    name: str = models.CharField(max_length=32)
    organization_type = models.CharField(choices=OrganizationType.choices)
    leader: Optional[User] = models.ForeignKey(to="User", on_delete=models.CASCADE)


class User(models.Model):
    username: str = models.CharField(default="", max_length=32)
    password: str = models.CharField(default="", max_length=128)
    email: str = models.CharField(default="", max_length=32)
    name: str = models.CharField(default="", max_length=32)
    age: int = models.IntegerField(default=-1)
    is_superuser: bool = models.BooleanField(default=False)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    organization: Optional[Organization] = models.ForeignKey(to=Organization, on_delete=models.CASCADE)


# 실제 수행은 안됩니다.
if __name__ == "__main__":

    user: User = User(
        username="soungryoul.kim0823",
        password="qwer1234!",
        name="김성렬",
        email="kimsoungryoul@gmail.com",
        age=37,
        is_superuser=False,
        organization=Organization(
            name="서버 개발1팀", leader=User(username="teamjang.kim0102", password="qwer1234!", name="김팀장"),
        ),
    )
    JSONRenderer
    user_serializing_dict = model_to_dict(user)

    print(f"Type: {type(user_serializing_dict)}", f"Data: {user_serializing_dict}")

    user_serializing_json: str = json.dumps(user_serializing_dict, cls=DjangoJSONEncoder)
    print(f"Type: {type(user_serializing_json)}", f"Data: {user_serializing_json}")

    user_serializing_bytes: bytes = user_serializing_json.encode("utf-8")
    print(f"Type: {type(user_serializing_bytes)}", f"Data: {user_serializing_bytes}")
