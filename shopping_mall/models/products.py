from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=128, help_text='상품명')
    price = models.IntegerField(help_text='상품 가격')
    store = models.ForeignKey(to='Store', on_delete=models.CASCADE, help_text='이 상품을 판매하는 가게')

    class Meta:
        db_table = 'product'
