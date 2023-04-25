from datetime import date
from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.validators import UniqueValidator

from aggregate.orders.models import Order
from aggregate.orders.models import OrderedProduct
from aggregate.products.serializers import OrderedProductSerializer
from aggregate.stores.models import Store
from aggregate.stores.serializers import StoreSerializer
from aggregate.users.models import User
from study_example_app.models import Company, Department1
from study_example_app.models import Employee
from study_example_app.serializers.validators import EnglishOnlyValidator
from study_example_app.serializers.validators import KoreanOnlyValidator


class SignUpSerializer(serializers.Serializer):
    """
    validation 로직을 설명하기 위한 학습용 Serializer
    """

    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text="회원 아이디",
    )
    password = serializers.CharField(
        min_length=8,
        max_length=128,
        required=True,
        allow_blank=False,
        allow_null=False,
        # default="default value", required옵션과 default 옵션은 함께 사용할수 없습니다.(둘중 하나만 사용해야함)
        error_messages={
            "required": "이 필드는 반드시 필요합니다.",
            "invalid": "올바르지 않은 데이터 타입 입니다.",
            "blank": "이 필드는 비어있으면 안됩니다",
            "null": "이 필드는 null일수 없습니다.",
            "max_length": "이 필드는 문자열 길이를 최대 {max_length}까지만 사용할 수 있습니다. ",
            "min_length": "이 필드는 문자열 길이는 최소 {min_length}이상이여야 합니다.",
        },
    )

    first_name = serializers.CharField(max_length=128, help_text="회원 이름(Eng)", validators=[EnglishOnlyValidator()])
    last_name = serializers.CharField(max_length=128, help_text="회원 성(Eng)", validators=[EnglishOnlyValidator()])
    name_kor = serializers.CharField(max_length=128, help_text="회원 성함", validators=[KoreanOnlyValidator()])

    phone = serializers.CharField(
        max_length=16,
        help_text="휴대폰번호",
        validators=[RegexValidator(regex=r"\d{3}-\d{3,4}-\d{4}$", message="올바른 휴대폰 번호 포맷이 아닙니다. 다시 입력해주세요.")],
    )

    def is_valid(self, raise_exception):
        """
        Serializer하위 모든 validation로직을 수행하는 메서드
        """
        return super().is_valid(raise_exception)

    def validate_first_name(self, attr: str) -> str:
        # 이름에는 알파벳만 사용되었는지 검사하고 이름에 들어간 공백을 제거한다.
        if not attr.isalpha():
            raise serializers.ValidationError(detail="first_name은 한글,숫자,특수문자가 포함되면 안됩니다.")
        return attr.strip()

    def validate_last_name(self, attr: str) -> str:
        # 성에 알파벳만 사용되었는지 검사하고 성에 들어간 공백을 제거한다.
        if not attr.isalpha():
            raise serializers.ValidationError(detail="last_name은 한글,숫자,특수문자가 포함되면 안됩니다.")
        return attr.strip()

    def validate_password(self, attr: str) -> str:
        # password의 복잡도 검사를 수행한다.
        validate_password(password=attr)
        return attr

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        개발자가 추가로 Validation 해주고 싶은 로직이 있다면 validate() 메서드를 오버라이딩 해서 작성한다.
        """

        # Field 수준 또는 객체 수준의 단순Validation 아니라 비지니스 레벨에서 걸리는 Validation들은 이곳에 작성한다.
        if User.objects.filter(date_joined__gte=date.today()).count() > 100:
            raise serializers.ValidationError(
                detail="서비스 정책에 의해 하루에 선착순 100명까지만 회원가입이 가능합니다.\
                                                      내일 다시 회원가입해주세요.",
            )
        return attrs

    def create(self, validated_data: dict[str, Any]) -> object:
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            name_kor=validated_data["name_kor"],
            phone=validated_data["phone"],
        )
        return user

    def to_representation(self, instance) -> dict[str, Any]:
        """
        Class를 Dictionary로 변환
        """
        return super().to_representation(instance)

    def to_internal_value(self, data: dict[str, Any]) -> object:
        """
        Dictionary를 Class로 변환
        """
        return super().to_internal_value(data)

    class Meta:
        validators = [
            # 회원가입한 회원은 이름+전화번호가 고유해야한다.
            UniqueTogetherValidator(queryset=User.objects.all(), fields=["first_name", "last_name", "phone"]),
        ]


class OrderReadOnlySerializer(serializers.Serializer):
    total_price = serializers.IntegerField(read_only=True, help_text="해당 필드는 역정규화 필드임으로 API외부에서 계산된 값을 사용하지 않는다.")
    store = StoreSerializer(read_only=True)
    orderedproduct_set = OrderedProductSerializer(many=True, read_only=True, help_text="주문한 상품과 갯수 목록")


class OrderWriteOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(choices=Order.Status.choices, required=False)
    aaa = serializers.DateTimeField()
    total_price = serializers.IntegerField(read_only=True, help_text="해당 필드는 역정규화 필드임으로 API외부에서 계산된 값을 사용하지 않는다.")
    store_id = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all(), source="store", help_text="주문이 접수된 가게")
    orderedproduct_set = OrderedProductSerializer(many=True, help_text="주문한 상품과 갯수 목록")

    def validate_aaa(self, attr):
        return attr

    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> Order:
        orderedproduct_data_list: list[dict[str, Any]] = validated_data["orderedproduct_set"]
        total_price = sum(map(lambda od: od["count"] * od["product"].price, orderedproduct_data_list))

        instance = Order.objects.create(store=validated_data["store"], total_price=total_price)
        instance.orderedproduct_set.bulk_create(
            objs=[
                OrderedProduct(order=instance, product=od_data["product"], count=od_data["count"])
                for od_data in orderedproduct_data_list
            ],
        )
        return instance

    @transaction.atomic
    def update(self, instance: Order, validated_data: dict[str, Any]) -> Order:
        instance.status = validated_data["status"]
        instance.save()
        return instance


class CompanySerializer(serializers.Serializer):
    name = serializers.CharField()
    company_number = serializers.CharField()


class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    company = CompanySerializer()
    is_deleted = serializers.BooleanField()
    birth_date = serializers.DateField(format="%Y-%m-%d")
    employment_period = serializers.FloatField(help_text="재직 기간 ex: 3.75년")
    programming_language_skill = serializers.ListField(child=serializers.CharField())
    department1 = serializers.PrimaryKeyRelatedField(queryset=Department1.objects.all())

    def create(self, validated_data: dict[str, Any]) -> Employee:
        print(validated_data["name"])
        print(validated_data["age"])
        print(validated_data["company"])
        print(validated_data["is_deleted"])
        print(validated_data["birth_date"])
        print(validated_data["employment_period"])
        print(validated_data["programming_language_skill"])
        print(validated_data["department1"])

        return Employee.objects.first()


class CustomRelatedField(serializers.PrimaryKeyRelatedField):
    default_error_messages = {
        "required": "해당 필드는 반드시 필요합니다.",
        "does_not_exist": " department1(pk={pk_value})는 존재하지 않습니다. 생성을 원하시면 pk필드를 제거후 요청해주세요.",
        "incorrect_type": "department1는 JSON Object 구조로 채워주셔야합니다. {data_type} 타입은 허용하지 않습니다.",
    }

    def __init__(self, **kwargs):
        self.allow_get_or_create = kwargs.pop("allow_get_or_create", False)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        if not isinstance(data, dict):
            self.fail("incorrect_type", data_type=type(data).__name__)

        try:
            if data.get("id"):
                return queryset.get(pk=data["id"])
        except ObjectDoesNotExist:
            self.fail("does_not_exist", pk_value=data["id"])

        if self.allow_get_or_create is True:
            return queryset.create(**data)


class CustomDepartmentField(CustomRelatedField):
    class Meta:
        model = Department1
        fields = "__all__"


class CustomCompanyField(CustomRelatedField):
    class Meta:
        model = Company
        fields = "__all__"


class EmployeeWithCustomDepartment1Serializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    company = CustomCompanyField(queryset=Company.objects.all(), allow_get_or_create=False)
    is_deleted = serializers.BooleanField()
    birth_date = serializers.DateField(format="%Y-%m-%d")
    employment_period = serializers.FloatField(help_text="재직 기간 ex: 3.75년")
    programming_language_skill = serializers.ListField(child=serializers.CharField())
    department1 = CustomDepartmentField(queryset=Department1.objects.all(), allow_get_or_create=True)

    def create(self, validated_data: dict[str, Any]) -> Employee:
        print(validated_data["name"])
        print(validated_data["age"])
        print(validated_data["company"])
        print(validated_data["is_deleted"])
        print(validated_data["birth_date"])
        print(validated_data["employment_period"])
        print(validated_data["programming_language_skill"])
        print(validated_data["department1"])

        employee = Employee.objects.create(**validated_data)

        return employee
