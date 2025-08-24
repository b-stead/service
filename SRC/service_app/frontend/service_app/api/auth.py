import jwt
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authentication import BaseAuthentication
import requests
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
# verifies the Google ID token and extracts the user's subject (sub)


def jwks_client_for_issuer(iss: str) -> jwt.PyJWKClient:
    """Fetch JWKS client for the issuer."""
    response = requests.get(f"{iss}/.well-known/openid-configuration", timeout=5)
    jwks_uri = response.json()["jwks_uri"]
    return jwt.PyJWKClient(uri=jwks_uri)


def authenticate_user(id_token: str) -> str | None:
    """Verify the Google ID token and return the subject (sub)."""
    unverified_payload = jwt.decode(id_token, options={"verify_signature": False})
    iss = unverified_payload.get("iss")
    if iss != settings.TOKEN_ISSUER:
        return None
    jwks_client = jwks_client_for_issuer(settings.TOKEN_ISSUER)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    payload = jwt.decode(id_token, signing_key.key, audience=settings.TOKEN_AUDIENCE)
    return payload.get("sub")


def create_access_token(
    data: dict, lifetime: timedelta = timedelta(seconds=settings.TOKEN_LIFETIME_SECONDS)
) -> str:
    """Create a signed access token."""
    _data = data.copy()
    expires = datetime.utcnow() + lifetime
    _data.update({"exp": expires})
    return jwt.encode(_data, settings.SECRET_KEY, algorithm="HS256")


def validate_access_token(token: str) -> str:
    """Validate the access token and return the subject (sub)."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            leeway=timedelta(seconds=settings.TOKEN_LEEWAY_SECONDS),
        )
    except jwt.PyJWTError as err:
        raise AuthenticationFailed(f"Invalid token: {err}")
    sub = payload.get("sub")
    if not sub:
        raise AuthenticationFailed("Token does not contain a subject.")
    if not User.objects.filter(sub=sub).exists():
        raise AuthenticationFailed("User does not exist.")
    return sub


class CustomAccessToken(AccessToken):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload["sub"] = str(user.sub)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Generate custom access token
        refresh = RefreshToken.for_user(self.user)
        access = CustomAccessToken(self.user)  # Use the custom access token class

        data["refresh"] = str(refresh)
        data["access"] = str(access)
        return data


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            print("No Authorization header or invalid format")
            return None

        token = auth_header.split(" ")[1]
        try:
            decoded_token = AccessToken(token)
            sub = decoded_token.get("sub")
            if not sub:
                raise Exception("Token does not contain a subject")
            user = User.objects.get(sub=sub)
            return (user, None)
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
