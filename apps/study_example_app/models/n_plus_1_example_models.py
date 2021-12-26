from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=128, help_text="음식점 가게명")
    tel_num = models.CharField(max_length=16, help_text="음식점 연락처")


class Menu(models.Model):
    name = models.CharField(max_length=128, help_text="음식 메뉴이름")
    price = models.IntegerField(help_text="음식 가격")

    restaurant = models.ForeignKey(to="Restaurant", on_delete=models.CASCADE, help_text="이 메뉴를 판매하는 음식점")
