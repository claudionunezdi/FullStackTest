# nucleo/tests/test_deposits.py
import pytest
import uuid
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from nucleo.models import Account, AccountStatus


@pytest.mark.django_db
def test_successful_deposit():
    user = User.objects.create_user(
        username="claudio",
        password="123456",
    )
    account = Account.objects.create(
        owner=user,
        number="002-0001",
        currency="CLP",
        balance=Decimal("1000.00"),
    )
    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "amount": Decimal("123456.00"),
        "channel": "APP",
    }


    response = client.post(f"/api/accounts/{account.id}/deposit/", payload, format="json")

    assert response.status_code == 201
    data = response.json()
    # El balance ahora debe reflejar el depósito
    assert data["balance"] == "124456.00"


@pytest.mark.django_db
def test_deposit_inactive_account():
    user = User.objects.create_user(
        username="claudio",
        password="123456",
    )
    account = Account.objects.create(
        owner=user,
        number="002-0002",
        currency="CLP",
        balance=Decimal("100000.00"),
        status=AccountStatus.FROZEN,
    )
    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "amount": Decimal("50000.00"),
        "channel": "APP",
    }


    response = client.post(f"/api/accounts/{account.id}/deposit/", payload, format="json")

    # Cuenta congelada → 409
    assert response.status_code == 409

    account.refresh_from_db()
    assert account.balance == Decimal("100000.00")
    assert account.status == AccountStatus.FROZEN
