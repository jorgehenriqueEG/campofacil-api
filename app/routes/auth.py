import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

load_dotenv()

_KEYCLOAK_URL = os.environ["KEYCLOAK_URL"]
_KEYCLOAK_REALM = os.environ["KEYCLOAK_REALM"]
_TOKEN_URL = f"{_KEYCLOAK_URL}/realms/{_KEYCLOAK_REALM}/protocol/openid-connect/token"
_CLIENT_ID = "campofacil-app"

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str


@router.post("/token", response_model=TokenResponse)
async def login(body: LoginRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _TOKEN_URL,
            data={
                "grant_type": "password",
                "client_id": _CLIENT_ID,
                "username": body.username,
                "password": body.password,
            },
        )

    if response.status_code == 401:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Auth service error")

    data = response.json()
    return TokenResponse(
        access_token=data["access_token"],
        expires_in=data["expires_in"],
        token_type=data["token_type"],
    )
