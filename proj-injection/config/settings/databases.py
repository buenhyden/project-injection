"""DATABASES 관련 설정."""

import os

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": os.environ["DEFAULT_USERNAME"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOSTNAME"],
        "PORT": os.environ["POSTGRES_PORT"],
        # "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "db.sqlite3",
    }
}
# Auth User Model
AUTH_USER_MODEL = "accounts.Accounts"  # 추가
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
