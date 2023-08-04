from django.conf import settings  # noqa
from django.db import NotSupportedError  # noqa
from django.db.backends.postgresql.base import DatabaseWrapper as PostgresDatabaseWrapper  # noqa
from django.utils.encoding import smart_str  # noqa
from django.utils.functional import cached_property  # noqa


from .client import DatabaseClient  # noqa
from .creation import DatabaseCreation  # noqa
from .features import DatabaseFeatures  # noqa
from .introspection import DatabaseIntrospection # noqa
from .operations import DatabaseOperations  # noqa
from .schema import DatabaseSchemaEditor  # noqa


class DatabaseWrapper(PostgresDatabaseWrapper):
    vendor = "dynamodb"
    display_name = "DynamoDB"

    # https://docs.aws.amazon.com/ko_kr/amazondynamodb/latest/developerguide/ql-reference.select.html
    operators = {
        "exact": "= ?",
        "iexact": "= UPPER(?)",
        "contains": "LIKE ?",
        "icontains": "LIKE UPPER(?)",
        "regex": "~ ?",
        "iregex": "~* ?",
        "gt": "> ?",
        "gte": ">= ?",
        "lt": "< ?",
        "lte": "<= ?",
        "startswith": "LIKE ?",
        "endswith": "LIKE ?",
        "istartswith": "LIKE UPPER(?)",
        "iendswith": "LIKE UPPER(?)",
    }