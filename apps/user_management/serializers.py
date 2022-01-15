from rest_framework import serializers

from aggregate.users.models import User


class UserQueryParamSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=User.UserStatus.choices,
        error_messages={"invalid_choice": "올바른 상태값을 입력해주세요."},
    )
    user_type = serializers.ChoiceField(
        choices=User.UserType.choices,
        error_messages={"invalid_choice": "존재하지 않는 고객 유형입니다."},
    )
