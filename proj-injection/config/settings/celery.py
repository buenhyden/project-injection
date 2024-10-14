"""CELERY 설정."""

import os

CELERY_BROKER_URL = f"""redis://:{os.environ["REDIS_PASSWORD"]}@{os.environ["REDIS_HOSTNAME"]}:{os.environ["REDIS_PORT"]}"""
CELERY_RESULT_BACKEND = f"""redis://:{os.environ["REDIS_PASSWORD"]}@{os.environ["REDIS_HOSTNAME"]}:{os.environ["REDIS_PORT"]}"""
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_BACKEND = "django-db"
# CELERY_CACHE_BACKEND = "default"
# CELERY_TIMEZONE = os.environ["TZ"]
