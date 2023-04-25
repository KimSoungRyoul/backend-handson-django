from django.http import HttpRequest
from django.shortcuts import render
from table_document_app.utils import get_dict_of_models_list


def db_schema_docs_template_view(request: HttpRequest):
    apps_and_models = get_dict_of_models_list()
    context = {
        "apps": apps_and_models,
    }
    return render(request, "db_schema.html", context)
