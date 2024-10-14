"""drf-yasg의 swagger와 redoc와 관련한 설정."""

# Swagger Settings
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "USE_SESSION_AUTH": False,
    "VALIDATOR_URL": None,
}
# Redoc Settings
REDOC_SETTINGS = {
    "LAZY_RENDERING": False,
}
