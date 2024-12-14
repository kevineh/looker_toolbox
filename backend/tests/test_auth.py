import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

client = TestClient(app)


@pytest.fixture
def mock_looker_client():

    with patch("api.auth.looker_client") as mock:
        mock.validate_connection.return_value = True
        mock.create_client.return_value = Mock()
        yield mock


def test_login_success(mock_looker_client):
    # Configure mock behavior
    mock_looker_client.validate_connection.return_value = True

    # Make request using TestClient
    response = client.post(
        "/api/auth/login", json={"client_id": "test_id", "client_secret": "test_secret"}
    )
    assert response.status_code == 200


def test_login_invalid_credentials(mock_looker_client):

    # Mock both the client creation and validation
    mock_sdk = Mock()
    mock_looker_client.create_client.return_value = mock_sdk
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

    # Mock user info response
    mock_user = Mock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_user.display_name = "Test User"
    mock_looker_client.create_client().me.return_value = mock_user

    response = client.get(
        "/api/auth/verify", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
