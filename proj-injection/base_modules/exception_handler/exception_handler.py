"""Error가 발생할 경우, Error code및 response를 맞추기 위한 Class를 정의함."""

import logging

from django.core.exceptions import BadRequest, ObjectDoesNotExist
from django.core.exceptions import PermissionDenied as django_PermissionDenied
from django.db import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)
from django.http import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
)
from jwt.exceptions import InvalidTokenError
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAcceptable,
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
    Throttled,
    UnsupportedMediaType,
    ValidationError,
)
from rest_framework.views import set_rollback

from defines import ErrorCode, ResponseStatus

from ..response_handler import response_handler

logger = logging.getLogger("system_error")


def custom_exception_handler(exc, context):
    """restframework에서 exception을 처리하기 위한 handler.

    Args:
        exc (exceptions): exceptions
        context (dict): _description_

    Returns:
        rest_framework.response.Response: 예외 발생에 따른 응답
    """
    # HTTP status code "400 Bad Request".
    if isinstance(exc, BadRequest):
        exc = ValidationError(*(exc.args))
        error_code = ErrorCode.BADREQUEST.value
    elif isinstance(exc, ValidationError):
        exc = ValidationError(*(exc.args))
        error_code = ErrorCode.BADREQUEST.value
    elif isinstance(exc, HttpResponseBadRequest):
        exc = ValidationError(*(exc.args))
        error_code = ErrorCode.BADREQUEST.value
    elif isinstance(exc, ParseError):
        exc = ParseError(*(exc.args))
        error_code = ErrorCode.BADREQUEST.value

    # HTTP status code "401 Unauthenticated"
    elif isinstance(exc, AuthenticationFailed):
        exc = AuthenticationFailed(*(exc.args))
        error_code = ErrorCode.UNAUTHENTICATED.value
    elif isinstance(exc, NotAuthenticated):
        exc = NotAuthenticated(*(exc.args))
        error_code = ErrorCode.UNAUTHENTICATED.value
    elif isinstance(exc, InvalidTokenError):
        exc = NotAuthenticated(*(exc.args))
        error_code = ErrorCode.UNAUTHENTICATED.value

    # HTTP status code "403 Forbidden".
    elif isinstance(exc, PermissionDenied):
        exc = PermissionDenied(*(exc.args))
        error_code = ErrorCode.PERMISSIONDENIED.value
    elif isinstance(exc, HttpResponseForbidden):
        exc = PermissionDenied(*(exc.args))
        error_code = ErrorCode.PERMISSIONDENIED.value
    elif isinstance(exc, django_PermissionDenied):
        exc = PermissionDenied(*(exc.args))
        error_code = ErrorCode.PERMISSIONDENIED.value

    # HTTP status code "404 Not Found".
    elif isinstance(exc, Http404):
        exc = NotFound(*(exc.args))
        error_code = ErrorCode.NOTFOUND.value
    elif isinstance(exc, ObjectDoesNotExist):
        exc = NotFound(*(exc.args))
        error_code = ErrorCode.NOTFOUND.value
    elif isinstance(exc, HttpResponseNotFound):
        exc = NotFound(*(exc.args))
        error_code = ErrorCode.NOTFOUND.value
    elif isinstance(exc, NotFound):
        exc = NotFound(*(exc.args))
        error_code = ErrorCode.NOTFOUND.value

    # HTTP status code "405 Method Not Allowed".
    elif isinstance(exc, MethodNotAllowed):
        exc = MethodNotAllowed(*(exc.args))
        error_code = ErrorCode.METHODNOTALLOWD.value
    elif isinstance(exc, HttpResponseNotAllowed):
        exc = MethodNotAllowed(*(exc.args))
        error_code = ErrorCode.METHODNOTALLOWD.value

    # HTTP status code "406 Not Acceptable".
    elif isinstance(exc, NotAcceptable):
        exc = NotAcceptable(*(exc.args))
        error_code = ErrorCode.NOTACCEPTABLE.value
    #  HTTP status code "415 Unsupported Media Type".
    elif isinstance(exc, UnsupportedMediaType):
        exc = UnsupportedMediaType(*(exc.args))
        error_code = ErrorCode.UNSUPPORTEDMEDIATYPE.value
    # "429 Too Many Requests".
    elif isinstance(exc, Throttled):
        exc = Throttled(*(exc.args))
        error_code = ErrorCode.THROTTLED.value
    # Databases
    elif isinstance(exc, Error):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, InterfaceError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, DatabaseError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, DataError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, OperationalError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, IntegrityError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, InternalError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, ProgrammingError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    elif isinstance(exc, NotSupportedError):
        exc = DatabaseError(*(exc.args))
        error_code = ErrorCode.DATABASEERROR.value
    else:
        exc = BaseException(*(exc.args))
        error_code = ErrorCode.UNKNOWN.value
        logger.error(exc)

    result = {"error_code": error_code}

    if isinstance(exc, APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = f"{exc.wait}"
        result["message"] = exc.detail

        set_rollback()
        status_code = exc.status_code
    else:
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = f"{exc.wait}"
        result["message"] = exc.__str__()
        status_code = 500
    return response_handler(
        response_status=ResponseStatus.FAIL.value,
        result=result,
        status_code=status_code,
        headers=headers,
    )
