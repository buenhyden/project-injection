"""app(machines)의 MachineHistory관련 serializers."""

from rest_framework import serializers

from ..models import MachinesHistory


class MachinesHistorySerializer(serializers.ModelSerializer):
    """사출기 작업기록 데이터에 대한 Serializer."""

    class Meta:
        """MachinesHistorySerializer Metadata."""

        model = MachinesHistory
        fields = "__all__"
        read_only_fields = ("id",)


class ResponseSuccessMachineHistorySerializer(serializers.Serializer):
    """사출기 작업기록 데이터 조회에 성공하였을 때, response body 구조를 정의함."""

    status = serializers.IntegerField(default=1)
    result = MachinesHistorySerializer(many=True)
