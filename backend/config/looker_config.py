from typing import Optional
from pydantic import BaseSettings


class LookerSettings(BaseSettings):
    """
    Looker SDK configuration settings
    """

    base_url: str
    client_id: str
    client_secret: str
    verify_ssl: bool = True
    timeout: int = 120

    class Config:
        env_file = ".env"
