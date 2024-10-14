"""app(accounts)의 view를 정의함."""

from django.shortcuts import get_object_or_404
from drf_yasg.openapi import TYPE_INTEGER, TYPE_OBJECT, TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView, status
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import Token

from base_modules.response_handler import response_handler
from base_modules.swagger_schema_view import (
    set_fail_response_schema,
)
from config.settings import SECRET_KEY
from defines import ResponseStatus

from ..models import Accounts
from ..serializers import (
    AccountsLoginSerializer,
    AccountsRegisterSerializer,
    RequestAccountLoginSerializer,
    RequestAccountsRegisterSerializer,
    ResponseSuccessAccountsLoginSerializer,
    ResponseSuccessAccountsRegisterSerializer,
)


class AccountRegisterAPIView(APIView):
    """사용자의 계정을 등록하기 위한 APIView."""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            201: ResponseSuccessAccountsRegisterSerializer,
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
        request_body=RequestAccountsRegisterSerializer,
        tags=["User"],
    )
    def post(self, request: Request):
        """사용자를 시스템에 등록한다.

        사용자 인증을 위해 JWT(JSON Web Token)를 사용.

        Args:
            request (Request): HttpRequest object

        Returns:
            rest_framework.response.Response: 계정 생성 요청에 대한 응답
        """
        serializer = AccountsRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token: Token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            result = {
                "user": serializer.data,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }
            res = response_handler(
                response_status=ResponseStatus.SUCCESS.value,
                result=result,
                status_code=status.HTTP_201_CREATED,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        res = response_handler(
            response_status=ResponseStatus.FAIL.value,
            result=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return res


class AccountLoginAPIView(APIView):
    """사용자의 로그인을 관리하기 위한 APIView Class."""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: ResponseSuccessAccountsLoginSerializer,
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
        tags=["User"],
    )
    def get(self, request: Request):
        """시스템에 등록된 사용자가 토큰을 이용하여 사용자의 정보를 확인한다.

        사용자 인증을 위해 JWT(JSON Web Token)를 사용.
        토큰이 만료되었을 경우, 토큰을 갱신한다.

        Args:
            request (Request): HttpRequest object

        Returns:
            rest_framework.response.Response: 계정 정보 요청에 대한 응답
        """
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            if "access" not in request.COOKIES:
                raise NotAuthenticated
            access = request.COOKIES["access"]
            payload = decode(access, SECRET_KEY, algorithms=["HS256"])
            pk = payload.get("user_id")
            user = get_object_or_404(Accounts, pk=pk)
            serializer = AccountsLoginSerializer(instance=user)
            res = response_handler(
                response_status=ResponseStatus.SUCCESS.value,
                result=serializer.data,
                status_code=status.HTTP_200_OK,
            )
            return res

        except ExpiredSignatureError:
            # 토큰 만료 시 토큰 갱신
            refresh = request.COOKIES.get("refresh", None)
            data = {"refresh": refresh}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                token = serializer.validated_data
                access = token["access"]
                payload = decode(access, SECRET_KEY, algorithms=["HS256"])
                pk = payload.get("user_id")
                user = get_object_or_404(Accounts, pk=pk)
                serializer = AccountsLoginSerializer(instance=user)
                res = response_handler(
                    response_status=ResponseStatus.SUCCESS.value,
                    result=serializer.data,
                    status_code=status.HTTP_200_OK,
                )
                res.set_cookie("access", access)
                res.set_cookie("refresh", refresh)
                return res
            raise InvalidTokenError

        except InvalidTokenError:
            raise InvalidTokenError
        except NotAuthenticated:
            raise NotAuthenticated

    @swagger_auto_schema(
        responses={
            200: ResponseSuccessAccountsLoginSerializer,
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
        request_body=RequestAccountLoginSerializer,
        tags=["User"],
    )
    def post(self, request: Request):
        """시스템에 등록된 사용자가 로그인한다.

        사용자 인증을 위해 JWT(JSON Web Token)를 사용.

        Args:
            request (Request): HttpRequest object

        Returns:
            rest_framework.response.Response: 로그인 요청에 대한 응답
        """
        token_serializer = TokenObtainPairSerializer(data=request.data)
        if token_serializer.is_valid(raise_exception=True):
            user = token_serializer.user
            serializer = AccountsLoginSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            result = {
                "user": serializer.data,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            }
            res = response_handler(
                response_status=ResponseStatus.SUCCESS.value,
                result=result,
                status_code=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        res = response_handler(
            response_status=ResponseStatus.FAIL.value,
            result=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return res


class AccountLogoutAPIView(APIView):
    """사용자의 로그아웃을 관리하기 위한 APIView Class."""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            202: Schema(
                type=TYPE_OBJECT,
                properties={
                    "message": Schema(
                        "message", description="로그아웃 성공", type=TYPE_STRING
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
        },
        tags=["User"],
    )
    def post(self, request):
        """로그아웃을 한다.

        response에서 token을 삭제한다.

        Args:
            request (Request): HttpRequest object

        Returns:
            rest_framework.response.Response: 로그아웃 요청에 대한 응답
        """
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        result = {}
        result["message"] = "logout success"
        res = response_handler(
            response_status=ResponseStatus.SUCCESS.value,
            result=result,
            status_code=status.HTTP_202_ACCEPTED,
        )
        res.delete_cookie("access")
        res.delete_cookie("refresh")
        return res
