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
from django.forms import model_to_dict
from rest_framework.utils.encoders import JSONEncoder


@dataclasses.dataclass
class Organization:
    class OrganizationType(Enum):
        BUSINESS = "business"
        MANAGEMENT_SUPPORT = "management_support"
        TECHNOLOGY_RESEARCH = "technology_research"

    name: str = ""
    organization_type: OrganizationType = ""
    leader: Optional[User] = None


@dataclasses.dataclass
class User:
    username: str = dataclasses.field(default="")
    password: str = dataclasses.field(default="")
    email: str = dataclasses.field(default="")
    name: str = dataclasses.field(default="")
    age: int = dataclasses.field(default=-1)
    is_superuser: bool = dataclasses.field(default=False)
    created_at: datetime = dataclasses.field(default_factory=datetime.now)
    organization: Optional[Organization] = dataclasses.field(default=None)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(obj, Organization):
            return obj.__dict__
        return super().default(obj)


dictionary_data = {"나는datetime객체": datetime.now(), "나는time객체": time(11, 34), "나는date객체": date(2020, 8, 22)}
JSONEncoder
model_to_dict()
print(json.dumps(dictionary_data, cls=DjangoJSONEncoder))

print(json.dumps(dictionary_data, cls=CustomJSONEncoder))

if __name__ == "__main__":

    user: User = User(
        username="soungryoul.kim0823",
        password="qwer1234!",
        name="김성렬",
        email="kimsoungryoul@gmail.com",
        age=37,
        is_superuser=False,
        organization=Organization(
            name="서버 개발1팀",
            leader=User(username="teamjang.kim0102", password="qwer1234!", name="김팀장"),
        ),
    )

    user_serializing_dict: Dict[str, Any] = dataclasses.asdict(user)
    print(f"Type: {type(user_serializing_dict)}", f"Data: {user_serializing_dict}")

    user_serializing_json: str = json.dumps(user_serializing_dict, cls=CustomJSONEncoder)
    print(f"Type: {type(user_serializing_json)}", f"Data: {user_serializing_json}")

    user_serializing_bytes: bytes = user_serializing_json.encode("utf-8")
    print(f"Type: {type(user_serializing_bytes)}", f"Data: {user_serializing_bytes}")
