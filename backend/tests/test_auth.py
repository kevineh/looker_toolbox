import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

client = TestClient(app)


@pytest.fixture
def mock_looker_client():
    with patch("services.looker_client.LookerClient") as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        mock_instance.validate_connection.return_value = True
        yield mock_instance


def test_login_success(mock_looker_client):
    response = client.post(
        "/api/auth/login", json={"client_id": "test_id", "client_secret": "test_secret"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_login_invalid_credentials(mock_looker_client):
    mock_looker_client.validate_connection.return_value = False
    response = client.post(
        "/api/auth/login",
        json={"client_id": "invalid_id", "client_secret": "invalid_secret"},
    )
    assert response.status_code == 401


def test_verify_token(mock_looker_client):
    # First login to get token
    login_response = client.post(
        "/api/auth/login", json={"client_id": "test_id", "client_secret": "test_secret"}
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/auth/verify", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
