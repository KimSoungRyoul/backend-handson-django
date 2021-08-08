""""
순수 Python3.7미만 버전을  사용해서 직렬화 하는 로직 작성하기
"""
from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional


class Organization:
    class OrganizationType(Enum):
        BUSINESS = "business"
        MANAGEMENT_SUPPORT = "management_support"
        TECHNOLOGY_RESEARCH = "technology_research"

    name: str = ""
    organization_type: OrganizationType = ""
    leader: Optional[User] = None


class User:
    username: str = ""
    password: str = ""
    email: str = ""
    name: str = ""
    age: int = -1
    is_superuser: bool = False
    created_at: str = None  # yyyy-mm-dd hh:MM:ss
    # created_at: datetime = None

    def __init__(
        self, username: str, password: str, email: str, name: str, age: int, is_superuser: bool,
    ):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.age = age
        self.is_superuser = is_superuser
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":

    user: User = User(
        username="soungryoul.kim0823",
        password="qwer1234!",
        name="김성렬",
        email="kimsoungryoul@gmail.com",
        age=37,
        is_superuser=False,
    )

    user_serializing_dict: Dict[str, Any] = user.__dict__
    print(f"Type: {type(user_serializing_dict)}", f"Data: {user_serializing_dict}")

    user_serializing_json: str = json.dumps(user_serializing_dict)
    print(f"Type: {type(user_serializing_json)}", f"Data: {user_serializing_json}")

    user_serializing_bytes: bytes = user_serializing_json.encode("utf-8")
    print(f"Type: {type(user_serializing_bytes)}", f"Data: {user_serializing_bytes}")

a = {
    "username": "soungryoul.kim0823",
    "password": "qwer1234!",
    "email": "kimsoungryoul@gmail.com",
    "name": "김성렬",
    "age": 37,
    "is_superuser": false,
    "created_at": "2021-08-08 22:36:16",
    "organization": {
        "name": "서버 개발1팀",
        "organization_type": "",
        "leader": {
            "username": "teamjang.kim0102",
            "password": "qwer1234!",
            "email": "",
            "name": "김팀장",
            "age": -1,
            "is_superuser": true,
            "created_at":"2021-04-08 12:45:18",
            "organization": null,
        },
    },
}
