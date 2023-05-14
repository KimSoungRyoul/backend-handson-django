import os
import uuid

from django.db import models
from django.utils import timezone


def upload_filepath(instance: models.Model, filename: str):
    # ex: filename = "./i_am_file.txt""
    today_str = timezone.now().strftime("%Y%m%d")
    # ex: file_basename = "i_am_file.txt"
    file_basename: str = os.path.basename(filename)
    return f"{instance._meta.db_table}/{today_str}/{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=file_basename)}_{file_basename}"


class FileFieldExampleModel(models.Model):
    file = models.FileField(upload_to=upload_filepath, null=True, max_length=256)
    image = models.ImageField(upload_to=upload_filepath, null=False, max_length=256)
