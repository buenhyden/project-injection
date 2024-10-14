"""app(machine)와 관련된 Django의 model을 정의."""

from django.db import models

from defines import MachineStatus


# Create your models here.
class InjectionMoldingMachines(models.Model):
    """InjectionMoldingMachines 사출기에 대한 데이터가 기록되는 테이블."""

    name = models.CharField(max_length=64, blank=False, null=False)
    location = models.CharField(max_length=256, blank=False, null=False)
    status = models.SmallIntegerField(
        choices=MachineStatus.choices(),
        blank=False,
        null=False,
        default=MachineStatus.READY.value,
    )
    owner_id = models.BigIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """InjectionMoldingMachines metadata."""

        app_label = "machines"
        db_table = "injection_molding_machines"

    def __str__(self):
        """human-readable representation of the model."""
        return self.name
