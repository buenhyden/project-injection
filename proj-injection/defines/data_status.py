"""데이터베이스에 입력되는 정의값들을 class로 정의하여 모아놓은 파일."""

from enum import Enum


class MachineStatus(Enum):
    """InjectionMoldingMachines의 status 필드를 정의하기 위한 class."""

    POWEROFF = 0  # 전원 꺼짐
    READY = 1  # 전원이 켜졌으나 작업이 되고 있지 않음.
    RUNNING = 2  # 작업중
    PENDING = 3  # 보류중
    ERROR = 4  # 작업중 원인 불명의 원인으로 문제 발생함

    @classmethod
    def choices(cls):
        """InjectionMoldingMachines의 status 필드에서 choices로 사용할 수 있도록 만든 method."""
        return tuple((i.value, i.name) for i in cls)


class OperationResult(Enum):
    """MachinesHistory의 result 필드를 정의하기 위한 class."""

    SUCCESS = 1
    REMOTEFAILED = 2
    INTERNALFAILED = 3
    PENDING = 4
    PERMISSIONDENIED = 5
    IGNORE = 6
    INVALIDCOMMAND = 7

    @classmethod
    def choices(cls):
        """MachinesHistory result 필드에서 choices로 사용할 수 있도록 만든 method."""
        return tuple((i.value, i.name) for i in cls)
