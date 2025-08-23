import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_login_user():
    user = User.objects.create_user(
        username="claudiouser",
        email="claudio@example.com",
        password="123456"
    )
    
    
    client = APIClient()
    payload = {"username": "claudiouser", "password":"123456"}
    
    response = client.post("/api/auth/login/", payload, format="json")
    
    
    assert response.status_code == 200 # type: ignore
    data = response.json() # type: ignore
    assert "access" in data
    assert "refresh" in data
    