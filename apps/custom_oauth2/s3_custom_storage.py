from storages.backends.s3boto3 import S3Boto3Storage

from config import settings


class MediaStorage(S3Boto3Storage):
    bucket_name = "pycon2023-django-sprints-bucket"
    location = "media"


class StaticStorage(S3Boto3Storage):
    bucket_name = "pycon2023-django-sprints-bucket"
    location = "static"

    # def __init__(self, *args, **kwargs):
    #     #kwargs["custom_domain"] = settings.AWS_CLOUDFRONT_DOMAIN
    #     super(StaticStorage, self).__init__(*args, **kwargs)
