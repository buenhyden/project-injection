"""app(accounts) Config."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """app(accounts) Config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
