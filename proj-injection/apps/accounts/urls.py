"""accounts app의 URLconf."""

from django.urls import path

from . import views

urlpatterns = [
    path("sign-up/", views.AccountRegisterAPIView.as_view(), name="user-sign-up"),
    path("log-in/", views.AccountLoginAPIView.as_view(), name="user-sign-in"),
    path("log-out/", views.AccountLogoutAPIView.as_view(), name="user-sign-in"),
    path(
        "user/machines/history/",
        views.AccountOperationMachineHistoryView.as_view(),
        name="user-machine-history",
    ),
]
