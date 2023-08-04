import typing

from django.db import models


class OrderedProduct(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE)
    product = models.ForeignKey(to="Product", on_delete=models.CASCADE)
    count = models.IntegerField(db_comment="주문한 해당 메뉴의 갯수", default=1)

    class Meta:
        db_table = "ordered_product"
        db_table_comment = "주문된 상품, Order와 Product사이 매핑테이블"


class Address(typing.TypedDict):
    """
    https://peps.python.org/pep-0655/
    TypedDict는 3.8에서 새로 나온 문법이고 3.11에 안정화 되었다.


    3.8~3.10 사이 TypedDict 구현은 불안정하기 때문에
    mypy와 함께 사용하려고 한다면
    from typing import TypedDict 대신에
    from typing_extensions import TypedDict 을 사용할것을 권장한다.
    """

    province: str  # 도/특별시/광역시 이름, 예: "Seoul"
    city: str | None  # 시/군 이름, 예: "Suwon-si", "Pyeongtaek-si". 주로 도에 속한 시/군을 나타냄.
    district: str | None  # 구 이름, 예: "Seocho-gu", "Gangnam-gu". 주로 특별시/광역시에 속한 구를 나타냄.
    township: str | None  # 읍/면/동 이름, 예: "Ojeong-dong", "Bugok-myeon".
    neighborhood: typing.NotRequired[str | None]  # 리 이름, 예: "Jung-ri", "Sang-ri".
    street: str | None  # 도로명, 예: "Teheran-ro", "Samsung-ro".
    building_number: str | None  # 건물 번호 혹은 건물명, 예: "123", "Acro Tower".
    postal_code: str | None  # 우편번호, 예: "06236"


def default_address() -> Address:
    return {
        "province": "",
        "city": "",
        "district": "",
        "township": "",
        "neighborhood": "",
        "street": "",
        "building_number": "",
        "postal_code": ""
    }


class Order(models.Model):
    class Status(models.TextChoices):
        WAIT_FOR_ACCEPT = "WAIT_FOR_ACCEPT", "주문수락대기중"
        CANCEL = "CANCEL"
        COOKING = "COOKING", "조리중"
        WAIT_FOR_DELIVERY = "WAIT_FOR_DELIVERY", "조리완료(배달대기중)"
        DELIVERY = "delivery", "배달중"

    status = models.CharField(max_length=32, choices=Status.choices, db_comment="주문 상태값", default=Status.WAIT_FOR_ACCEPT)
    total_price = models.IntegerField(default=0)
    product_set = models.ManyToManyField(to="Product", through="OrderedProduct")
    created_at = models.DateTimeField(auto_now_add=True, help_text="주문이 생성된 시간")
    address = models.JSONField(help_text="주문 배송지", default=default_address)
