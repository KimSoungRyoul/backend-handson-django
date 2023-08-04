from collections import namedtuple

from django.db.backends.postgresql.introspection import DatabaseIntrospection as PDatabaseIntrospection
from django.db.backends.base.introspection import FieldInfo as BaseFieldInfo
from django.db.backends.base.introspection import TableInfo as BaseTableInfo

FieldInfo = namedtuple("FieldInfo", BaseFieldInfo._fields + ("is_autofield", "comment"))
TableInfo = namedtuple("TableInfo", BaseTableInfo._fields + ("comment",))



class DatabaseIntrospection(PDatabaseIntrospection):
    ...