import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add backend directory to Python path
backend_path = str(Path(__file__).parent.parent)
sys.path.insert(0, backend_path)
# Set test environment variables before any imports
os.environ.update(
    {
        "LOOKER_BASE_URL": "https://test.looker.com:19999",
        "LOOKER_CLIENT_ID": "test_id",
        "LOOKER_CLIENT_SECRET": "test_secret",
        "LOOKER_VERIFY_SSL": "True",
        "LOOKER_TIMEOUT": "120",
    }
)


@pytest.fixture(scope="session", autouse=True)
def mock_settings_env():
    """Maintain test environment configuration throughout the test session"""
    with patch.dict(
        os.environ,
        {
            "LOOKER_BASE_URL": "https://test.looker.com:19999",
            "LOOKER_CLIENT_ID": "test_id",
            "LOOKER_CLIENT_SECRET": "test_secret",
            "LOOKER_VERIFY_SSL": "True",
            "LOOKER_TIMEOUT": "120",
        },
    ):
        yield
