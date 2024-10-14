"""작업 기록 저장을 위한 task를 관리하기 위한 파일."""

import logging

from celery import shared_task

from defines import MachineStatus, OperationResult

from ..models import InjectionMoldingMachines
from ..serializers import MachinesHistorySerializer

logger = logging.getLogger("system_error")


@shared_task
def task_machine_operation_history(return_value):
    """작업 요청에 따른 결과에 따라 해당 사출기의 작업을 기록한다.

    작업 요청에 따른 결과에 따라 해당 사출기의 작업을 기록한다.

    Args:
        return_value (dict): task_machine_operator의 return 값

    Returns:
        None : return 없음
    """
    try:
        request_datetime = return_value["request_datetime"]
        worker = return_value["worker"]
        result_status = return_value["result_status"]
        command = return_value["command"]
        machine_id = return_value["machine_id"]
        machine_owner_id = return_value["machine_owner_id"]

        if (
            result_status != OperationResult.PERMISSIONDENIED.value
            and result_status != OperationResult.IGNORE.value
        ):
            obj = InjectionMoldingMachines.objects.get(pk=machine_id)
            if result_status == OperationResult.SUCCESS.value:
                obj.status = MachineStatus.READY.value
                obj.save()
            elif result_status == OperationResult.REMOTEFAILED.value:
                obj.status = MachineStatus.ERROR.value
                obj.save()
            elif result_status == OperationResult.PENDING.value:
                obj.status = MachineStatus.PENDING.value
                obj.save()
        if result_status != OperationResult.IGNORE.value:
            history = {
                "request_datetime": request_datetime,
                "command": command,
                "worker": worker,
                "machine_id": machine_id,
                "machine_owner_id": machine_owner_id,
                "result": result_status,
            }
            serializer = MachinesHistorySerializer(data=history)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    except Exception as e:
        logger.error(e)
