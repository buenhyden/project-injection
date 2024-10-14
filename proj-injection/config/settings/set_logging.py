"""Logging 관련 설정."""

import os


def set_logging(BASE_DIR):
    """Logging의 설정을 리텀함.

    Args:
        BASE_DIR (str): Project Directory

    Returns:
        dict: Logging 설정값
    """
    LOG_BASE_FOLDER = BASE_DIR / "logs"
    if not os.path.exists(LOG_BASE_FOLDER):
        os.mkdir(LOG_BASE_FOLDER)
    LOG_CELERY_FOLDER = LOG_BASE_FOLDER / "celery"
    if not os.path.exists(LOG_CELERY_FOLDER):
        os.mkdir(LOG_CELERY_FOLDER)
    LOG_SERVER_FOLDER = LOG_BASE_FOLDER / "server"
    if not os.path.exists(LOG_SERVER_FOLDER):
        os.mkdir(LOG_SERVER_FOLDER)
    LOG_SYSTEM_FOLDER = LOG_BASE_FOLDER / "system"
    if not os.path.exists(LOG_SYSTEM_FOLDER):
        os.mkdir(LOG_SYSTEM_FOLDER)
    LOG_ERROR_FOLDER = LOG_BASE_FOLDER / "error"
    if not os.path.exists(LOG_ERROR_FOLDER):
        os.mkdir(LOG_ERROR_FOLDER)

    DEFAULT_LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[{server_time}] {message}",
                "style": "{",
            },
            "verbose": {
                "format": "[{levelname}][{asctime}][{module}:{lineno}-{funcName}][{process:d}][{thread:d}] {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "django.server": {
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOG_SERVER_FOLDER / "django.server.log",
                "when": "midnight",
                "encoding": "utf-8",
                "backupCount": 10,
                "formatter": "django.server",
            },
            "system_info": {
                "level": "INFO",
                "filters": ["require_debug_false"],
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOG_SYSTEM_FOLDER / "system_info.log",
                "when": "midnight",
                "encoding": "utf-8",
                "backupCount": 10,
                "formatter": "verbose",
            },
            "system_error": {
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOG_ERROR_FOLDER / "system_error.log",
                "when": "midnight",
                "encoding": "utf-8",
                "backupCount": 10,
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": "INFO",
                "propagate": False,
            },
            "system_info": {
                "handlers": ["system_info"],
                "level": "INFO",
                "propagate": False,
            },
            "system_error": {
                "handlers": ["system_error"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }
    return DEFAULT_LOGGING
