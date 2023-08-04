from typing import TypeVar, TYPE_CHECKING

from django.db import models
from django.db.models import sql

T = TypeVar("T", bound=models.Model, covariant=True)

DYNAMODB_DEFAULT_DB_ALIAS = "dynamodb"


class DynamoDBQuery(sql.Query):

    def sql_with_params(self):
        sql, params = self.get_compiler(DYNAMODB_DEFAULT_DB_ALIAS).as_sql()
        return sql.replace(f"\"{self.model._meta.db_table}\".", ""), params



class DynamoDBQuerySet(models.QuerySet[T]):

    def __init__(self, model=None, query=None, using=None, hints=None):
        using = using or DYNAMODB_DEFAULT_DB_ALIAS
        super().__init__(model=model, query=query, using=using, hints=hints)
        self._query = query or DynamoDBQuery(self.model)
