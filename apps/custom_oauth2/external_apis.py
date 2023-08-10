import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, DefaultDict

import httpx


@dataclass
class SocialUserInfo:
    social_uuid: str
    name: str
    nickname: str
    profile_image_url: str
    thumbnail_image_url: str
    email: str
    birthday: str


class KakaoHttpx:
    @staticmethod
    def retrieve_uuid(access_token: str) -> int:
        header = {
            f"Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        query_params = {"secure_resource": True, "property_keys": json.dumps(["id"])}
        res = httpx.get(
            url="https://kapi.kakao.com/v2/user/me",
            headers=header,
            params=query_params,
        )
        return res.json()["id"]

    # AAAAO7SxMjvTRSsSu2gs8Y3HjCR9R1bU0Q_R1Gn0m1ZKhpdf8XFdZpyLpO6KpM2udFoHiNaxrnkUZBRO-1jAWrAaW3Q
    @staticmethod
    def retrieve_social_info(access_token: str) -> SocialUserInfo:
        res = httpx.get(
            url="https://kapi.kakao.com/v2/user/me",
            headers={
                f"Authorization": f"Bearer {access_token}",
            },
            params={
                "secure_resource": True,
            },
        )
        data: DefaultDict[str, Any] = defaultdict(
            str,
            res.json(),
        )

        kakao_user = SocialUserInfo(
            social_uuid=data["id"],
            name=data["properties"].get("name") or data["properties"]["nickname"],
            nickname=data["properties"]["nickname"],
            profile_image_url=data["properties"]["profile_image"],
            thumbnail_image_url=data["properties"]["thumbnail_image"],
            email=data["kakao_account"]["email"],
            birthday=data["kakao_account"]["birthday"],
        )

        return kakao_user


# https://kapi.kakao.com/v2/user/me 응답Response 예시 포맷
# res.json() == {
#     "id": 2231780621,
#     "connected_at": "2022-05-07T07:40:02Z",
#     "properties": {
#         "nickname": "김성렬",
#         "profile_image": "http://k.kakaocdn.net/dn/bjakte/btrbQa4I0uh/I5tH3kPl4e4iXC191BZg5K/img_640x640.jpg",
#         "thumbnail_image": "http://k.kakaocdn.net/dn/bjakte/btrbQa4I0uh/I5tH3kPl4e4iXC191BZg5K/img_110x110.jpg",
#     },
#     "kakao_account": {
#         "profile_nickname_needs_agreement": False,
#         "profile_image_needs_agreement": False,
#         "profile": {
#             "nickname": "김성렬",
#             "thumbnail_image_url": "http://k.kakaocdn.net/dn/bjakte/btrbQa4I0uh/I5tH3kPl4e4iXC191BZg5K/img_110x110.jpg",
#             "profile_image_url": "http://k.kakaocdn.net/dn/bjakte/btrbQa4I0uh/I5tH3kPl4e4iXC191BZg5K/img_640x640.jpg",
#             "is_default_image": False,
#         },
#         "has_email": True,
#         "email_needs_agreement": False,
#         "is_email_valid": True,
#         "is_email_verified": True,
#         "email": "bluesky1356@kakao.com",
#         "has_birthday": True,
#         "birthday_needs_agreement": False,
#         "birthday": "0823",
#         "birthday_type": "SOLAR",
#     },
# }


class NaverHttpx:
    @staticmethod
    def retrieve_social_info(access_token: str) -> str:
        res = httpx.get(
            url="https://openapi.naver.com/v1/nid/me",
            headers={
                f"Authorization": f"Bearer {access_token}",
            },
        )
        return res.json()["response"]["id"]

    @staticmethod
    def retrieve_social_info(access_token: str) -> SocialUserInfo:
        res = httpx.get(
            url="https://openapi.naver.com/v1/nid/me",
            headers={
                f"Authorization": f"Bearer {access_token}",
            },
        )
        # 네이버 예시 포맷
        # res.json() == {
        #   'resultcode': '00',
        #   'message': 'success',
        #   'response': {
        #       'id': 'swoO2OWiNg4KNsUdkvByk_OV02oQepPGAOgBsrlwpio',
        #       'profile_image': 'https://phinf.pstatic.net/contact/20200222_249/1582358709327QcGkN_PNG/avatar_profile.png',
        #       'email': 'KimSoungRyoul@gmail.com',
        #       'name': '김성렬'
        #       }
        #   }
        data: DefaultDict[str, Any] = defaultdict(
            str,
            res.json()["response"],
        )

        naver_user = SocialUserInfo(
            social_uuid=data["id"],
            name=data["name"] or data["nickname"],
            nickname=data["nickname"],
            profile_image_url=data["profile_image"],
            thumbnail_image_url=data["profile_image"],
            email=data["email"],
            birthday=data["birthday"],
        )
        return naver_user
