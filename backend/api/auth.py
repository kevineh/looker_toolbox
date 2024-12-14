from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from services.looker_client import LookerClient
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from utils.auth_utils import create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
looker_client = LookerClient()

@router.post("/login")
async def login(credentials: Dict):
    """
    Authenticate with Looker API and return access token
    """

    try:
        sdk = looker_client.create_client(credentials)
        if looker_client.validate_connection(sdk):
            access_token = create_access_token(
                data={"client_id": credentials["client_id"]},
                expires_delta=timedelta(hours=8),
            )
            return {"access_token": access_token, "token_type": "bearer"}
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/verify")
async def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verify token and return current user info
    """

    try:
        sdk = looker_client.create_client()
        user_info = sdk.me()
        return {
            "verified": True,
            "user": {
                "id": user_info.id,
                "email": user_info.email,
                "display_name": user_info.display_name,
            },
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
