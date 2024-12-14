from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.auth_utils import verify_token
from services.looker_client import LookerClient

security = HTTPBearer()
looker_client = LookerClient()


async def verify_token_middleware(
    request: Request, credentials: HTTPAuthorizationCredentials = security
):
    """
    Middleware to verify JWT token and validate Looker session
    """
    token = credentials.credentials
    payload = verify_token(token)

    # Verify Looker session is still valid
    sdk = looker_client.create_client()
    if not looker_client.validate_connection(sdk):
        raise HTTPException(status_code=401, detail="Looker session expired")

    request.state.user = payload
    return payload
