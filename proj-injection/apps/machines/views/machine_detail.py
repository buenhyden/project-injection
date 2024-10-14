"""특정 사출기의 CRUD 요청을 다루기 위한 파일."""

from django.http import Http404
from drf_yasg.openapi import TYPE_INTEGER, TYPE_OBJECT, TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
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
)


class MachineDetailView(APIView):
    """특정 사출기를 다루기 위한 APIView."""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Primary Key를 이용하여 데이터베이스의 저장되어 있는 데이터를 조회한다.

        _extended_summary_

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
        responses={
            200: ResponseSuccessMachineDetailSerializer,
            400: set_fail_response_schema(400),
            401: set_fail_response_schema(401),
            403: set_fail_response_schema(403),
            404: set_fail_response_schema(404),
            405: set_fail_response_schema(405),
            406: set_fail_response_schema(406),
            415: set_fail_response_schema(415),
            429: set_fail_response_schema(429),
            500: set_fail_response_schema(500),
        }
    )
    def get(self, request, pk, format=None):
        """특정 사출기의 정보를 조회한다.

        인증된 사용자는 특정 사출기의 정보를 조회할 수 있다.

        Args:
            request (Request): HttpRequest object
            pk (int): InjectionMoldingMachines의 Primary Key
            format (str, optional): API 요청 시 응답 포맷을 지정하는 데 사용. Defaults to None.

        Returns:
            rest_framework.response.Response: 특정 사출기 정보 요청에 대한 응답
        """
        obj = self.get_object(pk)
        serializer = MachinesSerializer(obj)
        res = response_handler(
            response_status=ResponseStatus.SUCCESS.value,
            result=serializer.data,
            status_code=status.HTTP_200_OK,
        )
        return res

    @swagger_auto_schema(
        responses={
            202: ResponseSuccessMachineDetailSerializer,
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
    def put(self, request, pk, format=None):
        """사출기의 정보를 수정한다.

        인증된 사용자는 자신이 추가한 사출기의 정보를 수정할 수 있다.

        Args:
            request (Request): HttpRequest object
            pk (int): InjectionMoldingMachines의 Primary Key
            format (str, optional): API 요청 시 응답 포맷을 지정하는 데 사용. Defaults to None.

        Returns:
            rest_framework.response.Response: 사출기 정보 수정 요청에 대한 응답
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

        serializer = MachinesSerializer(obj, data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = response_handler(
                response_status=ResponseStatus.SUCCESS.value,
                result=serializer.data,
                status_code=status.HTTP_202_ACCEPTED,
            )
            return res
        res = response_handler(
            response_status=ResponseStatus.FAIL.value,
            result=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return res

    @swagger_auto_schema(
        responses={
            204: Schema(
                type=TYPE_OBJECT,
                properties={
                    "message": Schema(
                        "message", description="사출기 삭제 성공", type=TYPE_STRING
                    ),
                    "status": Schema(
                        "Response Status Code",
                        description="Response Status",
                        type=TYPE_INTEGER,
                        default=ResponseStatus.SUCCESS.value,
                    ),
                },
            ),
            400: set_fail_response_schema(400),
            401: set_fail_response_schema(401),
            403: set_fail_response_schema(403),
            404: set_fail_response_schema(404),
            405: set_fail_response_schema(405),
            406: set_fail_response_schema(406),
            415: set_fail_response_schema(415),
            429: set_fail_response_schema(429),
            500: set_fail_response_schema(500),
        }
    )
    def delete(self, request, pk, format=None):
        """사출기를 삭제한다.

        인증된 사용자는 자신이 추가한 사출기를 삭제할 수 있다.

        Args:
            request (Request): HttpRequest object
            pk (int): InjectionMoldingMachines의 Primary Key
            format (str, optional): API 요청 시 응답 포맷을 지정하는 데 사용. Defaults to None.

        Returns:
            rest_framework.response.Response: 사출기 삭제 요청에 대한 응답
        """
        result = {}
        auth = request.auth.payload
        if auth is None:
            raise NotAuthenticated
        requested_user_id = auth["user_id"]

        obj = self.get_object(pk)
        obj_owner_id = obj.owner_id
        if requested_user_id != obj_owner_id:
            raise PermissionDenied
        obj.delete()
        result["message"] = "machine deleted"
        res = response_handler(
            response_status=ResponseStatus.SUCCESS.value,
            result=result,
            status_code=status.HTTP_204_NO_CONTENT,
        )
        return res
