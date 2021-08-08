from django.db import models

# Create your models here.
class Store(models.Model):
    class StoreType(models.TextChoices):
        FOOD = 'food', '배달음식'
        GROCERY = 'grocery', '식료품/가공식품'
        PET_FOOD = 'pet_food', '반려동물음식'

    name = models.CharField(max_length=128, help_text='음식점 가게명')
    owner = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    tel_num = models.CharField(max_length=16, help_text='음식점 연락처')
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'store'
