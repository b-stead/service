from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import jwt
from datetime import timedelta
from backend.db import Store
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.config import SECRET_KEY, TOKEN_LEEWAY_SECONDS
import structlog

logger = structlog.get_logger(module=__name__)
router = APIRouter()


class TokenRequest(BaseModel):
    id_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


backendScheme = HTTPBearer(bearerFormat="JWT")


async def valid_user(store: Store, token: Annotated[HTTPAuthorizationCredentials, Depends(backendScheme)]) -> str:
    """Confirm that the access token is valid and that the user exists in the database"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=['HS256'], leeway=timedelta(seconds=TOKEN_LEEWAY_SECONDS))
    except jwt.PyJWTError as err:
        logger.warning(f"access attempt with invalid token: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    sub: str | None = payload.get('sub')
    if sub is None:
        logger.warning("access attempt with token without subject")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        result = await store.valid_user(sub=sub)
    except Exception as err:
        logger.error(f"unexpected error: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if result is None:
        logger.warning("access attempt with token for non-existent user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return sub
Actor = Annotated[str, Depends(valid_user)]


async def valid_new_user(token: Annotated[HTTPAuthorizationCredentials, Depends(backendScheme)]) -> str:
    """Confirm only that the access token is valid"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=['HS256'], leeway=timedelta(seconds=TOKEN_LEEWAY_SECONDS))
    except jwt.PyJWTError as err:
        logger.warning(f"access attempt with invalid token: {err}", exc_info=err)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    sub: str | None = payload.get('sub')
    if sub is None:
        logger.warning("access attempt with token without subject")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return sub
NewActor = Annotated[str, Depends(valid_new_user)]


# @lru_cache
# def jwks_client_for_issuer(iss: str) -> jwt.PyJWKClient:
#   response = requests.get(f"{iss}/.well-known/openid-configuration", timeout=5)
#   return jwt.PyJWKClient(uri=response.json()['jwks_uri'])

# def create_access_token(data: dict[Any, Any], lifetime: timedelta = timedelta(seconds=TOKEN_LIFETIME_SECONDS)) -> str:
#   """Create a signed access token from the provided data"""
#   _data = data.copy()
#   expires = datetime.now() + lifetime
#   _data.update({'exp': expires})
#   return jwt.encode(_data, SECRET_KEY, algorithm='HS256')


# async def authenticate_user(id_token: str) -> str | None:
#   """Confirm with the issuer that the users's ID token is valid, and return the subject"""
#   unverified_payload = jwt.decode(id_token, options={"verify_signature": False})
#   iss = unverified_payload.get('iss')
#   payload = {}
#   if iss == TOKEN_ISSUER:
#     jwks_client = jwks_client_for_issuer(TOKEN_ISSUER)
#     id_signing_key = jwks_client.get_signing_key_from_jwt(id_token)
#     payload = jwt.decode(id_token, id_signing_key, audience=TOKEN_AUDIENCE)
#   return payload.get('sub')


# @router.post("/token", response_model=TokenResponse)
# async def login(token_request: TokenRequest) -> TokenResponse:
#   """Exchange a valid ID token for an access token. Note that the user may not exist in our database."""
#   try:
#     sub = await authenticate_user(id_token=token_request.id_token)
#   except (jwt.exceptions.InvalidTokenError) as err:
#     logger.warning(f"login attempt with invalid id token: {err}", exc_info=err)
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#   if not sub:
#     logger.warning("login attempt with unaccceptable id token: either the issuer could not be determined, the issue or audience is unexpected, or the sub could not be found")
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#   try:
#     access_token = create_access_token(data={'sub': sub})
#     return TokenResponse(access_token=access_token, token_type='bearer', expires_in=TOKEN_LIFETIME_SECONDS)
#   except Exception as err:
#     logger.error(f"unexpected error: {err}", exc_info=err)
#     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# backendScheme = HTTPBearer(bearerFormat="JWT")
