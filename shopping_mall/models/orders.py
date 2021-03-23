from django.db import models


class OrderedProduct(models.Model):
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    count = models.IntegerField(help_text='주문한 해당 메뉴의 갯수', default=1)

    class Meta:
        db_table = 'ordered_product'


class Order(models.Model):
    total_price = models.IntegerField(default=0)
    store = models.ForeignKey(to='Store', on_delete=models.CASCADE)
    product_set = models.ManyToManyField(to='Product', through='OrderedProduct')

    address = models.CharField(max_length=256, help_text='주문 배송지')
