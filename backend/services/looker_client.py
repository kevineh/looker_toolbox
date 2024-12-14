import looker_sdk
from config.looker_config import LookerSettings


class LookerClient:
    """
    Looker SDK client wrapper
    """

    def __init__(self):
        self.settings = LookerSettings()

    def create_client(self, api_credentials=None):
        """
        Initialize Looker SDK client with credentials
        """
        if api_credentials:
            # Use provided credentials
            sdk = looker_sdk.init40(
                base_url=self.settings.base_url,
                client_id=api_credentials.get("client_id"),
                client_secret=api_credentials.get("client_secret"),
                verify_ssl=self.settings.verify_ssl,
                timeout=self.settings.timeout,
            )
        else:
            # Use environment variables
            sdk = looker_sdk.init40()

        return sdk

    def validate_connection(self, sdk):
        """
        Test connection with provided credentials
        """
        try:
            sdk.me()
            return True
        except Exception:
            return False
