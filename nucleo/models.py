import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower

from django.template.defaultfilters import default_if_none

# Create your models here.

User = get_user_model()

class AccountStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Activa"
    FROZEN = "FROZEN", "Congelada"
    CLOSED = "CLOSED", "Cerrada"


class Account(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accounts')
    number = models.CharField(max_length=30, unique=True)
    currency = models.CharField(max_length=3, default='CLP')
    currency_to_USD = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=10, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)

    '''
    Aqui establecemos cuanto es el maximo que se puede retirar como test quiero ver si el numero puede separarse con "_" 
    cuando se trata de Django
    '''
    per_tx_limit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('2000000.00'))
    daily_limit = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("500000.00")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["number"]),


        ]
        constraints = [
            models.UniqueConstraint(fields=["owner","number"], name="unique_account_number")
        ]

    def __str__(self):
        return f"{self.number} ({self.currency})"

    # ——— Invariantes del dominio (POO) ———
    def can_withdraw(self, amount: Decimal) -> bool:
        return (
            self.status == AccountStatus.ACTIVE and
            amount > 0 and
            amount <= self.per_tx_limit and
            self.balance >= amount
        )

    def clean(self):
        if self.number:
            self.number = self.number.strip()

    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("number"), name= "unique_account_number")
        ]

class Withdrawal(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    channel = models.CharField(max_length=30,default="APP")

    """
    Como evitamos los retiros duplicados?
    asi
    """

    request_id = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['account',"created_at"]),


        ]

    def __str__(self):
        return f"Withdrawal {self.amount} {self.account.currency} #{self.id}"



class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=18,decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    channel = models.CharField(max_length=30,default="APP")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        indexes = [
            models.Index(fields=['account',"created_at"]),
        ]


    def __str__(self):
        return f"Deposit {self.amount} {self.account.currency} #{self.id}"


