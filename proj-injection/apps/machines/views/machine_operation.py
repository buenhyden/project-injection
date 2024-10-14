"""특정 사출기에 대한 동작 요청을 다루기 위한 파일."""

from datetime import datetime

from celery import chain
from django.core.exceptions import BadRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from base_modules.response_handler import response_handler
from base_modules.swagger_schema_view import set_fail_response_schema
from defines import (
    ResponseStatus,
)

from ..serializers import RequestOperationSerializer, ResponseOperationSerializer
from ..tasks import task_machine_operation_history, task_machine_operator


class MachineOperationView(APIView):
    """특정 사출기를 동작시키기 위한 APIView."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="machines_operation_create",
        responses={
            200: ResponseOperationSerializer,
            400: set_fail_response_schema(400),
            401: set_fail_response_schema(401),
            403: set_fail_response_schema(403),
            404: set_fail_response_schema(404),
            405: set_fail_response_schema(405),
            406: set_fail_response_schema(406),
            415: set_fail_response_schema(415),
            429: set_fail_response_schema(429),
            500: set_fail_response_schema(500),
        },
        request_body=RequestOperationSerializer,
    )
    def post(self, request, pk, format=None):
        """특정 사출기를 동작시키거나 중단시키는 명령을 수행한다.

        특정 사출기에 대하여 동작을 시키거나 중단할 수 있다.

        Args:
            request (Request): HttpRequest object
            pk (int): InjectionMoldingMachines의 Primary Key
            format (str, optional): API 요청 시 응답 포맷을 지정하는 데 사용. Defaults to None.

        Raises:
            NotAuthenticated: 인증되지 않은 사용자.
            PermissionDenied: 권한없음
            BadRequest: 명령이 잘못 입력됨.

        Returns:
            rest_framework.response.Response: 특정 사출기를 동작/중단 요청에 대한 응답
        """
        request_datetime = datetime.now()
        request_data = request.data
        auth = request.auth.payload
        if auth is None:
            raise NotAuthenticated
        requested_user_id = auth["user_id"]
        command = request_data.get("command")
        if command is None:
            raise BadRequest
        result = {
            "command": command,
        }

        res = chain(
            task_machine_operator.s(
                pk=pk,
                worker=requested_user_id,
                request_datetime=request_datetime,
                command=command,
            ),
            task_machine_operation_history.s(),
        )()        
        result["message"] = "Operation Success"

        res = response_handler(
            response_status=ResponseStatus.SUCCESS.value,
            result=result,
            status_code=status.HTTP_200_OK,
        )
        return res
