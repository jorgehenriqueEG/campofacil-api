import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

load_dotenv()

_KEYCLOAK_URL = os.environ["KEYCLOAK_URL"]
_KEYCLOAK_REALM = os.environ["KEYCLOAK_REALM"]
_ISSUER = f"{_KEYCLOAK_URL}/realms/{_KEYCLOAK_REALM}"
_JWKS_URL = f"{_ISSUER}/protocol/openid-connect/certs"

# Fetches and caches Keycloak's public keys; re-fetches on unknown kid (key rotation).
_jwks_client = PyJWKClient(_JWKS_URL, cache_keys=True)

_bearer = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> dict:
    token = credentials.credentials
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=_ISSUER,
            # Audience is realm-specific and depends on Keycloak client configuration.
            # Signature + issuer validation already proves the token came from our Keycloak.
            options={"verify_aud": False},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token issuer")
    except jwt.PyJWKClientError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to fetch signing keys")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload
