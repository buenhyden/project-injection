"""시스템의 url, settings, asgi, wsgi 등을 설정."""

from .celery import app as celery_app

__all__ = ("celery_app",)
