"""JWT token 관련하여 사용되는 serializer."""

from rest_framework import serializers


class TokenObtainPairResponseSerializer(serializers.Serializer):
    """로그인 혹은 계정 생성을 할 경우, token이 생성되고 body의 token에 실려오는 값에 대한 정의."""

    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    """token을 갱신할 경우, body의 token에 실려오는 값에 대한 정의."""

    access = serializers.CharField()


class TokenVerifyResponseSerializer(serializers.Serializer):
    """token을 검증할 경우, 요청하는 body에 대한 정의."""

    token = serializers.CharField()
