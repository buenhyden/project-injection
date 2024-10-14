"""URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from base_modules.swagger_schema_view import swagger_schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger<format>/",
        swagger_schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/swagger/",
        swagger_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/docs/",
        swagger_schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/", include("apps.accounts.urls"), name="accounts"),
    path("api/", include("apps.machines.urls"), name="machines"),
    # url(
    #     r"^static/(?P<path>.*)$", static.serve, {"document_root": settings.STATIC_ROOT}
    # ),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
