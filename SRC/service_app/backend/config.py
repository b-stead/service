import os


def getenv_or_panic(env: str) -> str:
    value = os.getenv(env)
    if value is None:
        raise RuntimeError(f"{env} is required")
    return value


# Required configuration
SECRET_KEY = getenv_or_panic("SECRET_KEY")
# TOKEN_ISSUER = getenv_or_panic("TOKEN_ISSUER")
# TOKEN_AUDIENCE = getenv_or_panic("TOKEN_AUDIENCE")

# Optional configuration
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "disable")
LOG_STYLE = os.getenv("LOG_STYLE", "json")
LOG_LEVEL = os.getenv("LOG_LEVEL", "debug")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TOKEN_LIFETIME_SECONDS = int(os.getenv("TOKEN_LIFETIME_SECONDS", "3600"))
TOKEN_LEEWAY_SECONDS = int(os.getenv("TOKEN_LEEWAY_SECONDS", "60"))
TEST_ENVIRONMENT = os.getenv("TEST_ENVIRONMENT", "false") == "true"
