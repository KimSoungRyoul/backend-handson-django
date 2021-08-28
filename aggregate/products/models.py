from django.contrib.postgres.indexes import HashIndex
from django.db import models
from django.db.models import TextChoices


class Product(models.Model):
    class ProductType(TextChoices):
        GROCERY = 'grocery', '식료품'
        FURNITURE = 'furniture', '가구'
        BOOKS = 'books', '책'
        FOOD =  "food", "음식"

    name = models.CharField(max_length=128, help_text='상품명')
    price = models.IntegerField(help_text='상품 가격')
    created_at = models.DateTimeField(auto_now_add=True)
    product_type = models.CharField(choices=ProductType.choices, max_length=32)
    store = models.ForeignKey(to='stores.Store', on_delete=models.CASCADE, help_text='이 상품을 판매하는 가게')

    class Meta:
        db_table = 'product'
        ordering = ('-created_at',)
        indexes = (
            models.Index( # django는 이런방식으로 Database에 Index를 생성 할 수 있다.
                fields=['created_at'], name='created_at_index',
            ),
            models.Index(fields=['name', 'product_type'], name='name_pt_composite_index'),
            # 각 database별로 제공하는 Index의 전략이 다양한데 postgres의 경우 django가 선탟할수있도록 기능을 제공한다.
            HashIndex(fields=['name'], name='name_hash_index'),
        )
        constraints = (
            models.CheckConstraint(check=models.Q(price__lte=100_000_000), name='check_unreasonalbe_price'),
            models.UniqueConstraint(fields=['store', 'name', 'product_type'], name='unique_in_store'),
        )


class GroceryProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type=Product.ProductType.GROCERY)


class GroceryProduct(Product):
    objects = GroceryProductManager()

    class Meta:
        proxy = True

    # 각종 식료품 관련 메서드들 ...
    # ex: is_3_days_before_to_expired() 유통기한 3일남은 상품인가?


class FurnitureProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type=Product.ProductType.FURNITURE)


class FurnitureProduct(Product):
    objects = FurnitureProductManager()

    class Meta:
        proxy = True

    # 각종 가구 관련 메서드들
    # ex: is_heavy() 대형 가구인가?


class BooksProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(product_type=Product.ProductType.BOOKS)


class BooksProduct(Product):
    objects = BooksProductManager()

    class Meta:
        proxy = True
