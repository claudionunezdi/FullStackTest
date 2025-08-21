# nucleo/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from itertools import chain

from nucleo.models import Account, Withdrawal
from nucleo.serializers import (
    AccountSerializer,
    WithdrawalRequestSerializer,
    WithdrawalResponseSerializer,
    WithdrawalSerializer,
    DepositRequestSerializer,
    DepositResponseSerializer,
)
from nucleo.services import WithdrawalService, DepositService
from nucleo.domain_exceptions import (
    AccountNotActive, InsufficientFunds, AmountOutOfPolicy, DailyLimitExceeded, DuplicateRequest
)




class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="withdraw",
        serializer_class=WithdrawalRequestSerializer,
    )
    def withdraw(self, request, pk=None):
        account = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            w = WithdrawalService.withdraw(
                account_id=account.id,
                amount=data["amount"],
                channel=data["channel"],
                request_id=data["request_id"],
            )
            return Response(WithdrawalResponseSerializer(w).data, status=status.HTTP_201_CREATED)

        except InsufficientFunds as e:
            return Response({"detail": str(e)}, status=status.HTTP_402_PAYMENT_REQUIRED)
        except DailyLimitExceeded as e:
            return Response({"detail": str(e)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except AccountNotActive as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)
        except AmountOutOfPolicy as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DuplicateRequest:
            return Response({"detail": "Solicitud duplicada (idempotente)."}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path="deposit",
        serializer_class=DepositRequestSerializer,
    )
    def deposit(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            acc = DepositService.deposit(
                account_id=pk,
                amount=data["amount"],
                channel=data["channel"],
            )
            return Response(
                DepositResponseSerializer(acc).data,
                status=status.HTTP_201_CREATED,
            )
        except AccountNotActive as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)
        except AmountOutOfPolicy as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="movements")
    def movements(self,request,pk=None):
        account = get_object_or_404(self.get_queryset(), pk=pk)

        withdrawals = account.withdrawals.all().values(
            "id", "amount","channel", "created_at"
        )

        for w in withdrawals:
            w["type"] = "withdrawal"
        deposits = account.deposits.all().values(
            "id", "amount", "channel", "created_at"
        )

        for d in deposits:
            d["type"] = "deposit"


        movements = sorted(
            chain(withdrawals, deposits),
            key=lambda m: m["created_at"],
            reverse=True,
        )

        return Response(movements, status=status.HTTP_200_OK)

class WithdrawalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(account__owner=self.request.user)

