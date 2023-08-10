# type("CustomUserManager", (UserManager, type(MysqlQuerySet.as_manager())), {})() # 선언과동시에 생성
from django.contrib.auth.models import UserManager
from django_mysql.models.query import QuerySet as MysqlQuerySet


class CustomUserManager(UserManager, type(MysqlQuerySet.as_manager())):
    ...
