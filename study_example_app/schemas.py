from drf_spectacular.utils import OpenApiExample

USER_CREATE_QUERY_PARAM_EXAMPLES = [
    OpenApiExample(
        "이것은 Query Parameter Example입니다.",
        summary="short optional summary1",
        description="longer description",
        value="1993-08-23",
    ),
    OpenApiExample(
        "이것은 Query Parameter Example2입니다.",
        summary="short optional summary2",
        description="longer description",
        value="1993-08-23",
    ),
    OpenApiExample(
        "이것은 Query Parameter Example3입니다.",
        summary="short optional summary3",
        description="longer description",
        value="1993-08-23",
    ),
]

USER_CREATE_EXAMPLES = [
    OpenApiExample(
        name="success_example",
        value={
            "username": "root",
            "password": "django_1234",
            "first_name": "성렬",
            "last_name": "김",
            "email": "user@example.com",
        },
    ),
    OpenApiExample(
        request_only=True,
        summary="비밀번호 너무 쉬움 예제",
        name="invalid_example1",
        value={
            "username": "root23",
            "password": "1234",
            "first_name": "성렬",
            "last_name": "김",
            "email": "user@example.com",
        },
    ),
    OpenApiExample(
        request_only=True,
        summary="이름 필수 입력 예제",
        name="invalid_example2",
        value={
            "username": "root434",
            "password": "django_1234",
            "first_name": "성렬",
            "last_name": "김",
            "email": "user@example.com",
        },
    ),
    OpenApiExample(
        response_only=True,
        name="success_example2",
        value={
            "username": "root434",
            "password": "django_1234",
            "first_name": "성렬",
            "last_name": "김",
            "email": "user@example.com",
        },
    ),
]
