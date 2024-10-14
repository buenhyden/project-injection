"""app(machines)의 InjectionMoldingMachines관련 serializers."""

from rest_framework import serializers

from ..models import InjectionMoldingMachines


class MachinesSerializer(serializers.ModelSerializer):
    """사출기 관련 데이터에 대한 Serializer."""

    class Meta:
        """MachinesSerializer Metadata."""

        model = InjectionMoldingMachines
        fields = "__all__"
        read_only_fields = ("id",)


class RequestMachineSerializer(serializers.Serializer):
    """사출기 데이터의 생성 및 수정에 필요한 request의 body 구조를 정의함."""

    name = serializers.CharField()
    location = serializers.CharField()


class ResponseSuccessMachineListSerializer(serializers.Serializer):
    """사출기 데이터의 목록 조회에 성공하였을 때, response body 구조를 정의함."""

    status = serializers.IntegerField(default=1)
    result = MachinesSerializer(many=True)


class ResponseSuccessMachineDetailSerializer(serializers.Serializer):
    """특정 사출기의 조회, 사출기 데이터 생성 및 수정에 성공하였을 때, response body 구조를 정의함."""

    status = serializers.IntegerField(default=1)
    result = MachinesSerializer(many=False)


class RequestOperationSerializer(serializers.Serializer):
    """사출기의 작업을 시작/중지하기 위해 필요한 request의 body 구조를 정의함."""

    command = serializers.CharField(default="START")


class ResponseOperationSerializer(serializers.Serializer):
    """사출기의 작업을 시작/중지에 성공하였을 때, response body 구조를 정의함."""

    status = serializers.IntegerField(default=1)
    message = serializers.CharField()
