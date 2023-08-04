from django.contrib.postgres import indexes
from django.db import models
from django.db.models import TextChoices


# from psqlextra.models import PostgresModel


class Product(models.Model):
    class ProductType(TextChoices):
        GROCERY = "grocery", "식료품"
        FURNITURE = "furniture", "가구"
        BOOKS = "books", "책"
        FOOD = "food", "음식"

    name = models.CharField(max_length=128, db_comment="상품명")
    price = models.PositiveIntegerField(db_comment="상품 가격")
    created_at = models.DateTimeField(auto_now_add=True, db_comment="생성시간")
    updated_at = models.DateTimeField(auto_now=True, db_comment="수정시간")
    product_type = models.CharField(choices=ProductType.choices, max_length=32)

    class Meta:
        db_table = "product"
        db_table_comment = "상품 테이블 입니다."
        ordering = ("-created_at",)
        indexes = (
            # django는 이런방식으로 Database에 Index를 생성 할 수 있다.
            models.Index(fields=["created_at"], name="created_at_index"),
            # 각 database별로 제공하는 Index의 전략이 다양한데 postgres의 경우 HashIndex가 있고 이를 django가 제공한다.
            # mysql도 높은버전에서는 HashIndex지원된다
            indexes.HashIndex(fields=["name"], name="name_pt_composite_index"),
        )
        constraints = (
            # 제약조건은 Unique 조건으로 주로 사용한다.
            models.UniqueConstraint(fields=["name", "product_type"], name="unique_product_name_type"),

            # 제약조건은 이런식으로도 줄수있기는한데 잘 사용안한다.
            models.CheckConstraint(check=models.Q(price__lte=100_000_000), name="check_unreasonalbe_price"),

        )
Product.objects