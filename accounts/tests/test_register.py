import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    
    payload = {
        "username": "claudiouser",
        "email":"claudio@example.com",
        "password": "123456",
    }
    
    response = client.post("/api/auth/register/", payload, format="json")
    
    
    assert response.status_code == 201 # type: ignore
    assert User.objects.filter(username="claudiouser").exists()
    