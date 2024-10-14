"""machines app의 URLconf."""

from django.urls import path

from . import views

urlpatterns = [
    path("machines/", views.MachineListView.as_view(), name="machines-list"),
    
    path(
        "machines/<int:pk>/", views.MachineDetailView.as_view(), name="machine-detail"
    ),
    path(
        "machines/<int:pk>/operation/",
        views.MachineOperationView.as_view(),
        name="machines-start",
    ),
    path(
        "machines/<int:pk>/history/",
        views.MachineHistoryView.as_view(),
        name="machine-detail-history",
    ),
]
