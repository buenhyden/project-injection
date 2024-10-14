"""swagger의 실패에 대한 responses를 세팅하기 위한 함수."""

from drf_yasg.openapi import TYPE_INTEGER, TYPE_OBJECT, TYPE_STRING, Schema

from defines import ErrorCode, ResponseStatus


def set_fail_response_schema(http_status_code):
    """swagger의 실패에 대한 responses를 세팅하기 위한 함수.

    Args:
        http_status_code (int): http status code

    Returns:
        drf_yasg.openapi.Schema: openapi Schema
    """
    status = Schema(
        "Response Status Code",
        description="Response Status",
        type=TYPE_INTEGER,
        default=ResponseStatus.FAIL.value,
    )
    message = Schema("message", description="Error와 관련된 메시지", type=TYPE_STRING)
    if http_status_code == 400:
        title_error_code = ErrorCode.BADREQUEST.value
    elif http_status_code == 401:
        title_error_code = ErrorCode.UNAUTHENTICATED.value
    elif http_status_code == 403:
        title_error_code = ErrorCode.PERMISSIONDENIED.value
    elif http_status_code == 404:
        title_error_code = ErrorCode.NOTFOUND.value
    elif http_status_code == 405:
        title_error_code = ErrorCode.METHODNOTALLOWD.value
    elif http_status_code == 406:
        title_error_code = ErrorCode.NOTACCEPTABLE.value
    elif http_status_code == 415:
        title_error_code = ErrorCode.UNSUPPORTEDMEDIATYPE.value
    elif http_status_code == 429:
        title_error_code = ErrorCode.THROTTLED.value
    else:
        title_error_code = ErrorCode.UNKNOWN.value
    error_code = Schema(
        description="Error Code",
        default=title_error_code,
        type=TYPE_INTEGER,
    )
    schema = Schema(
        type=TYPE_OBJECT,
        properties={"status": status, "error_code": error_code, "message": message},
    )
    return schema
