"""사용자의 사출기의 작업 기록에 대한 요청을 다루기 위한 파일."""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView

from apps.machines.models import MachinesHistory
from apps.machines.serializers import (
    MachinesHistorySerializer,
    ResponseSuccessMachineHistorySerializer,
)
from base_modules.response_handler import response_handler
from base_modules.swagger_schema_view import set_fail_response_schema
from defines import ResponseStatus


class AccountOperationMachineHistoryView(APIView):
    """사용자의 사출기의 작업 기록을 다루기 위한 APIView."""

    @swagger_auto_schema(
        operation_id="account_machines_history_list",
        responses={
            200: ResponseSuccessMachineHistorySerializer,
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
        tags=["User Machine History"],
    )
    def get(self, request, format=None):
        """사용자가 자신의 사출기 작업 기록을 조회한다.

        인증된 사용자는 자신이 소유한 모든 사출기에 대한 작업 기록을 조회할 수 있다.

        Args:
            request (Request): HttpRequest object
            format (str, optional): API 요청 시 응답 포맷을 지정하는 데 사용. Defaults to None.
        """
        auth = request.auth.payload
        if auth is None:
            raise NotAuthenticated
        histories = MachinesHistory.objects.filter(worker=auth["user_id"])
        serializer = MachinesHistorySerializer(histories, many=True)
        res = response_handler(
            response_status=ResponseStatus.SUCCESS.value,
            result=serializer.data,
            status_code=status.HTTP_200_OK,
        )
        return res
