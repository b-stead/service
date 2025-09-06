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
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "disable")

print(f"POSTGRES_USERNAME: {POSTGRES_USERNAME}")
print(f"POSTGRES_PASSWORD: {POSTGRES_PASSWORD}")
print(f"POSTGRES_HOST: {POSTGRES_HOST}")
print(f"POSTGRES_PORT: {POSTGRES_PORT}")
print(f"POSTGRES_DATABASE: {POSTGRES_DATABASE}")
print(f"POSTGRES_SSLMODE: {POSTGRES_SSLMODE}")