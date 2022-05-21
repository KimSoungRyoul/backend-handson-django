from django.db import models

# Create your models here.


class Major(models.Model):
    class Type(models.TextChoices):
        ENGINEERING = "engineering", "공학계열"
        BUSINESS = "business", "상경계열"

    name = models.CharField(max_length=32)
    major_type = models.CharField(choices=Type.choices, max_length=32)
    university = models.ForeignKey(to="University", on_delete=models.CASCADE)

    class Meta:
        db_table = "major"


class University(models.Model):
    name = models.CharField(max_length=64, help_text="학교이름")
    date_established = models.DateField(help_text="설립일자")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "university"
