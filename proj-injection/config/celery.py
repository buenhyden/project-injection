"""defines the Celery instance."""

import os

from celery import Celery

# 'celery' program 구동을 위한 Default Django settings module을 setting.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

app = Celery("config")
# 네임스페이스='CELERY'는 모든 셀러리 관련 구성 키에 'CELERY_' 접두사가 있어야 함을 의미.
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

# 등록된 django apps 내부의 모든 task 모듈을 찾는다.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """A task that dumps its own request information."""
    print(f"Request: {self.request!r}")
