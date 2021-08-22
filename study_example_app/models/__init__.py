from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.db import models
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import DecimalField
from django.db.models import DurationField
from django.db.models import F
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import IntegerChoices
from django.db.models import IntegerField
from django.db.models import Model
from django.db.models import Q
from django.db.models import TextChoices
from django.db.models.signals import post_save
from django.dispatch import receiver

from .file_field_example_models import *
from .n_plus_1_example_models import *
from .normal_field_example_models import *




class Student(models.Model):
    name = models.CharField(max_length=128, help_text="학생 이름")
    phone = models.CharField(
        max_length=32, help_text="연락처", validators=[validators.RegexValidator(regex=r"\d{2,3}-\d{3,4}-\d{4}")],
    )
    age = models.PositiveIntegerField(help_text="나이", default=0)
    major = models.CharField(max_length=32, help_text="전공")
    student_serial_num = models.CharField(max_length=64, help_text="학번")

    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 날짜")
    modified_at = models.DateTimeField(auto_now=True, help_text="수정 날짜")

    class Meta:
        abstract = False
        app_label = "study_example_app"
        managed = True
        proxy = False

        db_table = "student_db_table"
        get_latest_by = ("modified_at", "age")
        ordering = ("-modified_at", "name")
        # ordering = [F("phone").asc(nulls_last=True)]

        indexes = (
            models.Index(fields=("modified_at",), name="student_modified_at_idx"),
            models.Index(fields=("name", "age"), name="name_age_composite_idx"),
        )
        constraints = (
            models.CheckConstraint(check=Q(age__lte=140), name="constraint_abnormal_age"),
            models.UniqueConstraint(fields=("phone",), name="constraint_unique_phone"),
        )
