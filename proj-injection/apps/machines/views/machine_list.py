"""사출기 데이터의 생성 또는 목록 조회에 대한 요청을 다루기 위한 파일"""

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from base_modules.response_handler import response_handler
from base_modules.swagger_schema_view import set_fail_response_schema
from defines import ResponseStatus

from ..models import InjectionMoldingMachines
from ..serializers import (
    MachinesSerializer,
    RequestMachineSerializer,
    ResponseSuccessMachineDetailSerializer,
    ResponseSuccessMachineListSerializer,
)


class MachineListView(APIView):
    """사출기 데이터의 생성 또는 목록 조회를 다루기 위한 APIView."""

    queryset = InjectionMoldingMachines.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: ResponseSuccessMachineListSerializer,
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
        # manual_parameters=[
        #     Parameter(
        #         "page_size",
        #         IN_QUERY,
        #         description="page",
        #         type=TYPE_INTEGER,
        #     )
        # ],
    )
    def get(self, request, format=None):
        """사출기의 전체 목록을 조회한다.

        인증된 사용자는 모든 사출기의 목록을 조회할 수 있다.
        """
        objs = InjectionMoldingMachines.objects.all()
        serializer = MachinesSerializer(objs, many=True)
        res = response_handler(
            response_status=ResponseStatus.SUCCESS.value,
            result=serializer.data,
            status_code=status.HTTP_200_OK,
        )
        return res

    @swagger_auto_schema(
        responses={
            201: ResponseSuccessMachineDetailSerializer,
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
        request_body=RequestMachineSerializer,
    )
    def post(self, request, format=None):
        """새로운 사출기를 추가한다.

        인증된 사용자가 새로운 사출기를 추가할 수 있다.

        Args:
            request (Request): HttpRequest object
            format (str, optional): API 요청 시 응답 포맷을 지정하는 데 사용. Defaults to None.

        Returns:
            rest_framework.response.Response: 사출기 추가 요청에 대한 응답
        """
        request_data = request.data
        auth = request.auth.payload
        if auth is None:
            raise NotAuthenticated
        request_data["owner_id"] = auth["user_id"]
        serializer = MachinesSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = response_handler(
                response_status=ResponseStatus.SUCCESS.value,
                result=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
            return res
        res = response_handler(
            response_status=ResponseStatus.FAIL.value,
            result=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return res
