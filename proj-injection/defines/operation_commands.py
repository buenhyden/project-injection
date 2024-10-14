"""사출기에 작동과 관련한 command에 대한 정의값을 class로 정의하여 모아놓은 파일."""

from enum import Enum, auto


class OperationCommands(Enum):
    """사출기에 내릴 수 있는 명령어를 정의한 class."""

    START = auto()
    STOP = auto()
