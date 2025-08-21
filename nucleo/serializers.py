from rest_framework import serializers
from nucleo.models import Account, Withdrawal, Deposit



class WithdrawalRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    channel = serializers.CharField(max_length=30, default="APP")
    request_id = serializers.CharField(max_length=64)

class WithdrawalResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ["id", "amount", "channel", "request_id","created_at", ]


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ["id", "amount", "channel", "request_id", "created_at"]

class AccountSerializer(serializers.ModelSerializer):
    withdrawals = WithdrawalSerializer(read_only=True, many=True)

    class Meta:
        model = Account
        fields = [
            "id", "number", "currency", "balance", "status",
            "per_tx_limit", "daily_limit", "withdrawals"
        ]
        read_only_fields = ["id", "balance", "status"]


class DepositRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=18,decimal_places=2)
    channel = serializers.CharField(max_length=30, default="APP")


class DepositResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id","number", "currency", "balance", "status",]


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ["id", "amount", "channel", "created_at"]


class MovementSerializer(serializers.Serializer):
    id= serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    channel = serializers.CharField()
    created_at = serializers.DateTimeField()



