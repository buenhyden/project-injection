"""django admin management for app(machines)."""

from django.contrib import admin

from .models import InjectionMoldingMachines, MachinesHistory


# Register your models here.
class InjectionMoldingMachinesAdmin(admin.ModelAdmin):
    """the representation of the InjectionMoldingMachines in the admin interface."""

    list_display = ("name", "location", "status", "owner_id")


# Register your models here.
class MachinesHistoryAdmin(admin.ModelAdmin):
    """the representation of the MachinesHistory in the admin interface."""

    list_display = (
        "machine_id",
        "machine_owner_id",
        "worker",
        "command",
        "result",
        "request_datetime",
    )


admin.site.register(InjectionMoldingMachines, InjectionMoldingMachinesAdmin)
admin.site.register(MachinesHistory, MachinesHistoryAdmin)
