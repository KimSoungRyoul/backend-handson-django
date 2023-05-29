from django.db import models

# 인증 로직의 경우
# 대부분 rest_framework_simplejwt 의 구현체(ex: RefreshToken ,Token)를 사용하였기 때문에
# 우리가 커스텀하게 다시 구현해줘야할 model 들이 없습니다.
# 궁금하면 from rest_framework_simplejwt.tokens import RefreshToken ,Token 의 모델이
# 어떻게 구현되어있는지 확인해보시면 학습에 도움이될 수 있습니다.
