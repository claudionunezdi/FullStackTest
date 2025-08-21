import uuid

import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from nucleo.models import Account, AccountStatus




@pytest.mark.django_db
def test_successful_withdrawal():
    #Crear usuario y cuenta
    user = User.objects.create_user(username="claudio", password="123456")
    account = Account.objects.create(
        owner = user,
        number = "001-0001",
        currency = "CLP",
        balance = Decimal("100000.00")
    )


    client = APIClient()
    client.force_authenticate(user=user)


    # Post /api/accounts/<id>/withdraw/

    payload = {
        "amount" : "50000.00",
        "channel" : "APP",
        "request_id" : str(uuid.uuid4())
    }
    response = client.post(f"/api/accounts/{account.id}/withdraw/", payload, format="json")


    #Validaciones

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "50000.00"
    assert data["channel"] == "APP"


    # 4) Question Balance bajó?


    account.refresh_from_db()
    assert account.balance == Decimal("50000.00")

class AccountTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="claudio", password="123456")
        self.account = Account.objects.create(
            owner=self.user,
            number="001-0001",
            currency="CLP",
            balance=Decimal("100000.00"),
        )

    def test_account_creation(self):
        self.assertEqual(self.account.balance, Decimal("100000.00"))
        self.assertEqual(self.account.currency, "CLP")


@pytest.mark.django_db
def test_withdrawal_insufficient_funds():
    user = User.objects.create_user(username="claudio", password="123456")
    account = Account.objects.create(
        owner=user,
        number="001-0001",
        currency="CLP",
        balance=Decimal("1000.00"),
    )
    client = APIClient()
    client.force_authenticate(user=user)
    ##Cargo a la cuenta supera el valor de la cuenta.
    payload= {
        "amount" : "50000.00",
        "channel" : "APP",
        "request_id" : str(uuid.uuid4())

    }
    response = client.post(f"/api/accounts/{account.id}/withdraw/", payload, format="json")
    #Solo arroja el codigo 402 y no altera ningun cambio.
    assert  response.status_code == 402 #Status Insuficientes.
    account.refresh_from_db()
    assert account.balance == Decimal("1000.00")



@pytest.mark.django_db
def  test_withdrawal_account_inactive():
    user = User.objects.create_user(username="claudio", password="123456")
    account = Account.objects.create(
        owner=user,
        number="001-0002", currency="CLP",
        balance=Decimal("100000.00"),
        status= AccountStatus.FROZEN
    )
    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "amount" : "50000.00",
        "channel" : "APP",
        "request_id" : str(uuid.uuid4())
    }
    response = client.post(f"/api/accounts/{account.id}/withdraw/", payload, format="json")

    assert response.status_code == 409
    account.refresh_from_db()
    assert account.balance == Decimal("100000.00")
    assert account.status == "FROZEN"
    assert account.status == AccountStatus.FROZEN




@pytest.mark.django_db
def test_withdrawal_exceeds_daily_limit():
    user = User.objects.create_user(username="claudio", password="123456")
    account = Account.objects.create(
        owner=user,
        number="001-0003",
        currency="CLP",
        balance=Decimal("100000.00"),
        daily_limit=Decimal("2000.00")
    )
    client = APIClient()
    client.force_authenticate(user=user)

    payload1 = {
        "amount" : "1500.00",
        "channel" : "APP",
        "request_id" : str(uuid.uuid4())
    }
    r1= client.post(f"/api/accounts/{account.id}/withdraw/", payload1, format="json")
    assert r1.status_code == 201

    #ESTO GENERA ERROR(si lo genera. bien!)
    payload2 = {
        "amount" : "1000.00",
        "channel" : "APP",
        "request_id" : str(uuid.uuid4())
    }
    r2 = client.post(f"/api/accounts/{account.id}/withdraw/", payload2, format="json")
    assert r2.status_code == 429 #Limite excedido



@pytest.mark.django_db
def test_withdrawal_idempotency():
    user = User.objects.create_user(username="claudio", password="123456")
    account = Account.objects.create(
        owner=user,
        number="001-0004",
        currency="CLP",
        balance=Decimal("100000.00"),

    )

    client = APIClient()
    client.force_authenticate(user=user)

    request_id = str(uuid.uuid4())
    payload = {
        "amount" : "1500.00",
        "channel" : "APP",
        "request_id" : request_id
    }

    response = client.post(f"/api/accounts/{account.id}/withdraw/", payload, format="json")
    assert response.status_code == 201

    #Ahora haremos con el mismo request_id
    r2 = client.post(f"/api/accounts/{account.id}/withdraw/", payload, format="json")
    assert r2.status_code == 200 #Idempotencia
