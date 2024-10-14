"""요청에 대한 응답의 상태를 나타내는 정의값."""

from enum import Enum


class ResponseStatus(Enum):
    """응답 결과에 대한 상태값을 정의한 class."""

    FAIL = 0
    SUCCESS = 1


class ErrorCode(Enum):
    """에러코드를 정의한 class."""

    UNKNOWN = 0
    OK = 1
    BADREQUEST = 2
    UNAUTHENTICATED = 3
    PERMISSIONDENIED = 4
    NOTFOUND = 5
    METHODNOTALLOWD = 6
    NOTACCEPTABLE = 7
    UNSUPPORTEDMEDIATYPE = 8
    THROTTLED = 9
    DATABASEERROR = 10
