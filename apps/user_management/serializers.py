from typing import Any, Dict

from aggregate.users.models import Department, Staff, User
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault


class UserQueryParamSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=User.UserStatus.choices,
        error_messages={"invalid_choice": "올바른 상태값을 입력해주세요."},
    )
    user_type = serializers.ChoiceField(
        choices=User.UserType.choices,
        error_messages={"invalid_choice": "존재하지 않는 고객 유형입니다."},
    )


class DepartmentField(serializers.CharField):
    def to_internal_value(self, data: str) -> Department:
        try:
            parent1_name, parent2_name, parent3_name = data.split(">")
        except ValueError:
            raise serializers.ValidationError({"department": " 조직은 반드시 'A>B>C' 포맷을 가져야 합니다."})

        try:
            department = Department.objects.get(
                parent1_name=parent1_name,
                parent2_name=parent2_name,
                parent3_name=parent3_name,
            )
        except Department.DoesNotExist:
            raise serializers.ValidationError({"department": f"{data}는 존재하지 않는 조직입니다."})

        return department

    def to_representation(self, value: Department) -> str:
        return str(value)


class MaskingField(serializers.CharField):
    def to_internal_value(self, data: str) -> str:


        return data

    def to_representation(self, value: str) -> str:
        # from django.contrib.auth.models import AnonymousUser
        if self.context.get("request") is not None:
            current_logined_user = self.context["request"].user
        else:
            current_logined_user = AnonymousUser
        if (
            current_logined_user is not AnonymousUser
            and current_logined_user.user_type == User.UserType.STAFF.value
        ):
            return value
        if not value:
            return value

        self.context[f"unmasking_{self.field_name}"] = value  # 혹시 모르니 원본 데이터 context에 저장
        return value[0] + "*" * len(value[1:])


class StaffSchema(serializers.ModelSerializer):
    department = DepartmentField(help_text="소속 부서")
    name_kor = MaskingField(help_text="조회하는 회원이 직원이 아니라면 개인정보를 볼수없도록 마스킹처리 됩니다.")

    def create(self, validated_data: Dict[str, Any]) -> Staff:
        staff = Staff.objects.create_user(
            username=validated_data["username"],
            is_superuser=False,  # 고정값, 외부에서 주는값에 의해 수정되면 안됨
            is_staff=True,  # 고정값, 외부에서 주는값에 의해 수정되면 안됨
            password=validated_data["password"],
            email=validated_data["email"],
            name_kor=validated_data["name_kor"],
            department=validated_data["department"],
        )
        return staff

    def update(self, instance: Department, validated_data: Dict[str, Any]) -> Staff:
        validated_data.pop("is_superuser",None)  # 고정값, 외부에서 주는값에 의해 수정되면 안됨
        validated_data.pop("is_staff",None)  # 고정값, 외부에서 주는값에 의해 수정되면 안됨

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Staff
        fields = ("id", "username", "is_superuser", "password", "is_staff", "department", "email", "name_kor")
        extra_kwargs = {"password": {"write_only": True}}
        depth = 1


class StaffDetailSchema(StaffSchema):
    class Meta(StaffSchema.Meta):
        fields = "__all__"
