from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres import fields as postgres_fields
from django.core import validators
from django.db.models import Model
from django.db.models import Q
from django_mysql.models import fields as mysql_fields

from .file_field_example_models import *
from .n_plus_1_example_models import *
from .normal_field_example_models import *


class Team(models.Model):
    name = models.CharField(max_length=32)


class Student(models.Model):
    name = models.CharField(max_length=128, help_text="학생 이름")
    phone = models.CharField(
        max_length=32, help_text="연락처", validators=[validators.RegexValidator(regex=r"\d{2,3}-\d{3,4}-\d{4}")],
    )
    age = models.PositiveIntegerField(help_text="나이", default=0)
    major = models.CharField(max_length=34, help_text="전공", default="sdf")
    student_serial_num = models.CharField(max_length=64, help_text="학번")

    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 날짜")
    modified_at = models.DateTimeField(auto_now=True, help_text="수정 날짜")

    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, help_text="sdfsdf2222", null=True)

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


class Department(models.Model):
    name = models.CharField(max_length=32, help_text="부서명")
    description = models.CharField(max_length=256, help_text="해당 부서가 하는 역할")


class Company(models.Model):
    name = models.CharField(max_length=64)
    company_number = models.CharField(max_length=32)


class Employee(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    company = models.ForeignKey(to="Company", on_delete=models.CASCADE)
    is_deleted = models.BooleanField()
    birth_date = models.DateField(null=True)
    employment_period = models.FloatField(help_text="재직 기간 ex: 3.75년")
    programming_language_skill = postgres_fields.ArrayField(base_field=models.CharField(max_length=32), size=5)
    # programming_language_skill = mysql_fields.ListCharField(base_field=CharField(max_length=32), size=5, max_length=(5 * 33))
    department = models.ForeignKey(to="Department", on_delete=models.CASCADE)
