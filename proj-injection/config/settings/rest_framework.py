"""Rest Framework 관련 설정."""

#
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "base_modules.exception_handler.custom_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
