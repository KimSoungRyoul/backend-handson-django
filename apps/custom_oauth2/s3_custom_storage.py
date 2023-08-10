from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage

from config import settings


class MediaStorage(S3Boto3Storage):
    bucket_name = "pycon2023-django-sprints-bucket"
    location = "media"


class StaticStorage(S3StaticStorage):
    bucket_name = "pycon2023-django-sprints-bucket"
    location = "static"

