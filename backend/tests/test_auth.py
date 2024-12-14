import pytest
from fastapi.testclient import TestClient
from main import app
from services.looker_client import LookerClient

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/api/auth/login", json={"client_id": "test_id", "client_secret": "test_secret"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_login_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        json={"client_id": "invalid_id", "client_secret": "invalid_secret"},
    )
    assert response.status_code == 401


def test_verify_token():
    # First login to get token
    login_response = client.post(
        "/api/auth/login", json={"client_id": "test_id", "client_secret": "test_secret"}
    )
    token = login_response.json()["access_token"]

    # Test token verification
    response = client.get(
        "/api/auth/verify", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["verified"] == True
