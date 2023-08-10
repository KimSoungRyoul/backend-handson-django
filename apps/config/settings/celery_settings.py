import os

from kombu.utils.url import safequote

# BROKER_URL = "http://localstack:4566/000000000000/hello-sb-queue"

AWS_ACCESS_KEY_ID = safequote(os.getenv("AWS_ACCESS_KEY_ID", ""))
AWS_SECRET_ACCESS_KEY = safequote(os.getenv("AWS_SECRET_ACCESS_KEY", ""))
HOST = os.getenv("SQS_URL", "")  # localhost:4566/000000000000/sample-queue

CELERY_BROKER_URL = f"sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}@{HOST}"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "predefined_queues": {
        "sample-celery": {
            "url": f"http://{HOST}" if "localhost" in HOST else f"https://{HOST}",
            "access_key_id": AWS_ACCESS_KEY_ID,
            "secret_access_key": AWS_SECRET_ACCESS_KEY,
        }
    },
    "region": os.getenv("AWS_REGION"),
    "visibility_timeout": 3600,
    "polling_interval": 10,
    "queue_name_prefix": "sample-",
    "CELERYD_PREFETCH_MULTIPLIER": 0,
}
