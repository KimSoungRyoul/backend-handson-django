import os
from uuid import uuid4

from django.db import models
from django.utils import timezone


def upload_filepath(instance: models.Model, filename: str):
    today_str = timezone.now().strftime("%Y%m%d")
    # ex: filename = "./i_am_file.txt""
    file_basename:str = os.path.basename(filename)
    # ex: file_basename = "i_am_file.txt"
    return f"aaaaa/duplicate_file_path.jpg"


class FileFieldExampleModel(models.Model):
    file = models.FileField(upload_to=upload_filepath, null=True, max_length=256)

    image = models.ImageField(upload_to=upload_filepath, null=False, max_length=256)
