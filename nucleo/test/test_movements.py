import pytest
import uuid
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from nucleo.models import Account


@pytest.mark.django_db
def test_movements_list():
    user = User.objects.create_user(username="claudio", password="123456")
    account = Account.objects.create(owner=user,
                                     number="003-0001",
                                     currency="CLP",
                                     balance=Decimal("0.00"),
                                     )
    client = APIClient()
    client.force_authenticate(user=user)


    #Accion Depositar

    client.post(
        f"/api/accounts/{account.id}/deposit/",
        {"amount": "5000.00", "channel":"APP"},
         format="json"
    )

    #Acción Retirar
    client.post(
        f"/api/accounts/{account.id}/withdraw/",
        {"amount": "2000.00", "channel":"APP", "request_id": str(uuid.uuid4())},
        format="json"
    )


    #Resultados
    response = client.get(f"/api/accounts/{account.id}/movements/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {"type"} <= set(data[0].keys())
