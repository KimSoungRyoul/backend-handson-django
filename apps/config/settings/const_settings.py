from os import getenv
from types import SimpleNamespace

PYCON2023APP_AUTH = SimpleNamespace(
    client_id=getenv("PYCON2023APP_CLIENT_ID"),
    secret=getenv("PYCON2023APP_CLIENT_SECRET"),
    redirect_url=getenv("PYCON2023APP_REDIRECT_URL"),
)

KAKAO_AUTH = SimpleNamespace(
    client_id=getenv("KAKAO_CLIENT_ID", ""),
    secret=getenv("KAKAO_SECRET", ""),
    redirect_url=getenv("KAKAO_REDIRECT_URL", ""),
)

NAVER_AUTH = SimpleNamespace(
    client_id=getenv("NAVER_CLIENT_ID", ""),
    secret=getenv("NAVER_CLIENT_SECRET", ""),
    redirect_url=getenv("NAVER_REDIRECT_URL", ""),
)
