"""accounts와 관련하여 사용되는 serializer."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .tokens import TokenObtainPairResponseSerializer

accounts = get_user_model()


class AccountsRegisterSerializer(serializers.ModelSerializer):
    """계정 생성을 위한 Serializer."""

    class Meta:
        """AccountsRegisterSerializer Metadata."""

        model = accounts
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """계정을 생성함.

        Args:
            validated_data (dict): validation된 데이터

        Returns:
            models.Model: 계정 생성.
        """
        return accounts.objects.create_user(**validated_data)


class AccountsLoginSerializer(serializers.ModelSerializer):
    """로그인을 위한 Serializer."""

    class Meta:
        """AccountsLoginSerializer Metadata."""

        model = accounts
        read_only_fields = ("id",)
        exclude = [
            "password",
        ]


class RequestAccountLoginSerializer(serializers.Serializer):
    """로그인 필요한 request의 body구조를 정의함."""

    username = serializers.CharField()
    password = serializers.CharField()


class RequestAccountsRegisterSerializer(serializers.Serializer):
    """계정 생성에 필요한 request의 body구조를 정의함."""

    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class ResponseRegisterResultUserField(serializers.Serializer):
    """계정 생성에 성공하였을 때, response body의 result의 형식을 정의함."""

    user = AccountsRegisterSerializer()
    token = TokenObtainPairResponseSerializer()


class ResponseSuccessAccountsRegisterSerializer(serializers.Serializer):
    """계정 생성에 성공하였을 때 response의 body를 정의함."""

    status = serializers.IntegerField(default=1)
    result = ResponseRegisterResultUserField()


class ResponseLoginResultUserField(serializers.Serializer):
    """로그인에 성공하였을 때, response body의 result의 형식을 정의함."""

    user = AccountsLoginSerializer()
    token = TokenObtainPairResponseSerializer()


class ResponseSuccessAccountsLoginSerializer(serializers.Serializer):
    """로그인에 성공하였을 때 response의 body를 정의함."""

    status = serializers.IntegerField(default=1)
    result = ResponseLoginResultUserField()
