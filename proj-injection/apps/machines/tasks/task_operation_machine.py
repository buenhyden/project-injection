"""작업 요청을 하는 tasks를 관리하기 위한 파일."""

import logging
from time import sleep

import requests
from celery import shared_task
from django.core.exceptions import BadRequest
from rest_framework.exceptions import PermissionDenied

from defines import MachineStatus, OperationCommands, OperationResult

from ..models import InjectionMoldingMachines

logger = logging.getLogger("system_error")


@shared_task
def task_machine_operator(pk, worker, request_datetime, command):
    """해당 사출기에 작업을 요청한다.

    해당 사출기에 작업을 요청하며 Command에 따라 나뉜다.

    Args:
        pk (int): InjectionMoldingMachines의 Primary Key
        worker (int): 요청한 사용자
        request_datetime (datetime): 요청한 시간
        command (str): Operation Command

    Returns:
        dict: MachinesHistory에 기록을 저장하기 위해 필요한 데이터
    """
    try:
        obj = InjectionMoldingMachines.objects.get(pk=pk)
        machine_id = obj.pk
        machine_owner_id = obj.owner_id
        location = obj.location
        obj_status = obj.status

        request_step = True
        if command == OperationCommands.START.name:
            if obj_status == MachineStatus.POWEROFF.value:
                request_step = False
            elif obj_status == MachineStatus.READY.value:
                request_step = True
            elif obj_status == MachineStatus.RUNNING.value:
                request_step = False
            elif obj_status == MachineStatus.PENDING.value:
                request_step = False
            else:
                request_step = False
        elif command == OperationCommands.STOP.name:
            if obj_status == MachineStatus.POWEROFF.value:
                request_step = False
            elif obj_status == MachineStatus.READY.value:
                request_step = False
            elif obj_status == MachineStatus.RUNNING.value:
                request_step = True
            elif obj_status == MachineStatus.PENDING.value:
                request_step = False
            else:
                request_step = False
        else:
            raise BadRequest
        sleep(10)
        if request_step:
            body = {"command": command}
            if worker != machine_owner_id:
                raise PermissionDenied
            response = requests.post(location, data=body)       

    except BadRequest as e:
        logger.error(e)
        result_status = OperationResult.IGNORE.value
    except PermissionDenied as e:
        logger.error(e)
        result_status = OperationResult.PERMISSIONDENIED.value
    except Exception as e:
        result_status = OperationResult.INTERNALFAILED.value
        logger.error(e)
    else:
        if request_step:
            operation_result = response.json()
            if operation_result["result"] == OperationResult.SUCCESS.value:
                result_status = OperationResult.SUCCESS.value
            elif operation_result["result"] == OperationResult.REMOTEFAILED.value:
                result_status = OperationResult.REMOTEFAILED.value
            else:
                result_status = OperationResult.PENDING.value
        else:
            result_status = OperationResult.INVALIDCOMMAND.value
    finally:
        return_value = {
            "request_datetime": request_datetime,
            "worker": worker,
            "result_status": result_status,
            "command": command,
            "machine_id": machine_id,
            "machine_owner_id": machine_owner_id,
        }
        return return_value
