from django.db.models import TextChoices


class OAS3Tag(TextChoices):
    PyCon2023Auth = "PyCon2023Auth (자체 인증서버 인증)", "던라이큰 자체 인증 OAuth2 APIs"
    SocialAuth = "SocialAuth (외부 인증) Kakao, Naver", "소셜인증 API (Kakao, Naver)"
    PyCon2023User = "PyCon2023User (자체 인증서버 회원가입,수정,조회)", "자체 인증서버 회원CRUD"
