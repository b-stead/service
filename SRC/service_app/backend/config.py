import os


def getenv_or_panic(env: str) -> str:
  value = os.getenv(env)
  if value is None:
    raise RuntimeError(f"{env} is required")
  return value

# Optional configuration
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "service_app")
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "disable")