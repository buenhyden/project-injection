"""Create a SchemaView class with default renderers and generators."""

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

swagger_schema_view = get_schema_view(
    openapi.Info(
        title="Injection Management API",
        default_version="v1",
        description="사출기 관리 시스템을 위한 RESTful API를 설계하고 구현한다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="chochyjj@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
