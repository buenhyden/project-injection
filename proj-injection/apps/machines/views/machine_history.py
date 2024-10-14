"""특정 사출기의 작업 기록에 대한 요청을 다루기 위한 파일."""

from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from base_modules.response_handler import response_handler
from base_modules.swagger_schema_view import set_fail_response_schema
from defines import ResponseStatus

from ..models import InjectionMoldingMachines, MachinesHistory
from ..serializers import (
    MachinesHistorySerializer,
    ResponseSuccessMachineHistorySerializer,
)


class MachineHistoryView(APIView):
    """사출기의 작업 기록을 다루기 위한 APIView."""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Primary Key를 이용하여 데이터베이스의 저장되어 있는 데이터를 조회한다.

        Args:
            pk (int): InjectionMoldingMachines의 Primary Key

        Raises:
            Http404: primary key에 대한 조회 결과 없을 경우 Http status code(404) 발생

        Returns:
            models.Model : InjectionMoldingMachines
        """
        try:
            return InjectionMoldingMachines.objects.get(pk=pk)
        except InjectionMoldingMachines.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_id="machines_history_list",
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
    )
    def get(self, request, pk, format=None):
        """특정 사출기의 작업 기록을 조회한다.

        인증된 사용자는 특정 사출기에 대한 작업 기록을 조회할 수 있다.

        Args:
            request (Request): HttpRequest object
            pk (int): InjectionMoldingMachines의 Primary Key
            format (str, optional): API 요청 시 응답 포맷을 지정하는 데 사용. Defaults to None.

        Returns:
            rest_framework.response.Response: 사출기 작업 기록 요청에 대한 응답
        """
        request_data = request.data
        auth = request.auth.payload
        if auth is None:
            raise NotAuthenticated
        request_data["owner_id"] = auth["user_id"]
        requested_user_id = auth["user_id"]

        obj = self.get_object(pk)
        obj_owner_id = obj.owner_id
        if requested_user_id != obj_owner_id:
            raise PermissionDenied
        histories = MachinesHistory.objects.filter(machine_id=obj.pk)
        serializer = MachinesHistorySerializer(histories, many=True)
        res = response_handler(
            response_status=ResponseStatus.SUCCESS.value,
            result=serializer.data,
            status_code=status.HTTP_200_OK,
        )
        return res
