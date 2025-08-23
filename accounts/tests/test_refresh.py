import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_refresh_token():
    user = User.objects.create_user(
        username="claudiouser",
        email="claudio@example.com",
        password="123456"
    )
    
    client = APIClient()
    login_res = client.post("/api/auth/login/", {"username": "claudiouser", "password": "123456"}, format="json")
    
    refresh_token = login_res.json()["refresh"]
    
    response = client.post("/api/auth/refresh/", {"refresh": refresh_token}, format="json")

    
    assert response.status_code == 200
    data = response.json()
    assert "access" in data