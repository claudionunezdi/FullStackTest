import decimal
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncDate


from .models import Account, Withdrawal, AccountStatus, Deposit
from .domain_exceptions import(
AccountNotActive,InsufficientFunds,AmountOutOfPolicy,DailyLimitExceeded,DuplicateRequest
)


class WithdrawalService:
    """
    Caso de uso: Retiro de dinero
    """

    @staticmethod
    @transaction.atomic
    def withdraw(*, account_id: int, amount: Decimal, channel: str, request_id: str) -> Withdrawal:
        # 1) Idempotencia → ¿ya se ejecutó con este request_id?
        if Withdrawal.objects.filter(request_id=request_id).exists():
            raise DuplicateRequest("Ya se procesó un retiro con este request_id.")

        # 2) Concurrencia: lock de fila de la cuenta
        account = Account.objects.select_for_update().get(pk=account_id)

        # 3) Validaciones de negocio
        if account.status != AccountStatus.ACTIVE:
            raise AccountNotActive("La cuenta no está activa.")

        if amount <= 0 or amount > account.per_tx_limit:
            raise AmountOutOfPolicy("Monto inválido o excede el límite por transacción.")

        if account.balance < amount:
            raise InsufficientFunds("Fondos insuficientes.")

        # 4) Límite diario
        today = timezone.localdate()
        daily_total = (
            account.withdrawals.filter(created_at__date=today)
            .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        )

        if daily_total + amount > account.daily_limit:
            raise DailyLimitExceeded("Supera el límite diario de retiros.")

        # 5) Aplicar efecto -> descontar saldo
        account.balance = account.balance - amount
        account.save(update_fields=["balance"])

        # 6) Registrar retiro
        withdrawal = Withdrawal.objects.create(
            account=account,
            amount=amount,
            channel=channel,
            request_id=request_id,
        )

        return withdrawal

class DepositService:
    """
    Caso de uso Deposito a la cuenta.
    - Verifica que la cuenta este activa
    - Verifica que el monto sea valido
    - Aplica el abono de forma transaccional
    """

    @staticmethod
    @transaction.atomic
    def deposit(*,
                account_id: int,
                amount: Decimal,
                channel: str = "APP",)-> Account:
        account = Account.objects.select_for_update().get(pk=account_id)
        if account.status != AccountStatus.ACTIVE:
            raise AccountNotActive("[Error] la cuenta no esta activa")

        if amount <= 0:
            raise AmountOutOfPolicy("[ERROR] el monto sea valido")


        # Efecto Economico

        account.balance = account.balance + amount
        account.save(update_fields=["balance"])


        return account


class DepositService:
    @staticmethod
    @transaction.atomic
    def deposit(*,account_id: int, amount: Decimal,
                channel: str)->Account:
        account = Account.objects.select_for_update().get(pk=account_id)

        if account.status != AccountStatus.ACTIVE:
            raise AccountNotActive("[Error] la cuenta no esta activa")
        if amount <= 0:
            raise AmountOutOfPolicy("[ERROR] el monto sea valido")


        #Creditar
        account.balance = account.balance + amount
        account.save(update_fields=["balance"])


        #Registrar el hecho
        Deposit.objects.create(account=account,amount=amount,channel=channel)

        return account





