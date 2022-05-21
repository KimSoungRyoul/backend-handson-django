from django.shortcuts import render

# Create your views here.

import os
from collections import defaultdict
from typing import Dict

from django.apps import apps as django_apps
from django.conf import settings
from django.db import connections
from django.db.models.fields import NOT_PROVIDED
from django.shortcuts import render

DIRECTORY_PATH = os.path.dirname(__file__)


def convert_fields_to_dict(fields, unique_together, db_field_info: Dict[str, str]):
    unique_together_tags = defaultdict(list)
    for idx, columns in enumerate(unique_together):
        for column in columns:
            unique_together_tags[column].append("U_{}".format(idx))

    return [
        {
            "name": field.column,
            "primary_key": field.primary_key,
            "django_field_type": field.__class__.__name__,
            "db_column_type": db_field_info.get(field.column)
            if db_field_info and db_field_info.get(field.column)
            else "마이그레이션 반영안된 Field",
            "null": field.null,
            "unique": field.unique,
            "unique_together_tags": unique_together_tags.get(field.name, ""),
            "db_index": field.db_index,
            "default": field.default if not field.default == NOT_PROVIDED else "None",
            "verbose_name": field.verbose_name,
            "help_text": field.help_text,
            "choices": field.choices,
            "fk": field.related_model._meta.db_table if field.is_relation else "",
            "many_to_many_fk": field if field.many_to_many else "",
            "max_length": field.max_length,
        }
        for field in fields
    ]


def convert_constraints_together_to_column_name_basis(unique_together, model_fields):
    field_to_column_map = {field.name: field.column for field in model_fields}
    return [[field_to_column_map[field] for field in fields] for fields in unique_together]


def get_dict_of_models_list():
    models_per_apps = []
    apps = {
        app_path.split(".")[-1]
        for app_path in settings.INSTALLED_APPS
       # if "apps." in app_path or app_path == "django_db"
    }
    for app_name in sorted(apps):

        models = sorted(
            [model for model in django_apps.app_configs.get(app_name).models.values() if not model._meta.proxy],
            key=lambda model: model._meta.db_table,
        )

        if not models:
            continue

        with connections["default"].cursor() as cursor:
            cursor.execute(
                "SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='django_db'"
            )
            column_info_dict = {}
            for row in cursor.fetchall():
                if column_info_dict.get(row[0]):
                    column_info_dict[row[0]][row[1]] = row[2]
                else:
                    column_info_dict[row[0]] = {row[1]: row[2]}

        models_per_apps.append(
            {
                "app_name": app_name,
                "models": [
                    {
                        "model_name": model.__name__,
                        "table_name": model._meta.db_table,
                        "unique_together": convert_constraints_together_to_column_name_basis(
                            model._meta.unique_together, model._meta.fields
                        ),
                        "index_together": convert_constraints_together_to_column_name_basis(
                            model._meta.index_together, model._meta.fields
                        ),
                        "fields": convert_fields_to_dict(
                            model._meta.fields + model._meta.many_to_many,
                            model._meta.unique_together,
                            db_field_info=column_info_dict.get(model._meta.db_table),
                        ),
                    }
                    for model in models
                ],
            }
        )

    return models_per_apps
