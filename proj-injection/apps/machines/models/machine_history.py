"""app(machine)의 machine의 작업 기록과 관련된 Django의 model을 정의."""

from django.db import models

from defines import OperationResult


class MachinesHistory(models.Model):
    """MachinesHistory : 사출기의 작업 기록을 저장하는 테이블."""

    request_datetime = models.DateTimeField()
    command = models.CharField(max_length=64)
    worker = models.BigIntegerField(blank=False, null=False)
    machine_id = models.BigIntegerField(blank=False, null=False)
    result = models.SmallIntegerField(
        choices=OperationResult.choices(),
        blank=False,
        null=False,
    )
    machine_owner_id = models.BigIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """MachinesHistory metadata."""

        app_label = "machines"
        db_table = "machines_history"
        indexes = [
            models.Index(fields=["machine_id", "machine_owner_id"], name="mo-index")
        ]
