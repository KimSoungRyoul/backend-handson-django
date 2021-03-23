from django.db import models


class Store(models.Model):
    class StoreType(models.TextChoices):
        FOOD = 'food', '배달음식'
        GROCERY = 'grocery', '식료품/가공식품'
        PET_FOOD = 'pet_food', '반려동물음식'

    name = models.CharField(max_length=128, help_text='음식점 가게명')
    owner = models.ForeignKey(to='ShoppingMallUser', on_delete=models.CASCADE)
    tel_num = models.CharField(max_length=16, help_text='음식점 연락처')

    class Meta:
        db_table = 'store'
